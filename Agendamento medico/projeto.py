from datetime import datetime
import mysql.connector

# Conexão com banco
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="25140377",
        database="projeto_final"
    )
    cursor = conn.cursor()
    print(" Conexão com banco de dados OK!")
except Exception as e:
    print(f" Erro ao conectar ao banco de dados: {e}")
    exit()

# Variáveis globais
usuario_logado = {}

def login():
    global usuario_logado
    while True:
        email = input("Digite seu email (ou 0 para voltar): ")
        if email == "0":
            return False
        
        senha = input("Digite sua senha: ")
        sql = "SELECT id_usuario, nome_usuario, email_usuario, data_nascimento FROM tbl_usuario WHERE email_usuario = %s AND senha_usuario = %s"
        cursor.execute(sql, (email, senha))
        resultado = cursor.fetchone()
        if resultado:
            usuario_logado = {
                "id": resultado[0],
                "nome": resultado[1],
                "email": resultado[2],
                "data_nasc": resultado[3]
            }
            print(f" Bem-vindo, {usuario_logado['nome']}!")
            return True
        else:
            print("Email ou senha incorretos. Tente novamente.")

def cadastro():
    try:
        nome = input("Digite seu nome: ")
        email = input("Digite seu email: ")
        senha = input("Digite uma senha: ")
        data_nasc_str = input("Digite sua data de nascimento (DD/MM/AAAA): ")
        data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y")
        sql = "INSERT INTO tbl_usuario (nome_usuario, email_usuario, senha_usuario, data_nascimento) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (nome, email, senha, data_nasc))
        conn.commit()
        print(" Cadastro realizado com sucesso!")
    except ValueError:
        print(" Data em formato inválido! Use DD/MM/AAAA.")
    except Exception as e:
        print(f" Erro ao cadastrar usuário: {e}")

def agendar():
    try:
        data_str = input("Digite a data do agendamento (DD/MM/AAAA): ")
        hora = input("Digite o horário do agendamento (HH:MM): ")
        descricao = input("Digite uma breve descrição do que você tem: ")

        data_agendamento = datetime.strptime(data_str, "%d/%m/%Y")
        hora_obj = datetime.strptime(hora, "%H:%M").time()

        sql = """
            INSERT INTO tbl_agendamento1 
            (id_usuario, data_hora, horas_agen, descricao_agen)
            VALUES (%s, %s, %s, %s)
        """
        valores = (
            usuario_logado['id'],
            data_agendamento,
            hora_obj,
            descricao
        )
        cursor.execute(sql, valores)
        conn.commit()
        print("Agendamento realizado com sucesso!")
    except ValueError:
        print(" Data ou hora em formato inválido!")
    except Exception as e:
        print(f"Erro ao agendar: {e}")

def lista():
    try:
        sql = """
            SELECT a.id_agen, u.nome_usuario, u.cpf_usuario, u.data_nascimento, 
                   a.data_hora, a.horas_agen, a.descricao_agen
            FROM tbl_agendamento1 a
            JOIN tbl_usuario u ON a.id_usuario = u.id_usuario
            WHERE a.id_usuario = %s
        """
        cursor.execute(sql, (usuario_logado['id'],))
        resultados = cursor.fetchall()

        if not resultados:
            print(" Nenhum agendamento encontrado.")
            return

        for linha in resultados:
            print(f"""
📝 ID: {linha[0]}
👤 Nome: {linha[1]}
🆔 CPF: {linha[2]}
🎂 Nascimento: {linha[3].strftime('%d/%m/%Y')}
📅 Data: {linha[4].strftime('%d/%m/%Y')}
🕒 Hora: {linha[5]}
📄 Descrição: {linha[6]}
----------------------------------
            """)
    except Exception as e:
        print(f" Erro ao listar agendamentos: {e}")

def excluir():
    try:
        ex = int(input("Digite o ID do agendamento que deseja excluir: "))
        cursor.execute("DELETE FROM tbl_agendamento1 WHERE id_agen = %s", (ex,))
        conn.commit()
        if cursor.rowcount > 0:
            print(" Agendamento excluído com sucesso!")
        else:
            print(" ID não encontrado.")
    except Exception as e:
        print(f" Erro ao excluir agendamento: {e}")

def menu_usuario():
    while True:
        print("\n---- Menu do Usuário ----")
        print("1 - Agendar")
        print("2 - Listar Agendamentos")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            agendar()
        elif opcao == "2":
            lista()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def medico():
    try:
        nome_med = input("Digite seu nome: ")
        cargo = input("Digite seu cargo: ")
        crm = input("Digite seu CRM: ")

        sql = "INSERT INTO tbl_medico(nome_medico, cargo_medico, crm_medico) VALUES (%s, %s, %s)"   
        cursor.execute(sql, (nome_med, cargo, crm))
        conn.commit()
        print(" Cadastro de médico realizado com sucesso!")
    except Exception as e:
        print(f" Erro ao cadastrar médico: {e}")

def menu_med():
    while True:
        print("\n---- Menu do Médico ----")
        print("1 - Listar Agendamentos")
        print("2 - Excluir Agendamento")
        print("0 - Voltar")
        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            lista()
        elif opcao == "2":
            excluir()
        elif opcao == "0":
            break
        else:
            print("Opção inválida!")

def usuario():
    while True:
        print("\nVocê é médico ou paciente?")
        print("1 - Médico")
        print("2 - Sou novo(a) aqui")
        print("3 - Já tenho cadastro")
        print("0 - Sair")
        escolha = input("Escolha: ")

        if escolha == "1":
            medico()
            menu_med()
        elif escolha == "2":
            cadastro()
            if login():
                menu_usuario()
        elif escolha == "3":
            if login():
                menu_usuario()
        elif escolha == "0":
            print("Encerrando o programa.")
            break
        else:
            print("Opção inválida!")

# Início
usuario()

# Finalização
cursor.close()
conn.close()
