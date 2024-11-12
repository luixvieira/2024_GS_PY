import oracledb
import json
import pandas as pd
from datetime import datetime


with open(r'credenciais_banco\credenciais_banco.json', 'r') as credenciais_banco:
    credenciais = json.load(credenciais_banco)
    
    username = credenciais['username']
    password = credenciais['password']
    dsn = credenciais['dsn']
    


# Conexão com o banco de dados
def conectar():
    try:
        # Conexão no modo Thin
        connection = oracledb.connect(user=username, password=password, dsn=dsn)
        return connection
    except oracledb.DatabaseError as e:
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
    except oracledb.DatabaseError as e:
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
    except oracledb.DatabaseError as e:
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
    except oracledb.DatabaseError as e:
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
    except oracledb.DatabaseError as e:
        print("Erro ao excluir usuário:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Função para gerar o relatório de um usuário específico
def gerar_relatorio_usuario():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        # Solicita o ID do usuário
        id_usuario = input("Digite o ID do usuário para o relatório: ")

        # Consulta SQL para obter os dados do usuário
        consulta_usuario = """
        SELECT
            u.id_usuario,
            u.nome AS nome_usuario,
            u.email,
            u.data_criacao
        FROM
            TB_EL_USUARIO u
        WHERE
            u.id_usuario = :id_usuario
        """

        cursor.execute(consulta_usuario, {'id_usuario': id_usuario})
        usuario = cursor.fetchone()

        if not usuario:
            print(f"Usuário com ID {id_usuario} não encontrado.")
            return

        # Consulta SQL para obter as residências do usuário
        consulta_residencias = """
        SELECT
            r.id_residencia,
            r.numero_moradores,
            r.metragem,
            t.regiao AS regiao_tarifa,
            t.preco_kwh
        FROM
            TB_EL_RESIDENCIA r
            LEFT JOIN TB_EL_TARIFA_ENERGIA t ON r.id_tarifa = t.id_tarifa
        WHERE
            r.id_usuario = :id_usuario
        """

        cursor.execute(consulta_residencias, {'id_usuario': id_usuario})
        residencias = cursor.fetchall()

        # Consulta SQL para obter os veículos do usuário
        consulta_veiculos = """
        SELECT
            v.id_veiculo,
            v.tipo_veiculo,
            v.km_mensal,
            v.emissao_co2_por_km
        FROM
            TB_EL_VEICULOS v
        WHERE
            v.id_usuario = :id_usuario
        """

        cursor.execute(consulta_veiculos, {'id_usuario': id_usuario})
        veiculos = cursor.fetchall()

        # Consulta SQL para obter os eletrodomésticos das residências do usuário
        consulta_eletrodomesticos = """
        SELECT
            ue.id_residencia,
            e.id_eletro,
            e.nome AS nome_eletrodomestico,
            e.potencia,
            e.emissao_co2_por_hora,
            e.marca,
            ue.horas_uso_diario
        FROM
            TB_EL_USO_ELETRODOMESTICO ue
            LEFT JOIN TB_EL_ELETRODOMESTICO e ON ue.id_eletro = e.id_eletro
            LEFT JOIN TB_EL_RESIDENCIA r ON ue.id_residencia = r.id_residencia
        WHERE
            r.id_usuario = :id_usuario
        """

        cursor.execute(consulta_eletrodomesticos, {'id_usuario': id_usuario})
        eletrodomesticos = cursor.fetchall()

        # Estrutura de dados para o relatório
        relatorio = {
            'Usuario': {
                'ID': usuario[0],
                'Nome': usuario[1],
                'Email': usuario[2],
                'Data de Criação': usuario[3].strftime('%Y-%m-%d')
            },
            'Residencias': [],
            'Veiculos': [],
            'Eletrodomesticos': []
        }

        # Adiciona as residências ao relatório
        for res in residencias:
            relatorio['Residencias'].append({
                'ID Residencia': res[0],
                'Numero de Moradores': res[1],
                'Metragem': res[2],
                'Regiao Tarifa': res[3],
                'Preco kWh': res[4]
            })

        # Adiciona os veículos ao relatório
        for veic in veiculos:
            relatorio['Veiculos'].append({
                'ID Veiculo': veic[0],
                'Tipo Veiculo': veic[1],
                'KM Mensal': veic[2],
                'Emissao CO2 por KM': veic[3]
            })

        # Adiciona os eletrodomésticos ao relatório
        for eletro in eletrodomesticos:
            relatorio['Eletrodomesticos'].append({
                'ID Residencia': eletro[0],
                'ID Eletrodomestico': eletro[1],
                'Nome Eletrodomestico': eletro[2],
                'Potencia': eletro[3],
                'Emissao CO2 por Hora': eletro[4],
                'Marca': eletro[5],
                'Horas de Uso Diario': eletro[6]
            })

        # Solicita ao usuário o formato de exportação
        while True:
            formato = input("Escolha o formato de exportação (1 para JSON, 2 para Excel): ")
            if formato == "1":
                exportar_json(relatorio, f"relatorio_usuario_{id_usuario}.json")
                break
            elif formato == "2":
                exportar_excel(relatorio, f"relatorio_usuario_{id_usuario}.xlsx")
                break
            else:
                print("Opção inválida. Por favor, escolha 1 para JSON ou 2 para Excel.")

    except oracledb.DatabaseError as e:
        print("Erro ao gerar relatório:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def gerar_relatorio_residencias():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        # Pergunta se deseja consultar as residências de um usuário específico
        opcao_usuario = input("Deseja consultar residências de um usuário específico? (s/n): ").strip().lower()
        if opcao_usuario == 's':
            id_usuario = int(input("Digite o ID do usuário: "))
            consulta = """
                SELECT r.id_residencia, r.numero_moradores, r.metragem, t.regiao AS regiao_tarifa, t.preco_kwh
                FROM TB_EL_RESIDENCIA r
                LEFT JOIN TB_EL_TARIFA_ENERGIA t ON r.id_tarifa = t.id_tarifa
                WHERE r.id_usuario = :id_usuario
            """
            cursor.execute(consulta, {'id_usuario': id_usuario})
        else:
            # Pergunta se deseja consultar uma residência específica
            opcao_residencia = input("Deseja consultar uma residência específica? (s/n): ").strip().lower()
            if opcao_residencia == 's':
                id_residencia = int(input("Digite o ID da residência: "))
                consulta = """
                    SELECT r.id_residencia, r.numero_moradores, r.metragem, t.regiao AS regiao_tarifa, t.preco_kwh
                    FROM TB_EL_RESIDENCIA r
                    LEFT JOIN TB_EL_TARIFA_ENERGIA t ON r.id_tarifa = t.id_tarifa
                    WHERE r.id_residencia = :id_residencia
                """
                cursor.execute(consulta, {'id_residencia': id_residencia})
            else:
                consulta = """
                    SELECT r.id_residencia, r.numero_moradores, r.metragem, t.regiao AS regiao_tarifa, t.preco_kwh
                    FROM TB_EL_RESIDENCIA r
                    LEFT JOIN TB_EL_TARIFA_ENERGIA t ON r.id_tarifa = t.id_tarifa
                """
                cursor.execute(consulta)

        residencias = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        # Exportação dos resultados
        if residencias:
            while True:
                formato = input("Escolha o formato de exportação (1 para JSON, 2 para Excel): ")
                if formato == "1":
                    exportar_json((columns, residencias), "relatorio_residencias.json")
                    break
                elif formato == "2":
                    exportar_excel((columns, residencias), "relatorio_residencias.xlsx")
                    break
                else:
                    print("Opção inválida. Por favor, escolha 1 para JSON ou 2 para Excel.")
        else:
            print("Nenhuma residência encontrada.")
    except oracledb.DatabaseError as e:
        print("Erro ao gerar relatório de residências:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def gerar_relatorio_eletrodomesticos():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        # Pergunta se deseja consultar os eletrodomésticos de uma residência específica
        opcao_residencia = input("Deseja consultar eletrodomésticos de uma residência específica? (s/n): ").strip().lower()
        if opcao_residencia == 's':
            id_residencia = int(input("Digite o ID da residência: "))
            consulta = """
                SELECT e.id_eletro, e.nome, e.potencia, e.emissao_co2_por_hora, e.marca, ue.horas_uso_diario
                FROM TB_EL_ELETRODOMESTICO e
                JOIN TB_EL_USO_ELETRODOMESTICO ue ON e.id_eletro = ue.id_eletro
                WHERE ue.id_residencia = :id_residencia
            """
            cursor.execute(consulta, {'id_residencia': id_residencia})
        else:
            # Pergunta se deseja consultar um eletrodoméstico específico
            opcao_eletro = input("Deseja consultar um eletrodoméstico específico? (s/n): ").strip().lower()
            if opcao_eletro == 's':
                id_eletro = int(input("Digite o ID do eletrodoméstico: "))
                consulta = """
                    SELECT e.id_eletro, e.nome, e.potencia, e.emissao_co2_por_hora, e.marca
                    FROM TB_EL_ELETRODOMESTICO e
                    WHERE e.id_eletro = :id_eletro
                """
                cursor.execute(consulta, {'id_eletro': id_eletro})
            else:
                consulta = """
                    SELECT e.id_eletro, e.nome, e.potencia, e.emissao_co2_por_hora, e.marca
                    FROM TB_EL_ELETRODOMESTICO e
                """
                cursor.execute(consulta)

        eletrodomesticos = cursor.fetchall()
        columns = [col[0] for col in cursor.description]

        # Exportação dos resultados
        if eletrodomesticos:
            while True:
                formato = input("Escolha o formato de exportação (1 para JSON, 2 para Excel): ")
                if formato == "1":
                    exportar_json((columns, eletrodomesticos), "relatorio_eletrodomesticos.json")
                    break
                elif formato == "2":
                    exportar_excel((columns, eletrodomesticos), "relatorio_eletrodomesticos.xlsx")
                    break
                else:
                    print("Opção inválida. Por favor, escolha 1 para JSON ou 2 para Excel.")
        else:
            print("Nenhum eletrodoméstico encontrado.")
    except oracledb.DatabaseError as e:
        print("Erro ao gerar relatório de eletrodomésticos:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Função para exportar dados em formato JSON
def exportar_json(data, filename):
    # Função para exportar dados em JSON, adaptada para diferentes tipos de dados
    def converter(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Tipo {type(obj)} não serializável")
    
    with open(filename, "w", encoding="utf-8") as json_file:
        # Verifica se `data` é uma lista de registros ou um dicionário completo
        if isinstance(data, list):
            json.dump([dict(zip(data[0], row)) for row in data[1]], json_file, indent=4, ensure_ascii=False, default=converter)
        else:
            json.dump(data, json_file, indent=4, ensure_ascii=False, default=converter)
    print(f"Dados exportados para {filename} com sucesso!")

def exportar_excel(data, filename):
    # Função para exportar dados em Excel, adaptada para diferentes tipos de dados
    if isinstance(data, dict):
        # Exportação para relatórios completos (exemplo: dados de usuário com residências e eletrodomésticos)
        with pd.ExcelWriter(filename) as writer:
            if 'Usuario' in data:
                df_usuario = pd.DataFrame([data['Usuario']])
                df_usuario.to_excel(writer, sheet_name='Usuario', index=False)
            if 'Residencias' in data:
                df_residencias = pd.DataFrame(data['Residencias'])
                df_residencias.to_excel(writer, sheet_name='Residencias', index=False)
            if 'Eletrodomesticos' in data:
                df_eletrodomesticos = pd.DataFrame(data['Eletrodomesticos'])
                df_eletrodomesticos.to_excel(writer, sheet_name='Eletrodomesticos', index=False)
    else:
        # Exportação de listas de registros (exemplo: resultado de consultas de residências ou eletrodomésticos)
        columns, rows = data
        df = pd.DataFrame(rows, columns=columns)
        df.to_excel(filename, index=False)

    print(f"Dados exportados para {filename} com sucesso!")




def inserir_tipo_eletrodomestico():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        nome = input("Digite o nome do eletrodoméstico: ")
        potencia = float(input("Digite a potência em watts (W): "))
        emissao_co2_por_hora = float(input("Digite a emissão de CO2 por hora em gramas: "))
        marca = input("Digite a marca do eletrodoméstico: ")

        # Verificar se o eletrodoméstico já existe
        cursor.execute("""
            SELECT ID_ELETRO FROM TB_EL_ELETRODOMESTICO
            WHERE nome = :1 AND marca = :2
        """, (nome, marca))
        resultado = cursor.fetchone()

        if resultado:
            print("Eletrodoméstico já cadastrado.")
        else:
            cursor.execute("""
                INSERT INTO TB_EL_ELETRODOMESTICO (nome, potencia, emissao_co2_por_hora, marca)
                VALUES (:1, :2, :3, :4)
            """, (nome, potencia, emissao_co2_por_hora, marca))
            connection.commit()
            print("Novo tipo de eletrodoméstico inserido com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir tipo de eletrodoméstico:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def consultar_eletrodomesticos():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()
        
        # Pergunta se deseja consultar eletrodomésticos de uma residência específica
        opcao_residencia = input("Deseja consultar eletrodomésticos de uma residência específica? (s/n): ").strip().lower()
        if opcao_residencia == 's':
            id_residencia = int(input("Digite o ID da residência: "))
            consulta = """
                SELECT e.id_eletro, e.nome, e.potencia, e.emissao_co2_por_hora, e.marca, ue.horas_uso_diario
                FROM TB_EL_ELETRODOMESTICO e
                JOIN TB_EL_USO_ELETRODOMESTICO ue ON e.id_eletro = ue.id_eletro
                WHERE ue.id_residencia = :id_residencia
            """
            cursor.execute(consulta, {'id_residencia': id_residencia})
        else:
            consulta = """
                SELECT id_eletro, nome, potencia, emissao_co2_por_hora, marca
                FROM TB_EL_ELETRODOMESTICO
            """
            cursor.execute(consulta)

        eletrodomesticos = cursor.fetchall()
        if eletrodomesticos:
            for eletro in eletrodomesticos:
                print(f"ID Eletrodoméstico: {eletro[0]}, Nome: {eletro[1]}, Potência: {eletro[2]}W, Emissão CO2 por Hora: {eletro[3]}g, Marca: {eletro[4]}")
                if len(eletro) > 5:
                    print(f"Horas de Uso Diário: {eletro[5]}")
        else:
            print("Nenhum eletrodoméstico encontrado.")
    except oracledb.DatabaseError as e:
        print("Erro ao consultar eletrodomésticos:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def atualizar_eletrodomestico():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()
        
        # Solicita o ID do eletrodoméstico a ser atualizado
        id_eletro = int(input("Digite o ID do eletrodoméstico a ser atualizado: "))

        # Verifica se o eletrodoméstico existe
        cursor.execute("SELECT id_eletro FROM TB_EL_ELETRODOMESTICO WHERE id_eletro = :id_eletro", {'id_eletro': id_eletro})
        if not cursor.fetchone():
            print("Eletrodoméstico não encontrado.")
            return

        # Solicita os novos valores
        nome = input("Digite o novo nome do eletrodoméstico: ")
        potencia = float(input("Digite a nova potência em watts (W): "))
        emissao_co2_por_hora = float(input("Digite a nova emissão de CO2 por hora em gramas: "))
        marca = input("Digite a nova marca do eletrodoméstico: ")

        # Atualiza os dados
        cursor.execute("""
            UPDATE TB_EL_ELETRODOMESTICO
            SET nome = :nome,
                potencia = :potencia,
                emissao_co2_por_hora = :emissao_co2_por_hora,
                marca = :marca
            WHERE id_eletro = :id_eletro
        """, {'nome': nome, 'potencia': potencia, 'emissao_co2_por_hora': emissao_co2_por_hora, 'marca': marca, 'id_eletro': id_eletro})

        connection.commit()
        print("Eletrodoméstico atualizado com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao atualizar eletrodoméstico:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def excluir_eletrodomestico():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()
        
        # Solicita o ID do eletrodoméstico a ser excluído
        id_eletro = int(input("Digite o ID do eletrodoméstico a ser excluído: "))

        # Verifica se o eletrodoméstico existe
        cursor.execute("SELECT id_eletro FROM TB_EL_ELETRODOMESTICO WHERE id_eletro = :id_eletro", {'id_eletro': id_eletro})
        if not cursor.fetchone():
            print("Eletrodoméstico não encontrado.")
            return

        # Exclui o eletrodoméstico
        cursor.execute("DELETE FROM TB_EL_ELETRODOMESTICO WHERE id_eletro = :id_eletro", {'id_eletro': id_eletro})
        connection.commit()
        print("Eletrodoméstico excluído com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao excluir eletrodoméstico:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def inserir_veiculo():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        id_usuario = int(input("Digite o ID do usuário proprietário do veículo: "))
        tipo_veiculo = input("Digite o tipo de veículo (Carro, Moto, Caminhonete, Bicicleta Elétrica): ")
        km_mensal = float(input("Digite a quilometragem mensal percorrida: "))
        emissao_co2_por_km = float(input("Digite a emissão de CO2 por km em gramas: "))

        cursor.execute("""
            INSERT INTO TB_EL_VEICULOS (id_usuario, tipo_veiculo, km_mensal, emissao_co2_por_km)
            VALUES (:1, :2, :3, :4)
        """, (id_usuario, tipo_veiculo, km_mensal, emissao_co2_por_km))
        connection.commit()
        print("Veículo inserido com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir veículo:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def inserir_gas():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        id_residencia = int(input("Digite o ID da residência: "))
        tipo_gas = input("Digite o tipo de gás (Botijão, Encanado): ")
        quantidade_mensal = float(input("Digite a quantidade mensal consumida (em litros ou kg): "))
        emissao_co2_por_unidade = float(input("Digite a emissão de CO2 por unidade de gás consumida: "))

        cursor.execute("""
            INSERT INTO TB_EL_GAS (id_residencia, tipo_gas, quantidade_mensal, emissao_co2_por_unidade)
            VALUES (:1, :2, :3, :4)
        """, (id_residencia, tipo_gas, quantidade_mensal, emissao_co2_por_unidade))
        connection.commit()
        print("Registro de consumo de gás inserido com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir registro de gás:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def associar_eletrodomestico_residencia():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        id_residencia = int(input("Digite o ID da residência: "))
        id_eletro = int(input("Digite o ID do eletrodoméstico: "))
        horas_uso_diario = float(input("Digite as horas de uso diário: "))

        # Verificar se a residência e o eletrodoméstico existem
        cursor.execute("SELECT id_residencia FROM TB_EL_RESIDENCIA WHERE id_residencia = :1", (id_residencia,))
        if not cursor.fetchone():
            print("Residência não encontrada.")
            return

        cursor.execute("SELECT ID_ELETRO FROM TB_EL_ELETRODOMESTICO WHERE ID_ELETRO = :1", (id_eletro,))
        if not cursor.fetchone():
            print("Eletrodoméstico não encontrado.")
            return

        # Inserir na tabela de uso de eletrodomésticos
        cursor.execute("""
            INSERT INTO TB_EL_USO_ELETRODOMESTICO (id_residencia, ID_ELETRO, horas_uso_diario)
            VALUES (:1, :2, :3)
        """, (id_residencia, id_eletro, horas_uso_diario))
        connection.commit()
        print("Eletrodoméstico associado à residência com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao associar eletrodoméstico à residência:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def inserir_residencia():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        # Solicita o ID do usuário e verifica se existe
        id_usuario = int(input("Digite o ID do usuário proprietário da residência: "))
        cursor.execute("SELECT id_usuario FROM TB_EL_USUARIO WHERE id_usuario = :1", (id_usuario,))
        if not cursor.fetchone():
            print("Usuário não encontrado. Por favor, insira um ID de usuário válido.")
            return

        # Solicita o ID da tarifa de energia e verifica se existe
        id_tarifa = int(input("Digite o ID da tarifa de energia associada à residência: "))
        cursor.execute("SELECT id_tarifa FROM TB_EL_TARIFA_ENERGIA WHERE id_tarifa = :1", (id_tarifa,))
        if not cursor.fetchone():
            print("Tarifa de energia não encontrada. Por favor, insira um ID de tarifa válido.")
            return

        # Solicita os demais dados da residência
        numero_moradores = int(input("Digite o número de moradores na residência: "))
        metragem = float(input("Digite a metragem da residência em metros quadrados: "))

        # Insere os dados na tabela TB_EL_RESIDENCIA
        cursor.execute("""
            INSERT INTO TB_EL_RESIDENCIA (id_usuario, id_tarifa, numero_moradores, metragem)
            VALUES (:1, :2, :3, :4)
        """, (id_usuario, id_tarifa, numero_moradores, metragem))
        connection.commit()
        print("Residência inserida com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir residência:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def consultar_residencia():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()
        
        # Solicita o ID do usuário para consulta das residências
        opcao_usuario = input("Deseja consultar residências de um usuário específico? (s/n): ").strip().lower()
        if opcao_usuario == 's':
            id_usuario = int(input("Digite o ID do usuário: "))
            consulta = """
                SELECT r.id_residencia, r.numero_moradores, r.metragem, t.regiao, t.preco_kwh
                FROM TB_EL_RESIDENCIA r
                LEFT JOIN TB_EL_TARIFA_ENERGIA t ON r.id_tarifa = t.id_tarifa
                WHERE r.id_usuario = :id_usuario
            """
            cursor.execute(consulta, {'id_usuario': id_usuario})
        else:
            consulta = """
                SELECT r.id_residencia, r.numero_moradores, r.metragem, t.regiao, t.preco_kwh
                FROM TB_EL_RESIDENCIA r
                LEFT JOIN TB_EL_TARIFA_ENERGIA t ON r.id_tarifa = t.id_tarifa
            """
            cursor.execute(consulta)

        residencias = cursor.fetchall()
        if residencias:
            for res in residencias:
                print(f"ID Residência: {res[0]}, Número de Moradores: {res[1]}, Metragem: {res[2]}, Região Tarifa: {res[3]}, Preço kWh: {res[4]}")
        else:
            print("Nenhuma residência encontrada.")
    except oracledb.DatabaseError as e:
        print("Erro ao consultar residências:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def atualizar_residencia():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()
        
        # Solicita o ID da residência a ser atualizada
        id_residencia = int(input("Digite o ID da residência a ser atualizada: "))

        # Verifica se a residência existe
        cursor.execute("SELECT id_residencia FROM TB_EL_RESIDENCIA WHERE id_residencia = :id_residencia", {'id_residencia': id_residencia})
        if not cursor.fetchone():
            print("Residência não encontrada.")
            return

        # Solicita os novos valores
        numero_moradores = int(input("Digite o novo número de moradores: "))
        metragem = float(input("Digite a nova metragem: "))
        id_tarifa = int(input("Digite o novo ID da tarifa de energia: "))

        # Atualiza os dados
        cursor.execute("""
            UPDATE TB_EL_RESIDENCIA
            SET numero_moradores = :numero_moradores,
                metragem = :metragem,
                id_tarifa = :id_tarifa
            WHERE id_residencia = :id_residencia
        """, {'numero_moradores': numero_moradores, 'metragem': metragem, 'id_tarifa': id_tarifa, 'id_residencia': id_residencia})

        connection.commit()
        print("Residência atualizada com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao atualizar residência:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def excluir_residencia():
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()
        
        # Solicita o ID da residência a ser excluída
        id_residencia = int(input("Digite o ID da residência a ser excluída: "))

        # Verifica se a residência existe
        cursor.execute("SELECT id_residencia FROM TB_EL_RESIDENCIA WHERE id_residencia = :id_residencia", {'id_residencia': id_residencia})
        if not cursor.fetchone():
            print("Residência não encontrada.")
            return

        # Exclui a residência
        cursor.execute("DELETE FROM TB_EL_RESIDENCIA WHERE id_residencia = :id_residencia", {'id_residencia': id_residencia})
        connection.commit()
        print("Residência excluída com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao excluir residência:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def inserir_tarifa_energia():
    connection = None
    cursor = None
    try:
        connection = conectar()
        if not connection:
            print("Não foi possível conectar ao banco de dados.")
            return

        cursor = connection.cursor()

        regiao = input("Digite a região da tarifa de energia: ")
        preco_kwh = float(input("Digite o preço por kWh (em R$): "))
        data_validade = input("Digite a data de validade da tarifa (YYYY-MM-DD) ou deixe em branco para indefinida: ")

        # Verificar se a região já possui uma tarifa cadastrada
        cursor.execute("SELECT id_tarifa FROM TB_EL_TARIFA_ENERGIA WHERE regiao = :1", (regiao,))
        if cursor.fetchone():
            print("Já existe uma tarifa cadastrada para essa região.")
            return

        # Inserir a nova tarifa na tabela
        if data_validade:
            cursor.execute("""
                INSERT INTO TB_EL_TARIFA_ENERGIA (regiao, preco_kwh, data_validade)
                VALUES (:1, :2, TO_DATE(:3, 'YYYY-MM-DD'))
            """, (regiao, preco_kwh, data_validade))
        else:
            cursor.execute("""
                INSERT INTO TB_EL_TARIFA_ENERGIA (regiao, preco_kwh)
                VALUES (:1, :2)
            """, (regiao, preco_kwh))

        connection.commit()
        print("Tarifa de energia inserida com sucesso!")
    except oracledb.DatabaseError as e:
        print("Erro ao inserir tarifa de energia:", e)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

