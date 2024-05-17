import re
import json
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
        print("\033[1;34mEscolha o tipo de cadastro:\033[m")
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
                    print("\033[1;31mCPF inválido. Por favor, digite um CPF válido.\033[m")
        elif tipo_escolha == '2':
            tipo_usuario = "fornecedor"
            while True:
                cpf_cnpj = input("Digite o CNPJ: ").strip()
                if self.validar_cnpj(cpf_cnpj):
                    break
                else:
                    print("\033[1;31mCNPJ inválido. Por favor, digite um CNPJ válido.\033[m")
        else:
            print("\033[1;31mEntrada inválida. Tente novamente.\033[m")
            return

        if tipo_escolha == '1':
            nome = input("Digite o nome: ").strip()
        else:
            nome = input("Digite a razão social: ").strip()

        senha = self.criar_senha()

        while True:
            email = input("Digite o email: ").strip()
            email_confirmacao = input("Confirme o email: ").strip()
            if email != email_confirmacao:
                print("\033[1;31mOs emails não coincidem. Por favor, digite novamente.\033[m")
                continue
            if self.validar_email(email):
                if email in self.usuarios:
                    print("\033[1;31mErro: Já existe um usuário cadastrado com este email.\033[m")
                else:
                    break
            else:
                print("\033[1;31mPor favor, insira um email válido.\033[m")

        while True:
            telefone = input("Digite o telefone (com DDD): ").strip()
            if self.validar_telefone(telefone):
                break
            else:
                print("\033[1;31mNúmero de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.\033[m")

        logradouro = input("Digite o logradouro: ").strip()
        while True:
            cep = input("Digite o CEP: ").strip()
            if self.validar_cep(cep):
                break
            else:
                print("\033[1;31mCEP inválido. Por favor, digite um CEP válido.\033[m")

        self.usuarios[email] = {
            "nome": nome,
            "email": email,
            "cpf_cnpj": cpf_cnpj,
            "tipo_usuario": tipo_usuario,
            "telefone": telefone,
            "logradouro": logradouro,
            "cep": cep,
            "senha": senha,
            "eventos": {},
            "preferencias_notificacao": "Não receber notificações"
        }
        print("\033[1;32mUsuário cadastrado com sucesso! 🎉\033[m")

    def validar_email(self, email):
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return True
        else:
            print("\033[1;31mEmail inválido. Por favor, insira um email válido.\033[m")
            return False

    def validar_telefone(self, telefone):
        if re.match(r"^\d{2}\d{8,9}$", telefone):
            return True
        else:
            print("\033[1;31mNúmero de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.\033[m")
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
            print("\033[1;31mCEP inválido. Por favor, insira um CEP válido.\033[m")
            return False

    def criar_senha(self):
        while True:
            print("\033[1;34mA senha deve conter pelo menos um número, uma letra maiúscula e ter mais de 5 caracteres.\033[m")
            senha = input("Crie uma senha para o usuário: ").strip()
            senha_confirmacao = input("Confirme sua senha: ").strip()

            if senha == senha_confirmacao:
                if re.search(r'[A-Z]', senha) and re.search(r'\d', senha) and len(senha) >= 5:
                    return senha
                else:
                    print("\033[1;31mSenha inválida. Certifique-se de que sua senha atenda aos requisitos e tente novamente.\033[m")
            else:
                print("\033[1;31mAs senhas não coincidem. Por favor, tente novamente.\033[m")

    def login(self):
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ")

        usuario = self.usuarios.get(email)
        if usuario and usuario['senha'] == senha:
            print("\033[1;32mLogin efetuado com sucesso! 🎉\033[m")
            if usuario['tipo_usuario'] == "cliente":
                self.menu_cliente(email)
            else:
                self.menu_fornecedor(email)
            return email
        else:
            print("\033[1;31mEmail ou senha inválidos.\033[m")
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
                print("\033[1;31mData inválida. Por favor, use o formato dd/mm/yyyy.\033[m")

        preferencias_usuario = input("Digite suas preferências para o orçamento: ").strip()
        orcamento_estimado = float(input("Digite o valor estimado para o orçamento: ").strip())

        evento_id = self.proximo_id
        self.proximo_id += 1

        self.usuarios[email]['eventos'][evento_id] = {
            "numero_cliente": self.usuarios[email]['telefone'],
            "detalhes_evento": detalhes_evento,
            "endereco_evento": endereco_evento,
            "data_evento": data_evento,
            "preferencias_usuario": preferencias_usuario,
            "orcamento_estimado": orcamento_estimado
        }
        print(f"\033[1;32mSolicitação de orçamento registrada com sucesso! 🎉 ID do evento: {evento_id}\033[m")

    def modificar_orcamento(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("\033[1;31mVocê não tem eventos cadastrados.\033[m")
            return

        self.visualizar_eventos(email)

        evento_id = int(input("Digite o ID do evento que deseja modificar: ").strip())
        if evento_id not in eventos:
            print("\033[1;31mID de evento inválido.\033[m")
            return

        evento = eventos[evento_id]
        print("\n\033[1;34mO que você gostaria de modificar?\033[m")
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
                    print("\033[1;31mData inválida. Por favor, use o formato dd/mm/yyyy.\033[m")
        elif escolha == '4':
            evento["preferencias_usuario"] = input("Digite suas novas preferências para o orçamento: ").strip()
        elif escolha == '5':
            evento["orcamento_estimado"] = float(input("Digite o novo valor estimado para o orçamento: ").strip())
        else:
            print("\033[1;31mOpção inválida. Nenhuma modificação foi feita.\033[m")
            return

        print("\033[1;32mSolicitação de orçamento modificada com sucesso!\033[m")

    def cancelar_orcamento(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("\033[1;31mVocê não tem eventos cadastrados.\033[m")
            return

        self.visualizar_eventos(email)

        evento_id = int(input("Digite o ID do evento que deseja cancelar: ").strip())
        if evento_id in eventos:
            del eventos[evento_id]
            print("\033[1;32mSolicitação de orçamento cancelada com sucesso!\033[m")
        else:
            print("\033[1;31mID de evento inválido.\033[m")

    def visualizar_eventos(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("\033[1;31mVocê não tem eventos cadastrados.\033[m")
            return

        print("\n\033[1;34mSeus Eventos Cadastrados:\033[m")
        for evento_id, evento in eventos.items():
            print(f"\n\033[1;33mID do Evento: {evento_id}\033[m")
            print(f"\033[1;36mDetalhes do Evento: {evento['detalhes_evento']}\033[m")
            print(f"\033[1;36mEndereço do Evento: {evento['endereco_evento']}\033[m")
            print(f"\033[1;36mData do Evento: {evento['data_evento'].strftime('%d/%m/%Y')}\033[m")
            print(f"\033[1;36mPreferências do Usuário: {evento['preferencias_usuario']}\033[m")
            print(f"\033[1;36mOrçamento Estimado: {evento['orcamento_estimado']}\033[m")
            print(f"\033[1;36mNúmero do Cliente: {evento['numero_cliente']}\033[m")

    def visualizar_orcamentos(self):
        print("\n\033[1;34mPropostas de Orçamentos Disponíveis:\033[m")
        for usuario_email, usuario in self.usuarios.items():
            for evento_id, orcamento in usuario['eventos'].items():
                print(f"\n\033[1;33mID do Evento: {evento_id}\033[m")
                print(f"\033[1;36mUsuário: {usuario_email}\033[m")
                print(f"\033[1;36mDetalhes do Evento: {orcamento['detalhes_evento']}\033[m")
                print(f"\033[1;36mEndereço do Evento: {orcamento['endereco_evento']}\033[m")
                print(f"\033[1;36mData do Evento: {orcamento['data_evento'].strftime('%d/%m/%Y')}\033[m")
                print(f"\033[1;36mPreferências do Usuário: {orcamento['preferencias_usuario']}\033[m")
                print(f"\033[1;36mOrçamento Estimado: {orcamento['orcamento_estimado']}\033[m")
                print(f"\033[1;36mNúmero do Cliente: {orcamento['numero_cliente']}\033[m")

    def alterar_dados(self, email):
        usuario = self.usuarios[email]
        print("\n\033[1;34mAlterar Dados do Usuário:\033[m")
        print("1. Nome/Razão Social")
        print("2. Senha")
        print("3. Telefone")
        print("4. Logradouro")
        print("5. CEP")
        escolha = input("Escolha uma opção (1-5): ")

        if escolha == '1':
            if usuario['tipo_usuario'] == 'cliente':
                usuario["nome"] = input("Digite o novo nome: ").strip()
            else:
                usuario["nome"] = input("Digite a nova razão social: ").strip()
        elif escolha == '2':
            nova_senha = self.criar_senha()
            if nova_senha:
                usuario["senha"] = nova_senha
        elif escolha == '3':
            while True:
                novo_telefone = input("Digite o novo telefone (com DDD): ").strip()
                if self.validar_telefone(novo_telefone):
                    usuario["telefone"] = novo_telefone
                    break
                else:
                    print("\033[1;31mNúmero de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.\033[m")
        elif escolha == '4':
            usuario["logradouro"] = input("Digite o novo logradouro: ").strip()
        elif escolha == '5':
            while True:
                novo_cep = input("Digite o novo CEP: ").strip()
                if self.validar_cep(novo_cep):
                    usuario["cep"] = novo_cep
                    break
                else:
                    print("\033[1;31mCEP inválido. Por favor, digite um CEP válido.\033[m")
        else:
            print("\033[1;31mOpção inválida. Nenhuma modificação foi feita.\033[m")
            return

        print("\033[1;32mDados alterados com sucesso!\033[m")

    def cancelar_conta(self, email):
        confirmacao = input("\033[1;31mTem certeza que deseja cancelar sua conta? Esta ação não pode ser desfeita. (s/n): \033[m").strip().lower()
        if confirmacao == 's':
            del self.usuarios[email]
            print("\033[1;32mConta cancelada com sucesso!\033[m")
            return True
        else:
            print("\033[1;34mAção cancelada.\033[m")
            return False

    def atualizar_preferencias_notificacao(self, email):
        print("\nComo você gostaria de receber notificações sobre novos serviços ou mudanças?")
        print("1. Email")
        print("2. SMS")
        print("3. Não receber notificações")
        escolha = input("Escolha uma opção (1-3): ")
        if escolha == '1':
            self.usuarios[email]['preferencias_notificacao'] = "Email"
            print("Você escolheu receber atualizações por Email.")
        elif escolha == '2':
            self.usuarios[email]['preferencias_notificacao'] = "SMS"
            print("Você escolheu receber atualizações por SMS.")
        elif escolha == '3':
            self.usuarios[email]['preferencias_notificacao'] = "Não receber notificações"
            print("Você não receberá notificações de atualizações.")
        else:
            print("Opção inválida. Nenhuma mudança foi feita em suas preferências.")

    def menu_cliente(self, email):
        while True:
            print("\n\033[1;34mMenu do Cliente:\033[m")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Solicitar Orçamento")
            print("4. Modificar Orçamento")
            print("5. Cancelar Orçamento")
            print("6. Visualizar Eventos")
            print("7. Atualizar Preferências de Notificação")
            print("8. Sair")
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
                self.atualizar_preferencias_notificacao(email)
            elif escolha == '8':
                print("\033[1;34mVocê saiu do sistema.\033[m")
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

    def menu_fornecedor(self, email):
        while True:
            print("\n\033[1;34mMenu do Fornecedor:\033[m")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Visualizar Propostas de Orçamento")
            print("4. Atualizar Preferências de Notificação")
            print("5. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.alterar_dados(email)
            elif escolha == '2':
                if self.cancelar_conta(email):
                    break
            elif escolha == '3':
                self.visualizar_orcamentos()
            elif escolha == '4':
                self.atualizar_preferencias_notificacao(email)
            elif escolha == '5':
                print("\033[1;34mVocê saiu do sistema.\033[m")
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

    def salvar_dados(self, arquivo="dados.json"):
        with open(arquivo, "w") as f:
            json.dump(self.usuarios, f, indent=4, default=str)
        print("\033[1;32mDados salvos com sucesso!\033[m")

    def carregar_dados(self, arquivo="dados.json"):
        try:
            with open(arquivo, "r") as f:
                self.usuarios = json.load(f)
            print("\033[1;32mDados carregados com sucesso!\033[m")
        except FileNotFoundError:
            print("\033[1;31mArquivo de dados não encontrado. Começando com dados vazios.\033[m")

def main_menu(sistema):
    sistema.carregar_dados()
    while True:
        print("\n\033[1;34mBem-vindo ao Sistema de Cadastro\033[m")
        print("1. Login")
        print("2. Cadastrar Usuário")
        print("3. Sair")
        escolha = input("Escolha uma opção: ")

        if escolha == '1':
            sistema.login()
        elif escolha == '2':
            sistema.cadastrar_usuario()
        elif escolha == '3':
            sistema.salvar_dados()
            print("\033[1;34mSaindo do sistema...\033[m")
            break

        else:
            print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

if __name__ == "__main__":
    sistema = SistemaCadastro()
    main_menu(sistema)
