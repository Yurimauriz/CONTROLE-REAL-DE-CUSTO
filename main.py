import sys
import crud  

def exibir_menu():
    print("\n" + "="*40)
    print("      SISTEMA CONTROLE REAL DE CUSTO      ")
    print("="*40)
    print("[1] Registrar Nova Venda")
    print("[2] Visualizar Relatório Financeiro")
    print("[0] Sair do Sistema")
    print("="*40)

def interacao_registrar_venda():
    print("\n--- REGISTRAR VENDA ---")
    
    try:
        id_usuario = int(input("Digite o ID do Usuário (Vendedor): "))
        
        produtos = []
        quantidades = []
        
        # Loop para permitir adicionar vários produtos em uma única venda/transação
        while True:
            id_prod = int(input("Digite o ID do Produto: "))
            qtd = int(input("Digite a Quantidade: "))
            
            produtos.append(id_prod)
            quantidades.append(qtd)
            
            continuar = input("Deseja adicionar mais um produto? (S/N): ").strip().upper()
            if continuar != 'S':
                break
        
        print("\nProcessando transação no banco de dados...")
        
       
        sucesso = crud.efetuar_venda(id_usuario, produtos, quantidades)
        
        if sucesso:
            print(" VENDA REALIZADA COM SUCESSO!")
            print("Estoque atualizado e indicadores financeiros gerados.")
            
    except ValueError:
        print("ERRO: Entrada inválida! Certifique-se de digitar números para IDs e Quantidades.")
    except Exception as e:
        # Pega a mensagem exata disparada pela Trigger ('Estoque insuficiente...')
        print("\n" + "!"*40)
        print(" TRANSACÃO ABORTADA PELO BANCO DE DADOS!")
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

def main():
    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            interacao_registrar_venda()
        elif opcao == "2":
            exibir_dashboard()
        elif opcao == "0":
            print("\nEncerrando o sistema... Até logo!")
            sys.exit()
        else:
            print("\n Opção inválida! Tente novamente.")

if __name__ == "__main__":
    main()