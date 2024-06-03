import re
import json
import os
from datetime import datetime


class SistemaCadastro:
    def __init__(self):
        self.usuarios = {}
        self.servicos = {
            1: "Planejamento de Eventos",
            2: "Catering",
            3: "Decoração",
            4: "Entretenimento",
            5: "Outros"
        }
        self.descricoes_servicos = {
            "Planejamento de Eventos": "Assistência completa na organização de eventos.",
            "Catering": "Opções de buffet personalizáveis para todos os tipos de eventos.",
            "Decoração": "Decoração customizada para diversos eventos.",
            "Entretenimento": "DJs, bandas ao vivo, mágicos, etc."
        }
        self.proximo_id = 1
        self.arquivo_dados = "dados.json"

    def salvar_dados(self):
        with open(self.arquivo_dados, "w") as f:
            json.dump(self.usuarios, f, indent=4, default=str)
        print("\033[1;32mDados salvos com sucesso!\033[m")

    def carregar_dados(self):
        if os.path.exists(self.arquivo_dados):
            try:
                with open(self.arquivo_dados, "r") as f:
                    self.usuarios = json.load(f)
                for usuario in self.usuarios.values():
                    for evento in usuario.get("eventos", {}).values():
                        if isinstance(evento["data_evento"], str):
                            evento["data_evento"] = datetime.strptime(evento["data_evento"], "%Y-%m-%d %H:%M:%S")
                        if "hora_evento" not in evento:
                            evento["hora_evento"] = "Não especificada"
                        if "convidados" not in evento:
                            evento["convidados"] = []
                        if "feedbacks" not in evento:
                            evento["feedbacks"] = []
                print("\033[1;32mDados carregados com sucesso!\033[m")
            except Exception as e:
                print(f"\033[1;31mErro ao carregar dados: {e}\033[m")
        else:
            print("\033[1;31mArquivo de dados não encontrado. Começando com dados vazios.\033[m")

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
                    if self.cpf_cnpj_existente(cpf_cnpj):
                        print("\033[1;31mErro: Já existe um usuário cadastrado com este CPF.\033[m")
                    else:
                        break
                else:
                    print("\033[1;31mCPF inválido. Por favor, digite um CPF válido.\033[m")
        elif tipo_escolha == '2':
            tipo_usuario = "fornecedor"
            while True:
                cpf_cnpj = input("Digite o CNPJ: ").strip()
                if self.validar_cnpj(cpf_cnpj):
                    if self.cpf_cnpj_existente(cpf_cnpj):
                        print("\033[1;31mErro: Já existe um usuário cadastrado com este CNPJ.\033[m")
                    else:
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
                print(
                    "\033[1;31mNúmero de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.\033[m")

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
        self.salvar_dados()
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
            print(
                "\033[1;31mNúmero de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.\033[m")
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

    def cpf_cnpj_existente(self, cpf_cnpj):
        for usuario in self.usuarios.values():
            if usuario["cpf_cnpj"] == cpf_cnpj:
                return True
        return False

    def criar_senha(self):
        while True:
            print(
                "\033[1;34mA senha deve conter pelo menos um número, uma letra maiúscula e ter mais de 5 caracteres.\033[m")
            senha = input("Crie uma senha para o usuário: ").strip()
            senha_confirmacao = input("Confirme sua senha: ").strip()

            if senha == senha_confirmacao:
                if re.search(r'[A-Z]', senha) and re.search(r'\d', senha) and len(senha) >= 5:
                    return senha
                else:
                    print(
                        "\033[1;31mSenha inválida. Certifique-se de que sua senha atenda aos requisitos e tente novamente.\033[m")
            else:
                print("\033[1;31mAs senhas não coincidem. Por favor, tente novamente.\033[m")

    def login(self):
        email = input("Digite seu email: ").strip()
        senha = input("Digite sua senha: ").strip()

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

    def cadastrar_evento(self, email):
        detalhes_evento = input("Descreva os detalhes do evento: ").strip()
        endereco_evento = input("Digite o endereço do evento: ").strip()
        while True:
            data_evento = input("Digite a data do evento (dd/mm/yyyy): ").strip()
            try:
                data_evento = datetime.strptime(data_evento, "%d/%m/%Y")
                break
            except ValueError:
                print("\033[1;31mData inválida. Por favor, use o formato dd/mm/yyyy.\033[m")
        hora_evento = input("Digite a hora do evento (HH:MM): ").strip()

        evento_id = self.proximo_id
        self.proximo_id += 1

        self.usuarios[email]['eventos'][evento_id] = {
            "detalhes_evento": detalhes_evento,
            "endereco_evento": endereco_evento,
            "data_evento": data_evento,
            "hora_evento": hora_evento,
            "orcamentos": [],
            "convidados": [],
            "feedbacks": []
        }
        self.salvar_dados()
        print(f"\033[1;32mEvento cadastrado com sucesso! 🎉 ID do evento: {evento_id}\033[m")

    def modificar_evento(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento que deseja modificar: "))

        if evento_id in self.usuarios[email]['eventos']:
            evento = self.usuarios[email]['eventos'][evento_id]
            print("\033[1;34mO que você gostaria de modificar?\033[m")
            print("1. Detalhes do Evento")
            print("2. Endereço do Evento")
            print("3. Data do Evento")
            print("4. Hora do Evento")
            escolha = input("Escolha uma opção (1-4): ")

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
                evento["hora_evento"] = input("Digite a nova hora do evento (HH:MM): ").strip()
            else:
                print("\033[1;31mOpção inválida. Nenhuma modificação foi feita.\033[m")
                return

            self.salvar_dados()
            print("\033[1;32mEvento modificado com sucesso!\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def cancelar_evento(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento que deseja cancelar: "))

        if evento_id in self.usuarios[email]['eventos']:
            confirmacao = input(
                "Tem certeza de que deseja cancelar o evento? Esta ação também cancelará todos os orçamentos associados. (s/n): ").strip().lower()
            if confirmacao == 's':
                del self.usuarios[email]['eventos'][evento_id]
                self.salvar_dados()
                print("\033[1;32mEvento e orçamentos associados cancelados com sucesso!\033[m")
            else:
                print("\033[1;34mOperação cancelada.\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def solicitar_orcamento(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento para o qual deseja solicitar um orçamento: "))

        if evento_id in self.usuarios[email]['eventos']:
            print("\033[1;34mServiços disponíveis:\033[m")
            for num, servico in self.servicos.items():
                print(f"{num}. {servico} - {self.descricoes_servicos.get(servico, 'Outros')}")
            servicos_solicitados = []
            while True:
                escolha = int(input("Digite o número do serviço desejado (1-5): ").strip())
                if escolha in self.servicos:
                    servicos_solicitados.append(self.servicos[escolha])
                    if escolha != 5:
                        break
                else:
                    print("\033[1;31mServiço inválido. Por favor, escolha um serviço da lista.\033[m")
            detalhes_adicionais = input("Digite mais detalhes sobre o que você precisa: ").strip()
            valor_planejado = input("Digite o valor planejado para o orçamento em R$: ").strip()

            orcamento_id = f"orc_{len(self.usuarios[email]['eventos'][evento_id]['orcamentos']) + 1}"
            self.usuarios[email]['eventos'][evento_id]['orcamentos'].append({
                "id": orcamento_id,
                "servicos": servicos_solicitados,
                "detalhes_adicionais": detalhes_adicionais,
                "valor_planejado": valor_planejado,
                "status": "Pendente",
                "fornecedor": ""
            })
            self.salvar_dados()
            print(f"\033[1;32mOrçamento solicitado com sucesso para o evento {evento_id}! 🎉\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def modificar_orcamento(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento para o qual deseja modificar o orçamento: "))

        if evento_id in self.usuarios[email]['eventos']:
            evento = self.usuarios[email]['eventos'][evento_id]
            if evento['orcamentos']:
                orcamento_id = input("Digite o ID do orçamento que deseja modificar: ").strip()
                orcamento = next((orc for orc in evento['orcamentos'] if orc['id'] == orcamento_id), None)

                if orcamento:
                    print("\033[1;34mServiços disponíveis:\033[m")
                    for num, servico in self.servicos.items():
                        print(f"{num}. {servico} - {self.descricoes_servicos.get(servico, 'Outros')}")
                    novos_servicos = []
                    while True:
                        escolha = int(input("Digite o número do serviço desejado (1-5): ").strip())
                        if escolha in self.servicos:
                            novos_servicos.append(self.servicos[escolha])
                            if escolha != 5:
                                break
                        else:
                            print("\033[1;31mServiço inválido. Por favor, escolha um serviço da lista.\033[m")
                    detalhes_adicionais = input("Digite mais detalhes sobre o que você precisa: ").strip()
                    novo_valor_planejado = input("Digite o novo valor planejado para o orçamento em R$: ").strip()

                    orcamento['servicos'] = novos_servicos
                    orcamento['detalhes_adicionais'] = detalhes_adicionais
                    orcamento['valor_planejado'] = novo_valor_planejado
                    orcamento['status'] = "Pendente"
                    self.salvar_dados()
                    print(f"\033[1;32mOrçamento modificado com sucesso para o evento {evento_id}! 🎉\033[m")
                else:
                    print("\033[1;31mID do orçamento não encontrado.\033[m")
            else:
                print("\033[1;31mNenhum orçamento solicitado para este evento.\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def cancelar_orcamento(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento para o qual deseja cancelar o orçamento: "))

        if evento_id in self.usuarios[email]['eventos']:
            evento = self.usuarios[email]['eventos'][evento_id]
            if evento['orcamentos']:
                orcamento_id = input("Digite o ID do orçamento que deseja cancelar: ").strip()
                orcamento = next((orc for orc in evento['orcamentos'] if orc['id'] == orcamento_id), None)

                if orcamento:
                    evento['orcamentos'].remove(orcamento)
                    self.salvar_dados()
                    print(f"\033[1;32mOrçamento cancelado com sucesso para o evento {evento_id}.\033[m")
                else:
                    print("\033[1;31mID do orçamento não encontrado.\033[m")
            else:
                print("\033[1;31mNenhum orçamento solicitado para este evento.\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def visualizar_eventos(self, email):
        eventos = self.usuarios[email].get('eventos', {})
        if eventos:
            print("\033[1;34mSeus Eventos:\033[m")
            for evento_id, evento in eventos.items():
                print(f"\033[1;36mID do Evento: {evento_id}\033[m")
                print(f"\033[1;36mDetalhes do Evento: {evento['detalhes_evento']}\033[m")
                print(f"\033[1;36mEndereço do Evento: {evento['endereco_evento']}\033[m")
                print(f"\033[1;36mData do Evento: {evento['data_evento'].strftime('%d/%m/%Y')}\033[m")
                print(f"\033[1;36mHora do Evento: {evento.get('hora_evento', 'Não especificada')}\033[m")
                if evento['orcamentos']:
                    for orcamento in evento['orcamentos']:
                        print(f"\033[1;36mOrçamento ID: {orcamento['id']}\033[m")
                        print(f"\033[1;36mServiços: {', '.join(orcamento['servicos'])}\033[m")
                        print(f"\033[1;36mDetalhes Adicionais: {orcamento['detalhes_adicionais']}\033[m")
                        print(f"\033[1;36mValor Planejado: R$ {orcamento['valor_planejado']}\033[m")
                        print(f"\033[1;36mStatus: {orcamento['status']}\033[m")
                        if orcamento['fornecedor']:
                            print(f"\033[1;36mFornecedor: {orcamento['fornecedor']}\033[m")
                            if "rating" in orcamento:
                                print(f"\033[1;36mAvaliação: {orcamento['rating']}/5\033[m")
                            if "comentario" in orcamento:
                                print(f"\033[1;36mComentário: {orcamento['comentario']}\033[m")
                if evento['convidados']:
                    for convidado in evento['convidados']:
                        print(f"\033[1;36mConvidado: {convidado['nome']}\033[m")
                        print(f"\033[1;36mEmail: {convidado['email']}\033[m")
                        print(f"\033[1;36mTelefone: {convidado['telefone']}\033[m")
                print("-" * 20)
        else:
            print("\033[1;31mVocê não possui eventos cadastrados.\033[m")

    def cadastrar_convidados(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento para o qual deseja cadastrar convidados: "))

        if evento_id in self.usuarios[email]['eventos']:
            evento = self.usuarios[email]['eventos'][evento_id]
            while True:
                nome = input("Digite o nome do convidado: ").strip()
                telefone = input("Digite o telefone do convidado (com DDD): ").strip()
                email_convidado = input("Digite o email do convidado: ").strip()

                convidado = {
                    "nome": nome,
                    "telefone": telefone,
                    "email": email_convidado
                }
                evento['convidados'].append(convidado)
                self.salvar_dados()
                print(f"\033[1;32mConvidado {nome} cadastrado com sucesso!\033[m")

                continuar = input("Deseja cadastrar outro convidado? (s/n): ").strip().lower()
                if continuar != 's':
                    break
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def enviar_convites(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento para o qual deseja enviar convites: "))

        if evento_id in self.usuarios[email]['eventos']:
            evento = self.usuarios[email]['eventos'][evento_id]
            if evento['convidados']:
                mensagem = ""
                incluir_mensagem = input("Deseja incluir uma mensagem personalizada? (s/n): ").strip().lower()
                if incluir_mensagem == 's':
                    mensagem = input("Digite a mensagem personalizada: ").strip()
                convite_preview = f"Convite para o evento {evento['detalhes_evento']}\n"
                convite_preview += f"Local: {evento['endereco_evento']}\n"
                convite_preview += f"Data: {evento['data_evento'].strftime('%d/%m/%Y')}\n"
                convite_preview += f"Hora: {evento['hora_evento']}\n"
                convite_preview += f"Organizado por: {self.usuarios[email]['nome']}\n"
                convite_preview += f"Telefone do organizador: {self.usuarios[email]['telefone']}\n"
                if mensagem:
                    convite_preview += f"Mensagem: {mensagem}\n"

                print("\033[1;34mPré-visualização do Convite:\033[m")
                print(convite_preview)

                confirmar_envio = input("Deseja enviar os convites? (s/n): ").strip().lower()
                if confirmar_envio == 's':
                    for convidado in evento['convidados']:
                        print(f"Enviando convite para {convidado['nome']} ({convidado['email']})...")
                        # Simulação de envio de email
                        print(f"Convite enviado para {convidado['email']}")
                    print("\033[1;32mTodos os convites foram enviados com sucesso!\033[m")
                else:
                    print("\033[1;34mEnvio de convites cancelado.\033[m")
            else:
                print("\033[1;31mNenhum convidado cadastrado para este evento.\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def registrar_feedback(self, email):
        self.visualizar_eventos(email)
        evento_id = int(input("Digite o ID do evento para o qual deseja registrar feedback: "))

        if evento_id in self.usuarios[email]['eventos']:
            evento = self.usuarios[email]['eventos'][evento_id]
            orcamentos_aceitos = [orc for orc in evento['orcamentos'] if
                                  orc['status'] == 'Aceito' and datetime.now() > evento["data_evento"]]

            if not orcamentos_aceitos:
                print("\033[1;31mNenhum orçamento aceito encontrado ou o evento ainda não ocorreu.\033[m")
                return

            print("\033[1;34mOrçamentos Aceitos:\033[m")
            for i, orc in enumerate(orcamentos_aceitos):
                print(f"{i + 1}. Orçamento ID: {orc['id']}")
                print(f"   Serviços: {', '.join(orc['servicos'])}")
                print(f"   Valor Planejado: R$ {orc['valor_planejado']}")
                print(f"   Fornecedor: {orc['fornecedor']}")
                if "rating" in orc:
                    print(f"   Avaliação: {orc['rating']}/5")
                if "comentario" in orc:
                    print(f"   Comentário: {orc['comentario']}")

            escolha = int(input("Digite o número do orçamento que deseja avaliar: ").strip())
            if 1 <= escolha <= len(orcamentos_aceitos):
                orcamento_selecionado = orcamentos_aceitos[escolha - 1]

                rating = int(input("Avalie o serviço de 0 a 5: ").strip())
                comentario = input("Escreva um comentário sobre o serviço: ").strip()

                feedback = {
                    "rating": rating,
                    "comentario": comentario
                }

                orcamento_selecionado['rating'] = rating
                orcamento_selecionado['comentario'] = comentario
                evento['feedbacks'].append(feedback)

                self.salvar_dados()
                print("\033[1;32mFeedback registrado com sucesso!\033[m")
            else:
                print("\033[1;31mOpção inválida.\033[m")
        else:
            print("\033[1;31mID do evento não encontrado.\033[m")

    def alterar_dados(self, email):
        usuario = self.usuarios.get(email)
        if usuario:
            print("\033[1;34mQual dado você gostaria de alterar?\033[m")
            print("1. Nome/Razão Social")
            print("2. Telefone")
            print("3. Logradouro")
            print("4. CEP")
            print("5. Senha")
            print("6. Cancelar")
            escolha = input("Digite o número correspondente à opção: ")

            if escolha == '1':
                novo_nome = input("Digite o novo nome/razão social: ").strip()
                usuario['nome'] = novo_nome
                self.salvar_dados()
                print("\033[1;32mNome/razão social alterado com sucesso!\033[m")
            elif escolha == '2':
                while True:
                    novo_telefone = input("Digite o novo telefone (com DDD): ").strip()
                    if self.validar_telefone(novo_telefone):
                        usuario['telefone'] = novo_telefone
                        self.salvar_dados()
                        print("\033[1;32mTelefone alterado com sucesso!\033[m")
                        break
                    else:
                        print(
                            "\033[1;31mNúmero de telefone inválido. Por favor, insira um número com DDD seguido de 8 ou 9 dígitos.\033[m")
            elif escolha == '3':
                novo_logradouro = input("Digite o novo logradouro: ").strip()
                usuario['logradouro'] = novo_logradouro
                self.salvar_dados()
                print("\033[1;32mLogradouro alterado com sucesso!\033[m")
            elif escolha == '4':
                while True:
                    novo_cep = input("Digite o novo CEP: ").strip()
                    if self.validar_cep(novo_cep):
                        usuario['cep'] = novo_cep
                        self.salvar_dados()
                        print("\033[1;32mCEP alterado com sucesso!\033[m")
                        break
                    else:
                        print("\033[1;31mCEP inválido. Por favor, digite um CEP válido.\033[m")
            elif escolha == '5':
                nova_senha = self.criar_senha()
                usuario['senha'] = nova_senha
                self.salvar_dados()
                print("\033[1;32mSenha alterada com sucesso!\033[m")
            elif escolha == '6':
                print("\033[1;34mAlteração cancelada.\033[m")
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")
        else:
            print("\033[1;31mUsuário não encontrado.\033[m")

    def cancelar_conta(self, email):
        confirmacao = input("Tem certeza de que deseja cancelar sua conta? (s/n): ").strip().lower()
        if confirmacao == 's':
            del self.usuarios[email]
            self.salvar_dados()
            print("\033[1;32mConta cancelada com sucesso.\033[m")
            return True
        else:
            print("\033[1;34mOperação cancelada.\033[m")
            return False

    def visualizar_orcamentos_disponiveis(self, email):
        for email_cliente, dados_usuario in self.usuarios.items():
            for evento_id, evento in dados_usuario.get('eventos', {}).items():
                print(f"\033[1;34mEvento ID: {evento_id}\033[m")
                print(f"Detalhes do evento: {evento['detalhes_evento']}")
                print(f"Endereço do evento: {evento['endereco_evento']}")
                print(f"Data do evento: {evento['data_evento'].strftime('%d/%m/%Y')}")
                print(f"Hora do evento: {evento.get('hora_evento', 'Não especificada')}")
                print("Orçamentos disponíveis:")
                for orcamento in evento['orcamentos']:
                    if orcamento['status'] == 'Pendente' and not orcamento['fornecedor']:
                        print(f"  Orçamento ID: {orcamento['id']}")
                        print(f"  Serviços: {', '.join(orcamento['servicos'])}")
                        print(f"  Detalhes Adicionais: {orcamento['detalhes_adicionais']}")
                        print(f"  Valor Planejado: R$ {orcamento['valor_planejado']}")
                        if "rating" in orcamento:
                            print(f"  Avaliação: {orcamento['rating']}/5")
                        aceitar = input(f"Deseja aceitar este orçamento? (s/n): ").strip().lower()
                        if aceitar == 's':
                            orcamento['status'] = 'Aceito'
                            orcamento['fornecedor'] = self.usuarios[email]['nome']
                            orcamento['email_cliente'] = email_cliente
                            orcamento['telefone_cliente'] = dados_usuario['telefone']
                            self.salvar_dados()
                            print("\033[1;32mOrçamento aceito com sucesso!\033[m")

    def visualizar_orcamentos_aceitos(self, email):
        print("\033[1;34mOrçamentos Aceitos:\033[m")
        for email_cliente, dados_usuario in self.usuarios.items():
            for evento_id, evento in dados_usuario.get('eventos', {}).items():
                for orcamento in evento['orcamentos']:
                    if orcamento['status'] == 'Aceito' and orcamento['fornecedor'] == self.usuarios[email]['nome']:
                        print(f"ID do Evento: {evento_id}")
                        print(f"  Detalhes do evento: {evento['detalhes_evento']}")
                        print(f"  Data do evento: {evento['data_evento']}")
                        print(f"  Orçamento Aceito: Valor: R$ {orcamento['valor_planejado']}")
                        print(f"  Serviços: {', '.join(orcamento['servicos'])}")
                        print(f"  Detalhes Adicionais: {orcamento['detalhes_adicionais']}")
                        print(f"  Email do Cliente: {orcamento['email_cliente']}")
                        print(f"  Telefone do Cliente: {orcamento['telefone_cliente']}")
                        if "rating" in orcamento:
                            print(f"  Avaliação: {orcamento['rating']}/5")
                        if "comentario" in orcamento:
                            print(f"  Comentário: {orcamento['comentario']}")

    def atualizar_preferencias_notificacao(self, email):
        print("\033[1;34mEscolha a preferência de notificação:\033[m")
        print("1. Email")
        print("2. SMS")
        print("3. Não receber notificações")
        escolha = input("Digite uma opção (1-3): ")
        if escolha == '1':
            self.usuarios[email]['preferencias_notificacao'] = "Email"
            self.salvar_dados()
            print("Você escolheu receber atualizações por Email.")
        elif escolha == '2':
            self.usuarios[email]['preferencias_notificacao'] = "SMS"
            self.salvar_dados()
            print("Você escolheu receber atualizações por SMS.")
        elif escolha == '3':
            self.usuarios[email]['preferencias_notificacao'] = "Não receber notificações"
            self.salvar_dados()
            print("Você não receberá notificações de atualizações.")
        else:
            print("Opção inválida. Nenhuma mudança foi feita em suas preferências.")

    def menu_cliente(self, email):
        while True:
            print("\n\033[1;34mMenu do Cliente:\033[m")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Eventos")
            print("4. Orçamentos")
            print("5. Convidados")
            print("6. Feedback")
            print("7. Atualizar Preferências de Notificação")
            print("8. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.alterar_dados(email)
            elif escolha == '2':
                if self.cancelar_conta(email):
                    break
            elif escolha == '3':
                self.menu_eventos_cliente(email)
            elif escolha == '4':
                self.menu_orcamentos_cliente(email)
            elif escolha == '5':
                self.menu_convidados_cliente(email)
            elif escolha == '6':
                self.registrar_feedback(email)
            elif escolha == '7':
                self.atualizar_preferencias_notificacao(email)
            elif escolha == '8':
                print("\033[1;34mVocê saiu do sistema.\033[m")
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

    def menu_eventos_cliente(self, email):
        while True:
            print("\n\033[1;34mMenu de Eventos:\033[m")
            print("1. Cadastrar Evento")
            print("2. Modificar Evento")
            print("3. Cancelar Evento")
            print("4. Visualizar Eventos")
            print("5. Voltar")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.cadastrar_evento(email)
            elif escolha == '2':
                self.modificar_evento(email)
            elif escolha == '3':
                self.cancelar_evento(email)
            elif escolha == '4':
                self.visualizar_eventos(email)
            elif escolha == '5':
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

    def menu_orcamentos_cliente(self, email):
        while True:
            print("\n\033[1;34mMenu de Orçamentos:\033[m")
            print("1. Solicitar Orçamento")
            print("2. Modificar Orçamento")
            print("3. Cancelar Orçamento")
            print("4. Visualizar Orçamentos")
            print("5. Voltar")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.solicitar_orcamento(email)
            elif escolha == '2':
                self.modificar_orcamento(email)
            elif escolha == '3':
                self.cancelar_orcamento(email)
            elif escolha == '4':
                self.visualizar_eventos(email)
            elif escolha == '5':
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

    def menu_convidados_cliente(self, email):
        while True:
            print("\n\033[1;34mMenu de Convidados:\033[m")
            print("1. Cadastrar Convidados")
            print("2. Enviar Convites")
            print("3. Voltar")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.cadastrar_convidados(email)
            elif escolha == '2':
                self.enviar_convites(email)
            elif escolha == '3':
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")

    def menu_fornecedor(self, email):
        while True:
            print("\n\033[1;34mMenu do Fornecedor:\033[m")
            print("1. Alterar Dados")
            print("2. Cancelar Conta")
            print("3. Visualizar e Aceitar Propostas de Orçamento")
            print("4. Meus Orçamentos Aceitos")
            print("5. Feedback")
            print("6. Atualizar Preferências de Notificação")
            print("7. Sair")
            escolha = input("Escolha uma opção: ")

            if escolha == '1':
                self.alterar_dados(email)
            elif escolha == '2':
                if self.cancelar_conta(email):
                    break
            elif escolha == '3':
                self.visualizar_orcamentos_disponiveis(email)
            elif escolha == '4':
                self.visualizar_orcamentos_aceitos(email)
            elif escolha == '5':
                self.registrar_feedback(email)
            elif escolha == '6':
                self.atualizar_preferencias_notificacao(email)
            elif escolha == '7':
                print("\033[1;34mVocê saiu do sistema.\033[m")
                break
            else:
                print("\033[1;31mOpção inválida. Por favor, escolha uma opção válida.\033[m")


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
