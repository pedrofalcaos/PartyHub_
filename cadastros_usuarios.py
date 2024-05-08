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
                self.cadastro_empresa(cpf_cnpj)  # Chamada de método específico para cadastro de empresa
                return True
            else:
                print("Entrada inválida. Por favor, escolha 1 para Pessoa Física ou 2 para Empresa.")

        # Coleta as informações gerais do usuário
        nome = input("Digite o nome: ").strip()
        email = input("Digite o email: ").strip()
        telefone = input("Digite o telefone: ").strip()

        # Verifica se o email já está cadastrado
        if email in self.usuarios:
            print("Erro: Já existe um usuário cadastrado com este email.")
            return False

        # Adiciona o novo usuário
        self.usuarios[email] = {
            "nome": nome,
            "email": email,
            "cpf_cnpj": cpf_cnpj,
            "tipo_usuario": tipo_usuario,
            "telefone": telefone
        }
        print("Usuário cadastrado com sucesso!")
        return True

    def cadastro_empresa(self, cnpj):
        # Pode incluir validações ou requisitos adicionais específicos para empresas
        razao_social = input("Digite a razão social da empresa: ").strip()
        endereco = input("Digite o endereço da empresa: ").strip()
        email_contato = input("Digite o email de contato da empresa: ").strip()

        # Armazenamento dos dados específicos de empresa
        self.usuarios[email_contato] = {
            "razao_social": razao_social,
            "cnpj": cnpj,
            "endereco": endereco,
            "email_contato": email_contato,
            "tipo_usuario": "fornecedor"
        }
        print("Cadastro de empresa realizado com sucesso!")

    def alterar_dados(self, email, nome=None, cpf_cnpj=None, tipo_usuario=None, telefone=None):
        if email not in self.usuarios:
            print("Erro: Usuário não encontrado.")
            return False

        if nome:
            self.usuarios[email]['nome'] = nome
        if cpf_cnpj:
            self.usuarios[email]['cpf_cnpj'] = cpf_cnpj
        if tipo_usuario:
            self.usuarios[email]['tipo_usuario'] = tipo_usuario
        if telefone:
            self.usuarios[email]['telefone'] = telefone

        print("Dados atualizados com sucesso!")
        return True

    def cancelar_conta(self, email):
        if email in self.usuarios:
            del self.usuarios[email]
            print("Conta cancelada com sucesso!")
            return True
        else:
            print("Erro: Usuário não encontrado.")
            return False


# Exemplo de uso do sistema
sistema = SistemaCadastro()
sistema.cadastrar_usuario()
