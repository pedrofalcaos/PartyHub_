import re
from datetime import datetime


class SistemaCadastro:
    def __init__(self):
        self.usuarios = {}
        self.servicos = {
            "Planejamento de Eventos": "Assistência completa na organização de eventos.",
            "Catering": "Opções de buffet personalizáveis para todos os tipos de eventos.",
            "Decoração": "Decoração customizada para diversos eventos.",
            "Entretenimento": "DJs, bandas ao vivo, mágicos, etc."
        }
        self.proximo_id = 1

    def cadastrar_usuario(self):
        print("Escolha o tipo de cadastro:")
        print("1. Pessoa Física")
        print("2. Empresa")
        tipo_escolha = input("Digite o número correspondente ao tipo de usuário (1 ou 2): ")

        if tipo_escolha == '1':
            tipo_usuario = "cliente"
            while True:
                cpf_cnpj = input("Digite o CPF: ").strip()
                if self.validar_cpf(cpf_cnpj):
                    break
                else:
                    print("CPF inválido. Por favor, digite um CPF válido.")
        elif tipo_escolha == '2':
            tipo_usuario = "fornecedor"
            while True:
                cpf_cnpj = input("Digite o CNPJ: ").strip()
                if self.validar_cnpj(cpf_cnpj):
                    break
                else:
                    print("CNPJ inválido. Por favor, digite um CNPJ válido.")
        else:
            print("Entrada inválida. Tente novamente.")
            return

        nome = input("Digite o nome: ").strip()
        senha = self.criar_senha()
        if senha is None:
            return

        while True:
            email = input("Digite o email: ").strip()
            if self.validar_email(email):
                if email in self.usuarios:
                    print("Erro: Já existe um usuário cadastrado com este email.")
                else:
                    break
            else:
                print("Por favor, insira um email válido.")

        while True:
            telefone = input("Digite o telefone (com DDD): ").strip()
            if self.validar_telefone(telefone):
                break
            else:
                print("Número de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.")

        logradouro = input("Digite o logradouro: ").strip()
        while True:
            cep = input("Digite o CEP: ").strip()
            if self.validar_cep(cep):
                break
            else:
                print("CEP inválido. Por favor, digite um CEP válido.")

        self.usuarios[email] = {
            "nome": nome,
            "email": email,
            "cpf_cnpj": cpf_cnpj,
            "tipo_usuario": tipo_usuario,
            "telefone": telefone,
            "logradouro": logradouro,
            "cep": cep,
            "senha": senha,
            "eventos": {}
        }
        print("Usuário cadastrado com sucesso!")

    def validar_email(self, email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            print("Email inválido. Por favor, insira um email válido.")
            return False

    def validar_telefone(self, telefone):
        if re.match(r"^\d{2}\d{8,9}$", telefone):
            return True
        else:
            print("Número de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.")
            return False

    def validar_cpf(self, cpf):
        cpf = ''.join(re.findall(r'\d', cpf))
        if (not cpf) or (len(cpf) != 11) or (cpf == cpf[0] * 11):
            return False
        soma = sum((10 - i) * int(cpf[i]) for i in range(9))
        resto = soma % 11
        if int(cpf[9]) != (11 - resto if resto > 1 else 0):
            return False
        soma = sum((11 - i) * int(cpf[i]) for i in range(10))
        resto = soma % 11
        if int(cpf[10]) != (11 - resto if resto > 1 else 0):
            return False
        return True

    def validar_cnpj(self, cnpj):
        cnpj = ''.join(re.findall(r'\d', cnpj))
        if (not cnpj) or (len(cnpj) != 14):
            return False
        multiplicadores = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj[i]) * multiplicadores[i] for i in range(12))
        resto = soma % 11
        if int(cnpj[12]) != (11 - resto if resto > 1 else 0):
            return False
        multiplicadores.insert(0, 6)
        soma = sum(int(cnpj[i]) * multiplicadores[i] for i in range(13))
        resto = soma % 11
        if int(cnpj[13]) != (11 - resto if resto > 1 else 0):
            return False
        return True

    def validar_cep(self, cep):
        if re.match(r"^\d{5}-?\d{3}$", cep):
            return True
        else:
            print("CEP inválido. Por favor, insira um CEP válido.")
            return False

    def criar_senha(self):
        print("A senha deve conter pelo menos um número, uma letra maiúscula e ter mais de 5 caracteres.")
        senha = input("Crie uma senha para o usuário: ").strip()
        confirmacao_senha = input("Confirme sua senha: ").strip()

        if (senha == confirmacao_senha and re.search(r'[A-Z]', senha) and
                re.search(r'\d', senha) and len(senha) > 5):
            return senha
        else:
            print(
                "Senha inválida ou não confere. Certifique-se de que sua senha atenda aos requisitos e tente novamente.")
            return None

    def login(self):
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ").strip()

        usuario = self.usuarios.get(email)
        if usuario and usuario['senha'] == senha:
            print("Login efetuado com sucesso!")
            if usuario['tipo_usuario'] == "cliente":
                self.menu_cliente(email)
            else:
                self.menu_fornecedor(email)
            return email
        else:
            print("Email ou senha inválidos.")
            return None

    def solicitar_orcamento(self, email):
        detalhes_evento = input("Descreva os detalhes do evento: ").strip()
        endereco_evento = input("Digite o endereço do evento: ").strip()
        while True:
            data_evento = input("Digite a data do evento (dd/mm/yyyy): ").strip()
            try:
                data_evento = datetime.strptime(data_evento, "%d/%m/%Y")
                break
            except ValueError:
                print("Data inválida. Por favor, use o formato dd/mm/yyyy.")

        preferencias_usuario = input("Digite suas preferências para o orçamento: ").strip()
        orcamento_estimado = float(input("Digite o valor estimado para o orçamento: ").strip())

        evento_id = self.proximo_id
        self.proximo_id += 1

        self.usuarios[email]['eventos'][evento_id] = {
            "detalhes_evento": detalhes_evento,
            "endereco_evento": endereco_evento,
            "data_evento": data_evento,
            "preferencias_usuario": preferencias_usuario,
            "orcamento_estimado": orcamento_estimado
        }
        print(f"Solicitação de orçamento registrada com sucesso! ID do evento: {evento_id}")

    def modificar_orcamento(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("Você não tem eventos cadastrados.")
            return

        self.visualizar_eventos(email)

        evento_id = int(input("Digite o ID do evento que deseja modificar: ").strip())
        if evento_id not in eventos:
            print("ID de evento inválido.")
            return

        evento = eventos[evento_id]
        print("\nO que você gostaria de modificar?")
        print("1. Detalhes do Evento")
        print("2. Endereço do Evento")
        print("3. Data do Evento")
        print("4. Preferências do Usuário")
        print("5. Orçamento Estimado")
        escolha = input("Escolha uma opção (1-5): ")

        if escolha == '1':
            evento["detalhes_evento"] = input("Descreva os novos detalhes do evento: ").strip()
        elif escolha == '2':
            evento["endereco_evento"] = input("Digite o novo endereço do evento: ").strip()
        elif escolha == '3':
            while True:
                data_evento = input("Digite a nova data do evento (dd/mm/yyyy): ").strip()
                try:
                    evento["data_evento"] = datetime.strptime(data_evento, "%d/%m/%Y")
                    break
                except ValueError:
                    print("Data inválida. Por favor, use o formato dd/mm/yyyy.")
        elif escolha == '4':
            evento["preferencias_usuario"] = input("Digite suas novas preferências para o orçamento: ").strip()
        elif escolha == '5':
            evento["orcamento_estimado"] = float(input("Digite o novo valor estimado para o orçamento: ").strip())
        else:
            print("Opção inválida. Nenhuma modificação foi feita.")
            return

        print("Solicitação de orçamento modificada com sucesso!")

    def cancelar_orcamento(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("Você não tem eventos cadastrados.")
            return

        self.visualizar_eventos(email)

        evento_id = int(input("Digite o ID do evento que deseja cancelar: ").strip())
        if evento_id in eventos:
            del eventos[evento_id]
            print("Solicitação de orçamento cancelada com sucesso!")
        else:
            print("ID de evento inválido.")

    def visualizar_eventos(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("Você não tem eventos cadastrados.")
            return

        print("\nSeus Eventos Cadastrados:")
        for evento_id, evento in eventos.items():
            print(f"\nID do Evento: {evento_id}")
            print(f"Detalhes do Evento: {evento['detalhes_evento']}")
            print(f"Endereço do Evento: {evento['endereco_evento']}")
            print(f"Data do Evento: {evento['data_evento'].strftime('%d/%m/%Y')}")
            print(f"Preferências do Usuário: {evento['preferencias_usuario']}")
            print(f"Orçamento Estimado: {evento['orcamento_estimado']}")

    def visualizar_orcamentos(self):
        print("\nPropostas de Orçamentos Disponíveis:")
        for usuario_email, usuario in self.usuarios.items():
            for evento_id, orcamento in usuario['eventos'].items():
                print(f"\nUsuário: {usuario_email}")
                print(f"ID do Evento: {evento_id}")
                print(f"Detalhes do Evento: {orcamento['detalhes_evento']}")
                print(f"Endereço do Evento: {orcamento['endereco_evento']}")
                print(f"Data do Evento: {orcamento['data_evento'].strftime('%d/%m/%Y')}")
                print(f"Preferências do Usuário: {orcamento['preferencias_usuario']}")
                print(f"Orçamento Estimado: {orcamento['orcamento_estimado']}")

    def menu_cliente(self, email):
        while True:
            print("\nMenu do Cliente")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Solicitar Orçamento")
            print("4. Modificar Orçamento")
            print("5. Cancelar Orçamento")
            print("6. Visualizar Eventos")
            print("7. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.alterar_dados(email)
            elif escolha == '2':
                if self.cancelar_conta(email):
                    break
            elif escolha == '3':
                self.solicitar_orcamento(email)
            elif escolha == '4':
                self.modificar_orcamento(email)
            elif escolha == '5':
                self.cancelar_orcamento(email)
            elif escolha == '6':
                self.visualizar_eventos(email)
            elif escolha == '7':
                print("Você saiu do sistema.")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

    def menu_fornecedor(self, email):
        while True:
            print("\nMenu do Fornecedor")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Visualizar Propostas de Orçamento")
            print("4. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.alterar_dados(email)
            elif escolha == '2':
                if self.cancelar_conta(email):
                    break
            elif escolha == '3':
                self.visualizar_orcamentos()
            elif escolha == '4':
                print("Você saiu do sistema.")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")


def main_menu(sistema):
    while True:
        print("\nBem-vindo ao Sistema de Cadastro")
        print("1. Login")
        print("2. Cadastrar Usuário")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            sistema.login()
        elif escolha == '2':
            sistema.cadastrar_usuario()
        elif escolha == '3':
            print("Saindo do sistema...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":
    sistema = SistemaCadastro()
    main_menu(sistema)
