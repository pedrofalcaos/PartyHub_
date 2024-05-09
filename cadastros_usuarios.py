class SistemaCadastro:
    def __init__(self):
        self.usuarios = {}

    def cadastrar_usuario(self):
        while True:
            print("Escolha o tipo de cadastro:")
            print("1. Pessoa Física")
            print("2. Empresa")
            tipo_escolha = input("Digite o número correspondente ao tipo de usuário (1 ou 2): ")

            if tipo_escolha == '1':
                tipo_usuario = "cliente"
                cpf_cnpj = input("Digite o CPF: ").strip()
                break
            elif tipo_escolha == '2':
                tipo_usuario = "fornecedor"
                cpf_cnpj = input("Digite o CNPJ: ").strip()
                self.cadastro_empresa(cpf_cnpj)
                return True
            else:
                print("Entrada inválida. Por favor, escolha 1 para Pessoa Física ou 2 para Empresa.")

        nome = input("Digite o nome: ").strip()
        email = input("Digite o email: ").strip()
        telefone = input("Digite o telefone: ").strip()
        senha = input("Crie uma senha para o usuário: ").strip()

        if email in self.usuarios:
            print("Erro: Já existe um usuário cadastrado com este email.")
            return False

        self.usuarios[email] = {
            "nome": nome,
            "email": email,
            "cpf_cnpj": cpf_cnpj,
            "tipo_usuario": tipo_usuario,
            "telefone": telefone,
            "senha": senha
        }
        print("Usuário cadastrado com sucesso!")
        return True

    def cadastro_empresa(self, cnpj):
        razao_social = input("Digite a razão social da empresa: ").strip()
        endereco = input("Digite o endereço da empresa: ").strip()
        email_contato = input("Digite o email de contato da empresa: ").strip()
        senha = input("Crie uma senha para a empresa: ").strip()

        self.usuarios[email_contato] = {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "endereco": endereco,
            "email_contato": email_contato,
            "tipo_usuario": "fornecedor",
            "senha": senha
        }
        print("Cadastro de empresa realizado com sucesso!")

    def login(self):
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ").strip()

        usuario = self.usuarios.get(email)
        if usuario and usuario['senha'] == senha:
            print("Login efetuado com sucesso!")
            return email
        else:
            print("Email ou senha inválidos.")
            return None

    def alterar_dados(self, email):
        while True:
            usuario = self.usuarios[email]
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
                if novo_nome:
                    usuario['nome'] = novo_nome
                    print("Nome atualizado com sucesso!")
            elif escolha == '2':
                novo_cpf_cnpj = input("Digite o novo CPF/CNPJ: ").strip()
                if novo_cpf_cnpj:
                    usuario['cpf_cnpj'] = novo_cpf_cnpj
                    print("CPF/CNPJ atualizado com sucesso!")
            elif escolha == '3':
                novo_tipo_usuario = input("Digite o novo tipo de usuário (cliente/fornecedor): ").strip()
                if novo_tipo_usuario:
                    usuario['tipo_usuario'] = novo_tipo_usuario
                    print("Tipo de usuário atualizado com sucesso!")
            elif escolha == '4':
                novo_telefone = input("Digite o novo telefone: ").strip()
                if novo_telefone:
                    usuario['telefone'] = novo_telefone
                    print("Telefone atualizado com sucesso!")
            elif escolha == '5':
                nova_senha = input("Digite a nova senha: ").strip()
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
            print("3. Cancelar Conta")
            print("4. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                current_user = sistema.login()
            elif escolha == '2':
                sistema.cadastrar_usuario()
            elif escolha == '3':
                email = input("Digite o email do usuário para cancelar a conta: ")
                sistema.cancelar_conta(email)
            elif escolha == '4':
                print("Saindo do sistema...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")
        else:
            print("\nMenu do Usuário")
            print("1. Alterar Dados")
            print("2. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                sistema.alterar_dados(current_user)
            elif escolha == '2':
                current_user = None  # Log out
                print("Você saiu do sistema.")
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

if __name__ == "__main__":
    sistema = SistemaCadastro()
    main_menu(sistema)
