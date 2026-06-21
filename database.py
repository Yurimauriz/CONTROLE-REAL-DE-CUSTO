import os
import psycopg2
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def obter_conexao():
    """
    Retorna uma conexão padrão com o banco de dados PostgreSQL.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "postgres"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres")
        )
        return conn
    except Exception as e:
        err_str = repr(e)
        raise Exception(f"Erro de conexão com o banco de dados PostgreSQL. Verifique se o servidor está ativo e se as credenciais no arquivo .env estão corretas. Detalhes: {err_str}")

def obter_conexao_autocommit():
    """
    Retorna uma conexão com autocommit ativado.
    Necessário para executar Procedures que gerenciam internamente COMMIT e ROLLBACK,
    como a procedure 'registrar_venda'.
    """
    conn = obter_conexao()
    conn.autocommit = True
    return conn
