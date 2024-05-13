import re

class SistemaCadastro:
    def __init__(self):
        self.usuarios = {}
        self.servicos = {
            "Planejamento de Eventos": "Assistência completa na organização de eventos.",
            "Catering": "Opções de buffet personalizáveis para todos os tipos de eventos.",
            "Decoração": "Decoração customizada para diversos eventos.",
            "Entretenimento": "DJs, bandas ao vivo, mágicos, etc."
        }

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
            self.cadastro_empresa(cpf_cnpj)
            return
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

        self.usuarios[email] = {
            "nome": nome,
            "email": email,
            "cpf_cnpj": cpf_cnpj,
            "tipo_usuario": tipo_usuario,
            "telefone": telefone,
            "senha": senha
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
        # Validação do primeiro dígito verificador
        soma = sum((10 - i) * int(cpf[i]) for i in range(9))
        resto = soma % 11
        if int(cpf[9]) != (11 - resto if resto > 1 else 0):
            return False
        # Validação do segundo dígito verificador
        soma = sum((11 - i) * int(cpf[i]) for i in range(10))
        resto = soma % 11
        if int(cpf[10]) != (11 - resto if resto > 1 else 0):
            return False
        return True

    def validar_cnpj(self, cnpj):
        cnpj = ''.join(re.findall(r'\d', cnpj))
        if (not cnpj) or (len(cnpj) != 14):
            return False
        # Validação dos dígitos verificadores
        multiplicadores = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        # Primeiro dígito
        soma = sum(int(cnpj[i]) * multiplicadores[i] for i in range(12))
        resto = soma % 11
        if int(cnpj[12]) != (11 - resto if resto > 1 else 0):
            return False
        # Segundo dígito
        multiplicadores.insert(0, 6)
        soma = sum(int(cnpj[i]) * multiplicadores[i] for i in range(13))
        resto = soma % 11
        if int(cnpj[13]) != (11 - resto if resto > 1 else 0):
            return False
        return True

    def criar_senha(self):
        print("A senha deve conter pelo menos um número e uma letra maiúscula.")
        senha = input("Crie uma senha para o usuário: ").strip()
        confirmacao_senha = input("Confirme sua senha: ").strip()

        if senha == confirmacao_senha and re.search(r'[A-Z]', senha) and re.search(r'\d', senha):
            return senha
        else:
            print("Senha inválida ou não confere. Certifique-se de que sua senha atenda aos requisitos e tente novamente.")
            return None

    def login(self):
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ").strip()

        usuario = self.usuarios.get(email)
        if usuario and usuario['senha'] == senha:
            print("Login efetuado com sucesso!")
            self.apresentacao_servicos()
            return email
        else:
            print("Email ou senha inválidos.")
            return None

    def apresentacao_servicos(self):
        print("\nBem-vindo ao Sistema! Aqui estão os serviços que oferecemos:")
        for servico, descricao in self.servicos.items():
            print(f"{servico}: {descricao}")
        self.atualizar_preferencias_notificacao()

    def atualizar_preferencias_notificacao(self):
        print("\nComo você gostaria de receber notificações sobre novos serviços ou mudanças?")
        print("1. Email")
        print("2. SMS")
        print("3. Não receber notificações")
        escolha = input("Escolha uma opção (1-3): ")
        if escolha == '1':
            print("Você escolheu receber atualizações por Email.")
        elif escolha == '2':
            print("Você escolheu receber atualizações por SMS.")
        elif escolha == '3':
            print("Você não receberá notificações de atualizações.")
        else:
            print("Opção inválida. Nenhuma mudança foi feita em suas preferências.")

    def alterar_dados(self, email):
        while True:
            usuario = self.usuarios.get(email)
            print("\nQual dado você gostaria de alterar?")
            print("1. Nome")
            print("2. CPF/CNPJ")
            print("3. Tipo de usuário")
            print("4. Telefone")
            print("5. Senha")
            print("6. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                novo_nome = input("Digite o novo nome: ").strip()
                usuario['nome'] = novo_nome
                print("Nome atualizado com sucesso!")
            elif escolha == '2':
                if usuario['tipo_usuario'] == "cliente":
                    while True:
                        novo_cpf_cnpj = input("Digite o novo CPF: ").strip()
                        if self.validar_cpf(novo_cpf_cnpj):
                            usuario['cpf_cnpj'] = novo_cpf_cnpj
                            print("CPF atualizado com sucesso!")
                            break
                        else:
                            print("CPF inválido. Por favor, digite um CPF válido.")
                else:
                    while True:
                        novo_cpf_cnpj = input("Digite o novo CNPJ: ").strip()
                        if self.validar_cnpj(novo_cpf_cnpj):
                            usuario['cpf_cnpj'] = novo_cpf_cnpj
                            print("CNPJ atualizado com sucesso!")
                            break
                        else:
                            print("CNPJ inválido. Por favor, digite um CNPJ válido.")
            elif escolha == '3':
                novo_tipo_usuario = input("Digite o novo tipo de usuário (cliente/fornecedor): ").strip()
                usuario['tipo_usuario'] = novo_tipo_usuario
                print("Tipo de usuário atualizado com sucesso!")
            elif escolha == '4':
                novo_telefone = input("Digite o novo telefone: ").strip()
                if self.validar_telefone(novo_telefone):
                    usuario['telefone'] = novo_telefone
                    print("Telefone atualizado com sucesso!")
            elif escolha == '5':
                nova_senha = self.criar_senha()
                if nova_senha:
                    usuario['senha'] = nova_senha
                    print("Senha atualizada com sucesso!")
            elif escolha == '6':
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

    def cancelar_conta(self, email):
        if email in self.usuarios:
            del self.usuarios[email]
            print("Conta cancelada com sucesso!")
            return True
        else:
            print("Erro: Usuário não encontrado.")
            return False

def main_menu(sistema):
    current_user = None
    while True:
        if not current_user:
            print("\nBem-vindo ao Sistema de Cadastro")
            print("1. Login")
            print("2. Cadastrar Usuário")
            print("4. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                current_user = sistema.login()
            elif escolha == '2':
                sistema.cadastrar_usuario()
            elif escolha == '4':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
        else:
            print("\nMenu do Usuário")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                sistema.alterar_dados(current_user)
            elif escolha == '2':
                if sistema.cancelar_conta(current_user):
                    current_user = None
            elif escolha == '3':
                current_user = None  # Log out
                print("Você saiu do sistema.")
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    sistema = SistemaCadastro()
    main_menu(sistema)
