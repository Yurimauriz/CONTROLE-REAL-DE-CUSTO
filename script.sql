
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

    -- O valor_total e valor_lucro são atualizados automaticamente na trigger tg_calculo_financeiro
END;
$$;




-- TRIGGER 1: CONTROLAR ESTOQUE AUTOMATICAMENTE E BARRAR SE FALTAR PRODUTO

CREATE OR REPLACE FUNCTION verificar_e_atualizar_estoque()
RETURNS TRIGGER AS $$
BEGIN
   
    IF (SELECT quantidade_estoque FROM Produto WHERE id_produto = NEW.id_produto) < NEW.quantidade_vendida THEN
      
        RAISE EXCEPTION 'Estoque insuficiente para o produto ID %', NEW.id_produto;
    END IF;

    
    UPDATE Produto 
    SET quantidade_estoque = quantidade_estoque - NEW.quantidade_vendida 
    WHERE id_produto = NEW.id_produto;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_controle_estoque
BEFORE INSERT ON ItensVenda
FOR EACH ROW
EXECUTE FUNCTION verificar_e_atualizar_estoque();



-- TRIGGER 2: CALCULAR CUSTOS, DESPESAS E LUCRO REAL A CADA ITEM INSERIDO

CREATE OR REPLACE FUNCTION calcular_financeiro_venda()
RETURNS TRIGGER AS $$
DECLARE
    v_custo_unitario NUMERIC(10,2);
    v_custo_total_item NUMERIC(10,2);
    v_despesa_item NUMERIC(10,2);
    v_receita_item NUMERIC(10,2);
BEGIN
    -- Busca o custo de reposição do produto vendido
    SELECT custo_reposicao INTO v_custo_unitario FROM Produto WHERE id_produto = NEW.id_produto;

    -- Calcula os custos, despesas e receita proporcional deste item (ex: estimando 5% de despesa operacional sobre o preço de venda)
    v_custo_total_item := v_custo_unitario * NEW.quantidade_vendida;
    v_despesa_item := (NEW.preco_unitario * NEW.quantidade_vendida) * 0.05; 
    v_receita_item := NEW.preco_unitario * NEW.quantidade_vendida;

    -- Atualiza os acumulados na tabela Venda
    UPDATE Venda
    SET valor_total = valor_total + v_receita_item,
        valor_reposicao = valor_reposicao + v_custo_total_item,
        valor_despesas = valor_despesas + v_despesa_item,
        valor_lucro = (valor_total + v_receita_item) - (valor_reposicao + v_custo_total_item) - (valor_despesas + v_despesa_item)
    WHERE id_venda = NEW.id_venda;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tg_calculo_financeiro
AFTER INSERT ON ItensVenda
FOR EACH ROW
EXECUTE FUNCTION calcular_financeiro_venda();