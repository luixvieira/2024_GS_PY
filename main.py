import funcoes

def menu_principal():
    while True:
        print("\nMenu Principal")
        print("1. Gerenciamento de Usuários")
        print("2. Gerenciamento de Residências")
        print("3. Gerenciamento de Eletrodomésticos")
        print("4. Exportar Relatórios")
        print("5. Sair do Programa")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            menu_gerenciamento_usuarios()
        elif opcao == "2":
            menu_gerenciamento_residencias()
        elif opcao == "3":
            menu_gerenciamento_eletrodomesticos()
        elif opcao == "4":
            menu_exportar_relatorios()
        elif opcao == "5":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_gerenciamento_usuarios():
    while True:
        print("\nGerenciamento de Usuários")
        print("1. Inserir Usuário")
        print("2. Consultar Usuários")
        print("3. Atualizar Usuário")
        print("4. Excluir Usuário")
        print("5. Inserir veiculo")
        print("6. Inserir gás")
        print("7. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            inserir_usuario()
        elif opcao == "2":
            consultar_usuarios()
        elif opcao == "3":
            atualizar_usuario()
        elif opcao == "4":
            excluir_usuario()
        elif opcao == "5":
            inserir_veiculo()
        elif opcao == "6":
            inserir_gas()
        elif opcao == "7":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_gerenciamento_residencias():
    while True:
        print("\nGerenciamento de Residências")
        print("1. Inserir Residência")
        print("2. Consultar Residências")
        print("3. Atualizar Residência")
        print("4. Excluir Residência")
        print("5. Inserir Tarifa de energia")
        print("6. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            inserir_residencia()
        elif opcao == "2":
            consultar_residencia()
        elif opcao == "3":
            atualizar_residencia()
        elif opcao == "4":
            excluir_residencia()
        elif opcao == "5":
            inserir_tarifa_energia()
        elif opcao == "6":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_gerenciamento_eletrodomesticos():
    while True:
        print("\nGerenciamento de Eletrodomésticos")
        print("1. Inserir Novo Tipo de Eletrodoméstico")
        print("2. Associar Eletrodoméstico a Residência")
        print("3. Consultar Eletrodomésticos")
        print("4. Atualizar Eletrodoméstico")
        print("5. Excluir Eletrodoméstico")
        print("6. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            inserir_tipo_eletrodomestico()
        elif opcao == "2":
            associar_eletrodomestico_residencia()
        elif opcao == "3":
            consultar_eletrodomesticos()
        elif opcao == "4":
            atualizar_eletrodomestico()
        elif opcao == "5":
            excluir_eletrodomestico()
        elif opcao == "6":
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_exportar_relatorios():
    while True:
        print("\nExportar Relatórios")
        print("1. Gerar Relatório de Usuários")
        print("2. Gerar Relatório de Residências")
        print("3. Gerar Relatório de Eletrodomésticos")
        print("4. Voltar ao Menu Principal")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            gerar_relatorio_usuario()
        elif opcao == "2":
            gerar_relatorio_residencias()
        elif opcao == "3":
            gerar_relatorio_eletrodomesticos()
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executar o Menu Principal
if __name__ == "__main__":
    menu_principal()
