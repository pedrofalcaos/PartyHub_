def convites_eventos(self, email):
        eventos = self.usuarios[email]['eventos']
        if not eventos:
            print("\033[1;31mVocê não tem eventos cadastrados.\033[m")
            return
        
        print("\n\033[1;34Dados do Evento Cadastrado:\033[m")
        for evento_id, evento in eventos.items():
            print(f"\n\033[1;33mID do Evento: {evento_id}\033[m")
            print(f"\033[1;36mEndereço do Evento: {evento['endereco_evento']}\033[m")
            print(f"\033[1;36mData do Evento: {evento['data_evento'].strftime('%d/%m/%Y')}\033[m")
        
        print("\n\033[Olá! Farei um evento no dia {data_evento} e gostaria da sua presença. Endereço {endereco_evento}.\033[m")

        print("\n\033[1;34Confirma Convite?:\033[m")
        print("1. Sim")
        print("2. Não")
        escolha = input("Escolha uma opção (1-2): ")

        if escolha == '1':
            print("Evento Confirmado com Sucesso!")
        else:
            print("Retorne ao Cadastro de Eventos!")
        return


