import cx_Oracle
import json
import pandas as pd

# Configuração da URL de conexão
username = "RM558935"
password = "310805"
dsn = "oracle.fiap.com.br/ORCL"

# Conexão com o banco de dados
def conectar():
    try:
        cx_Oracle.init_oracle_client(lib_dir=r"C:\oracle\instantclient_23_5")
        connection = cx_Oracle.connect(username, password, dsn)

        return connection
    except cx_Oracle.DatabaseError as e:
        print("Erro ao conectar no banco de dados:", e)
        return None

# Funções CRUD
def inserir_usuario():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return  # Encerra a função se a conexão falhar

        cursor = connection.cursor()
        
        nome = input("Digite o nome do usuário: ")
        email = input("Digite o email do usuário: ")

        cursor.execute("INSERT INTO TB_EL_USUARIO (nome, email) VALUES (:1, :2)", (nome, email))
        connection.commit()
        print("Usuário inserido com sucesso!")
    except cx_Oracle.DatabaseError as e:
        print("Erro ao inserir usuário:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def consultar_usuarios():
    try:
        connection = conectar()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM TB_EL_USUARIO")
        for row in cursor:
            print(row)
    except cx_Oracle.DatabaseError as e:
        print("Erro ao consultar usuários:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def atualizar_usuario():
    try:
        connection = conectar()
        cursor = connection.cursor()
        
        usuario_id = int(input("Digite o ID do usuário a ser atualizado: "))
        novo_email = input("Digite o novo email do usuário: ")

        cursor.execute("UPDATE TB_EL_USUARIO SET email = :1 WHERE id_usuario = :2", (novo_email, usuario_id))
        connection.commit()
        print("Usuário atualizado com sucesso!")
    except cx_Oracle.DatabaseError as e:
        print("Erro ao atualizar usuário:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def excluir_usuario():
    try:
        connection = conectar()
        cursor = connection.cursor()
        
        usuario_id = int(input("Digite o ID do usuário a ser excluído: "))

        cursor.execute("DELETE FROM TB_EL_USUARIO WHERE id_usuario = :1", (usuario_id,))
        connection.commit()
        print("Usuário excluído com sucesso!")
    except cx_Oracle.DatabaseError as e:
        print("Erro ao excluir usuário:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Funções de Relatório e Exportação
def gerar_relatorio():
    try:
        connection = conectar()
        cursor = connection.cursor()

        consulta = """
        SELECT nome, email, data_criacao FROM TB_EL_USUARIO
        WHERE data_criacao > TO_DATE(:1, 'YYYY-MM-DD')
        """
        data = input("Digite a data mínima para o relatório (YYYY-MM-DD): ")
        cursor.execute(consulta, (data,))
        
        # Fetching results
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

        # Exportar para JSON
        exportar_json(columns, rows, "relatorio_usuarios.json")

        # Exportar para Excel
        exportar_excel(columns, rows, "relatorio_usuarios.xlsx")

    except cx_Oracle.DatabaseError as e:
        print("Erro ao gerar relatório:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def exportar_json(columns, rows, filename):
    data = [dict(zip(columns, row)) for row in rows]
    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Dados exportados para {filename} com sucesso!")

def exportar_excel(columns, rows, filename):
    df = pd.DataFrame(rows, columns=columns)
    df.to_excel(filename, index=False)
    print(f"Dados exportados para {filename} com sucesso!")

# Menu do Sistema
def menu():
    while True:
        print("\nMenu do Sistema")
        print("1. Inserir Usuário")
        print("2. Consultar Usuários")
        print("3. Atualizar Usuário")
        print("4. Excluir Usuário")
        print("5. Gerar Relatório de Usuários")
        print("6. Sair")

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
            gerar_relatorio()
        elif opcao == "6":
            print("Saindo do sistema.")
            break
        else:
            print("Opção inválida. Tente novamente.")

# Executar o Menu
if __name__ == "__main__":
    menu()
