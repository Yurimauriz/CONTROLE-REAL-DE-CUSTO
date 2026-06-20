
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    login VARCHAR(50) UNIQUE NOT NULL,
    senha VARCHAR(250) NOT NULL,
    perfil_acesso VARCHAR(30) NOT NULL -- 'Gerente' ou 'Balcão'
);

CREATE TABLE Produto (
    id_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(100) NOT NULL,
    marca VARCHAR(50),
    quantidade_estoque INT NOT NULL DEFAULT 0,
    custo_reposicao NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    preco_venda NUMERIC(10, 2) NOT NULL DEFAULT 0.00,
    id_usuario INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE Venda (
    id_venda SERIAL PRIMARY KEY,
    data_venda TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    valor_total NUMERIC(10, 2) DEFAULT 0.00,
    valor_reposicao NUMERIC(10, 2) DEFAULT 0.00,
    valor_despesas NUMERIC(10, 2) DEFAULT 0.00,
    valor_lucro NUMERIC(10, 2) DEFAULT 0.00,
    id_usuario INT REFERENCES Usuario(id_usuario)
);

CREATE TABLE ItensVenda (
    id_item_venda SERIAL PRIMARY KEY,
    id_venda INT REFERENCES Venda(id_venda) ON DELETE CASCADE,
    id_produto INT REFERENCES Produto(id_produto),
    quantidade_vendida INT NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL
);

-- Soma totais de vendas para o dashboard
CREATE OR REPLACE FUNCTION obter_relatorio_financeiro()
RETURNS TABLE(
    total_receita NUMERIC(10, 2),
    total_reposicao NUMERIC(10, 2),
    total_lucro_liquido NUMERIC(10, 2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        COALESCE(SUM(valor_total), 0.00),
        COALESCE(SUM(valor_reposicao), 0.00),
        COALESCE(SUM(valor_lucro), 0.00)
    FROM Venda;
END;
$$ LANGUAGE plpgsql;

-- Registra uma nova venda
CREATE OR REPLACE PROCEDURE registrar_venda(
    p_id_usuario INT,
    p_produtos INT[],
    p_quantidades INT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id_venda INT;
    v_total_venda NUMERIC(10,2) := 0.00;
    i INT;
    v_preco_un NUMERIC(10,2);
BEGIN
    IF array_length(p_produtos, 1) != array_length(p_quantidades, 1) THEN
        RAISE EXCEPTION 'Erro: A lista de produtos e quantidades não coincide.';
    END IF;

    INSERT INTO Venda (id_usuario, valor_total)
    VALUES (p_id_usuario, 0.00)
    RETURNING id_venda INTO v_id_venda;

    FOR i IN 1..array_length(p_produtos, 1) LOOP
        SELECT preco_venda INTO v_preco_un FROM Produto WHERE id_produto = p_produtos[i];
        
        IF v_preco_un IS NULL THEN
            RAISE EXCEPTION 'Produto com ID % não encontrado.', p_produtos[i];
        END IF;

        INSERT INTO ItensVenda (id_venda, id_produto, quantidade_vendida, preco_unitario)
        VALUES (v_id_venda, p_produtos[i], p_quantidades[i], v_preco_un);

        v_total_venda := v_total_venda + (v_preco_un * p_quantidades[i]);
    END LOOP;

    UPDATE Venda SET valor_total = v_total_venda WHERE id_venda = v_id_venda;

    COMMIT;
    
EXCEPTION
    WHEN OTHERS THEN
        ROLLBACK;
        RAISE EXCEPTION 'Transação Abortada! Motivo: %', SQLERRM;
END;
$$;