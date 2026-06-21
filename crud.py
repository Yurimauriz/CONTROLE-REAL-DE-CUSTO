import database
import psycopg2

# ==========================================
# CRUD - USUÁRIO
# ==========================================

def criar_usuario(nome, login, senha, perfil_acesso):
    """
    Cria um novo usuário no banco de dados.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO Usuario (nome, login, senha, perfil_acesso)
                VALUES (%s, %s, %s, %s)
                RETURNING id_usuario;
            """
            cursor.execute(query, (nome, login, senha, perfil_acesso))
            id_usuario = cursor.fetchone()[0]
            conn.commit()
            return id_usuario
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise Exception(f"Erro ao criar usuário: {e}")
    finally:
        conn.close()

def listar_usuarios():
    """
    Retorna todos os usuários cadastrados.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id_usuario, nome, login, perfil_acesso 
                FROM Usuario 
                ORDER BY id_usuario;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            usuarios = []
            for row in rows:
                usuarios.append({
                    "id_usuario": row[0],
                    "nome": row[1],
                    "login": row[2],
                    "perfil_acesso": row[3]
                })
            return usuarios
    except psycopg2.DatabaseError as e:
        raise Exception(f"Erro ao listar usuários: {e}")
    finally:
        conn.close()

def buscar_usuario_por_id(id_usuario):
    """
    Busca um usuário pelo ID.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id_usuario, nome, login, perfil_acesso 
                FROM Usuario 
                WHERE id_usuario = %s;
            """
            cursor.execute(query, (id_usuario,))
            row = cursor.fetchone()
            if row:
                return {
                    "id_usuario": row[0],
                    "nome": row[1],
                    "login": row[2],
                    "perfil_acesso": row[3]
                }
            return None
    except psycopg2.DatabaseError as e:
        raise Exception(f"Erro ao buscar usuário: {e}")
    finally:
        conn.close()

def atualizar_usuario(id_usuario, nome, login, senha, perfil_acesso):
    """
    Atualiza as informações de um usuário existente.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                UPDATE Usuario 
                SET nome = %s, login = %s, senha = %s, perfil_acesso = %s 
                WHERE id_usuario = %s;
            """
            cursor.execute(query, (nome, login, senha, perfil_acesso, id_usuario))
            conn.commit()
            return cursor.rowcount > 0
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise Exception(f"Erro ao atualizar usuário: {e}")
    finally:
        conn.close()

def deletar_usuario(id_usuario):
    """
    Exclui um usuário pelo ID.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM Usuario WHERE id_usuario = %s;"
            cursor.execute(query, (id_usuario,))
            conn.commit()
            return cursor.rowcount > 0
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise Exception(f"Erro ao deletar usuário: {e}")
    finally:
        conn.close()


# ==========================================
# CRUD - PRODUTO
# ==========================================

def criar_produto(nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario):
    """
    Cria um novo produto no banco de dados.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                INSERT INTO Produto (nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id_produto;
            """
            cursor.execute(query, (nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario))
            id_produto = cursor.fetchone()[0]
            conn.commit()
            return id_produto
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise Exception(f"Erro ao criar produto: {e}")
    finally:
        conn.close()

def listar_produtos():
    """
    Retorna todos os produtos cadastrados.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id_produto, nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario 
                FROM Produto 
                ORDER BY id_produto;
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            produtos = []
            for row in rows:
                produtos.append({
                    "id_produto": row[0],
                    "nome_produto": row[1],
                    "marca": row[2],
                    "quantidade_estoque": row[3],
                    "custo_reposicao": row[4],
                    "preco_venda": row[5],
                    "id_usuario": row[6]
                })
            return produtos
    except psycopg2.DatabaseError as e:
        raise Exception(f"Erro ao listar produtos: {e}")
    finally:
        conn.close()

def buscar_produto_por_id(id_produto):
    """
    Busca um produto pelo ID.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                SELECT id_produto, nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario 
                FROM Produto 
                WHERE id_produto = %s;
            """
            cursor.execute(query, (id_produto,))
            row = cursor.fetchone()
            if row:
                return {
                    "id_produto": row[0],
                    "nome_produto": row[1],
                    "marca": row[2],
                    "quantidade_estoque": row[3],
                    "custo_reposicao": row[4],
                    "preco_venda": row[5],
                    "id_usuario": row[6]
                }
            return None
    except psycopg2.DatabaseError as e:
        raise Exception(f"Erro ao buscar produto: {e}")
    finally:
        conn.close()

def atualizar_produto(id_produto, nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario):
    """
    Atualiza as informações de um produto existente.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = """
                UPDATE Produto 
                SET nome_produto = %s, marca = %s, quantidade_estoque = %s, custo_reposicao = %s, preco_venda = %s, id_usuario = %s 
                WHERE id_produto = %s;
            """
            cursor.execute(query, (nome_produto, marca, quantidade_estoque, custo_reposicao, preco_venda, id_usuario, id_produto))
            conn.commit()
            return cursor.rowcount > 0
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise Exception(f"Erro ao atualizar produto: {e}")
    finally:
        conn.close()

def deletar_produto(id_produto):
    """
    Exclui um produto pelo ID.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM Produto WHERE id_produto = %s;"
            cursor.execute(query, (id_produto,))
            conn.commit()
            return cursor.rowcount > 0
    except psycopg2.DatabaseError as e:
        conn.rollback()
        raise Exception(f"Erro ao deletar produto: {e}")
    finally:
        conn.close()


# ==========================================
# INTEGRAÇÃO DE COMPRA/VENDA E DASHBOARD
# ==========================================

def efetuar_venda(id_usuario, produtos, quantidades):
    """
    Chama a Procedure 'registrar_venda' usando uma conexão em modo autocommit.
    Garante o correto rollback ou commit gerenciado no banco de dados.
    """
    conn = database.obter_conexao_autocommit()
    try:
        with conn.cursor() as cursor:
            # PostgreSQL Procedure Call via 'CALL' com arrays
            cursor.execute("CALL registrar_venda(%s, %s, %s);", (id_usuario, produtos, quantidades))
            return True
    except psycopg2.DatabaseError as e:
        # Repassa a exceção com a mensagem vinda das Triggers/Exceptions do PostgreSQL
        raise Exception(e)
    finally:
        conn.close()

def buscar_relatorio_financeiro():
    """
    Chama a Function 'obter_relatorio_financeiro' do banco.
    """
    conn = database.obter_conexao()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT total_receita, total_reposicao, total_lucro_liquido FROM obter_relatorio_financeiro();")
            row = cursor.fetchone()
            if row:
                return {
                    "total_receita": row[0],
                    "total_reposicao": row[1],
                    "total_lucro_liquido": row[2]
                }
            return {
                "total_receita": 0.00,
                "total_reposicao": 0.00,
                "total_lucro_liquido": 0.00
            }
    except psycopg2.DatabaseError as e:
        raise Exception(f"Erro ao carregar relatório financeiro: {e}")
    finally:
        conn.close()
