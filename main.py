import sys
import crud

def exibir_titulo(texto):
    print("\n" + "="*50)
    print(f" {texto.upper().center(48)} ")
    print("="*50)

def exibir_menu_principal():
    exibir_titulo("Controle Real de Custo")
    print(" [1] Registrar Nova Venda")
    print(" [2] Visualizar Relatório Financeiro (Dashboard)")
    print(" [3] Gerenciar Usuários (CRUD)")
    print(" [4] Gerenciar Produtos (CRUD)")
    print(" [0] Sair do Sistema")
    print("="*50)

# ==========================================
# GESTÃO DE USUÁRIOS
# ==========================================
def menu_usuarios():
    while True:
        exibir_titulo("Gerenciar Usuários")
        print(" [1] Cadastrar Usuário")
        print(" [2] Listar Usuários")
        print(" [3] Atualizar Usuário")
        print(" [4] Excluir Usuário")
        print(" [0] Voltar ao Menu Principal")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_usuario_ui()
        elif opcao == "2":
            listar_usuarios_ui()
        elif opcao == "3":
            atualizar_usuario_ui()
        elif opcao == "4":
            excluir_usuario_ui()
        elif opcao == "0":
            break
        else:
            print("\n Opção inválida! Tente novamente.")

def cadastrar_usuario_ui():
    print("\n--- CADASTRAR USUÁRIO ---")
    nome = input("Nome Completo: ").strip()
    login = input("Login (Único): ").strip()
    senha = input("Senha: ").strip()
    
    while True:
        perfil = input("Perfil de Acesso (Gerente/Balcão): ").strip()
        if perfil in ['Gerente', 'Balcão']:
            break
        print("ERRO: Perfil inválido! Escolha entre 'Gerente' ou 'Balcão'.")
        
    if not nome or not login or not senha:
        print("ERRO: Todos os campos são obrigatórios!")
        return
        
    try:
        id_usuario = crud.criar_usuario(nome, login, senha, perfil)
        print(f"\n Usuário cadastrado com sucesso! ID: {id_usuario}")
    except Exception as e:
        print(f"\n ERRO ao cadastrar usuário: {e}")

def listar_usuarios_ui():
    print("\n--- LISTA DE USUÁRIOS ---")
    try:
        usuarios = crud.listar_usuarios()
        if not usuarios:
            print("Nenhum usuário cadastrado.")
            return
            
        print(f"{'ID':<5} | {'Nome':<25} | {'Login':<15} | {'Perfil':<10}")
        print("-" * 65)
        for u in usuarios:
            print(f"{u['id_usuario']:<5} | {u['nome']:<25} | {u['login']:<15} | {u['perfil_acesso']:<10}")
    except Exception as e:
        print(f"\n ERRO ao listar usuários: {e}")

def atualizar_usuario_ui():
    print("\n--- ATUALIZAR USUÁRIO ---")
    try:
        id_usuario = int(input("Digite o ID do Usuário a ser atualizado: "))
        u = crud.buscar_usuario_por_id(id_usuario)
        if not u:
            print("Usuário não encontrado.")
            return
            
        print(f"Editando usuário: {u['nome']} ({u['perfil_acesso']})")
        nome = input(f"Novo Nome [{u['nome']}]: ").strip() or u['nome']
        login = input(f"Novo Login [{u['login']}]: ").strip() or u['login']
        senha = input("Digite a Nova Senha (ou repita a atual): ").strip()
        if not senha:
            print("ERRO: A senha não pode ser vazia!")
            return
            
        while True:
            perfil = input(f"Novo Perfil (Gerente/Balcão) [{u['perfil_acesso']}]: ").strip() or u['perfil_acesso']
            if perfil in ['Gerente', 'Balcão']:
                break
            print("ERRO: Perfil inválido! Escolha entre 'Gerente' ou 'Balcão'.")
            
        sucesso = crud.atualizar_usuario(id_usuario, nome, login, senha, perfil)
        if sucesso:
            print("\n Usuário atualizado com sucesso!")
        else:
            print("\n Não foi possível atualizar o usuário.")
    except ValueError:
        print("ERRO: ID inválido!")
    except Exception as e:
        print(f"\n ERRO ao atualizar usuário: {e}")

def excluir_usuario_ui():
    print("\n--- EXCLUIR USUÁRIO ---")
    try:
        id_usuario = int(input("Digite o ID do Usuário a ser excluído: "))
        confirmar = input(f"Tem certeza que deseja excluir o usuário ID {id_usuario}? (S/N): ").strip().upper()
        if confirmar == 'S':
            sucesso = crud.deletar_usuario(id_usuario)
            if sucesso:
                print("\n Usuário excluído com sucesso!")
            else:
                print("\n Usuário não encontrado ou não pôde ser excluído.")
        else:
            print("\nOperação cancelada.")
    except ValueError:
        print("ERRO: ID inválido!")
    except Exception as e:
        print(f"\n ERRO ao excluir usuário: {e}")

# ==========================================
# GESTÃO DE PRODUTOS
# ==========================================
def menu_produtos():
    while True:
        exibir_titulo("Gerenciar Produtos")
        print(" [1] Cadastrar Produto")
        print(" [2] Listar Produtos")
        print(" [3] Atualizar Produto")
        print(" [4] Excluir Produto")
        print(" [0] Voltar ao Menu Principal")
        print("="*50)
        
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "1":
            cadastrar_produto_ui()
        elif opcao == "2":
            listar_produtos_ui()
        elif opcao == "3":
            atualizar_produto_ui()
        elif opcao == "4":
            excluir_produto_ui()
        elif opcao == "0":
            break
        else:
            print("\n Opção inválida! Tente novamente.")

def cadastrar_produto_ui():
    print("\n--- CADASTRAR PRODUTO ---")
    try:
        nome_produto = input("Nome do Produto: ").strip()
        marca = input("Marca: ").strip()
        qtd_estoque = int(input("Quantidade em Estoque: "))
        custo_reposicao = float(input("Custo de Reposição (R$): "))
        preco_venda = float(input("Preço de Venda (R$): "))
        id_usuario = int(input("ID do Usuário Cadastrador (Responsável): "))
        
        if not nome_produto:
            print("ERRO: O nome do produto é obrigatório!")
            return
            
        id_produto = crud.criar_produto(nome_produto, marca, qtd_estoque, custo_reposicao, preco_venda, id_usuario)
        print(f"\n Produto cadastrado com sucesso! ID: {id_produto}")
    except ValueError:
        print("ERRO: Entrada numérica inválida para estoque, custo, preço ou ID de usuário.")
    except Exception as e:
        print(f"\n ERRO ao cadastrar produto: {e}")

def listar_produtos_ui():
    print("\n--- LISTA DE PRODUTOS ---")
    try:
        produtos = crud.listar_produtos()
        if not produtos:
            print("Nenhum produto cadastrado.")
            return
            
        print(f"{'ID':<5} | {'Produto':<20} | {'Marca':<12} | {'Qtd':<5} | {'Custo':<10} | {'Preço':<10} | {'Responsavel':<8}")
        print("-" * 75)
        for p in produtos:
            print(f"{p['id_produto']:<5} | {p['nome_produto']:<20} | {p['marca']:<12} | {p['quantidade_estoque']:<5} | R$ {p['custo_reposicao']:<7.2f} | R$ {p['preco_venda']:<7.2f} | {p['id_usuario']:<8}")
    except Exception as e:
        print(f"\n ERRO ao listar produtos: {e}")

def atualizar_produto_ui():
    print("\n--- ATUALIZAR PRODUTO ---")
    try:
        id_produto = int(input("Digite o ID do Produto a ser atualizado: "))
        p = crud.buscar_produto_por_id(id_produto)
        if not p:
            print("Produto não encontrado.")
            return
            
        print(f"Editando produto: {p['nome_produto']}")
        nome_produto = input(f"Novo Nome [{p['nome_produto']}]: ").strip() or p['nome_produto']
        marca = input(f"Nova Marca [{p['marca']}]: ").strip() or p['marca']
        qtd_estoque = input(f"Nova Qtd Estoque [{p['quantidade_estoque']}]: ").strip()
        qtd_estoque = int(qtd_estoque) if qtd_estoque else p['quantidade_estoque']
        
        custo_reposicao = input(f"Novo Custo Reposição [R$ {p['custo_reposicao']:.2f}]: ").strip()
        custo_reposicao = float(custo_reposicao) if custo_reposicao else p['custo_reposicao']
        
        preco_venda = input(f"Novo Preço Venda [R$ {p['preco_venda']:.2f}]: ").strip()
        preco_venda = float(preco_venda) if preco_venda else p['preco_venda']
        
        id_usuario = input(f"Novo ID Responsável [{p['id_usuario']}]: ").strip()
        id_usuario = int(id_usuario) if id_usuario else p['id_usuario']
        
        sucesso = crud.atualizar_produto(id_produto, nome_produto, marca, qtd_estoque, custo_reposicao, preco_venda, id_usuario)
        if sucesso:
            print("\n Produto atualizado com sucesso!")
        else:
            print("\n Não foi possível atualizar o produto.")
    except ValueError:
        print("ERRO: Entrada inválida!")
    except Exception as e:
        print(f"\n ERRO ao atualizar produto: {e}")

def excluir_produto_ui():
    print("\n--- EXCLUIR PRODUTO ---")
    try:
        id_produto = int(input("Digite o ID do Produto a ser excluído: "))
        confirmar = input(f"Tem certeza que deseja excluir o produto ID {id_produto}? (S/N): ").strip().upper()
        if confirmar == 'S':
            sucesso = crud.deletar_produto(id_produto)
            if sucesso:
                print("\n Produto excluído com sucesso!")
            else:
                print("\n Produto não encontrado ou não pôde ser excluído.")
        else:
            print("\nOperação cancelada.")
    except ValueError:
        print("ERRO: ID inválido!")
    except Exception as e:
        print(f"\n ERRO ao excluir produto: {e}")

# ==========================================
# PROCESSAMENTO DE VENDAS E DASHBOARD
# ==========================================
def interacao_registrar_venda():
    print("\n--- REGISTRAR VENDA ---")
    try:
        id_usuario = int(input("Digite o ID do Usuário (Vendedor): "))
        
        # Validar se o usuário existe
        u = crud.buscar_usuario_por_id(id_usuario)
        if not u:
            print("ERRO: Usuário não cadastrado! Cadastre o usuário antes de efetuar a venda.")
            return

        produtos = []
        quantidades = []
        
        while True:
            id_prod = int(input("Digite o ID do Produto: "))
            
            # Validar se o produto existe
            p = crud.buscar_produto_por_id(id_prod)
            if not p:
                print("ERRO: Produto não encontrado!")
                continue
                
            qtd = int(input(f"Digite a Quantidade (Disponível: {p['quantidade_estoque']}): "))
            if qtd <= 0:
                print("ERRO: A quantidade deve ser maior que zero!")
                continue

            produtos.append(id_prod)
            quantidades.append(qtd)
            
            continuar = input("Deseja adicionar mais um produto? (S/N): ").strip().upper()
            if continuar != 'S':
                break
        
        print("\nProcessando transação no banco de dados...")
        
        sucesso = crud.efetuar_venda(id_usuario, produtos, quantidades)
        if sucesso:
            print("\n" + "*"*40)
            print(" VENDA REALIZADA COM SUCESSO!")
            print(" Estoque atualizado e indicadores financeiros gerados.")
            print("*"*40)
            
    except ValueError:
        print("ERRO: Entrada inválida! Certifique-se de digitar números para IDs e Quantidades.")
    except Exception as e:
        # Pega a mensagem exata disparada pela Trigger ('Estoque insuficiente...')
        print("\n" + "!"*40)
        print(" TRANSAÇÃO ABORTADA PELO BANCO DE DADOS!")
        print(f"Motivo: {e}")
        print("Todos os dados desta operação foram desfeitos (ROLLBACK).")
        print("!"*40)

def exibir_dashboard():
    print("\n--- DASHBOARD FINANCEIRO ---")
    try:
        relatorio = crud.buscar_relatorio_financeiro()
        if relatorio:
            print(f"Faturamento Total: R$ {relatorio['total_receita']:.2f}")
            print(f"Custos de Reposição: R$ {relatorio['total_reposicao']:.2f}")
            print(f"Lucro Líquido Acumulado: R$ {relatorio['total_lucro_liquido']:.2f}")
        else:
            print("Nenhum dado financeiro encontrado.")
    except Exception as e:
        print(f"Erro ao carregar dashboard: {e}")

# ==========================================
# EXECUÇÃO PRINCIPAL
# ==========================================
def main():
    while True:
        exibir_menu_principal()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            interacao_registrar_venda()
        elif opcao == "2":
            exibir_dashboard()
        elif opcao == "3":
            menu_usuarios()
        elif opcao == "4":
            menu_produtos()
        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!")
            sys.exit()
        else:
            print("\n Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()
