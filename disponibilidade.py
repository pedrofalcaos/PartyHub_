print("Fornecedores")
print("1 RR Festas")
print("2 Boleria imperial")
print("3 Lucas dos salgados")
print("4 Sair")

opc = int(input("Escolha o fornecedor que deseja?"))

match (opc):
    case 1:
        while True:
            print("RR Festas,disponibilidade todos os dias, exceto aos dias que os locais estiverem alugados")
            
            dia_disponivel = int(input("Qual dia em maio planeja alugar um espaço para sua festa?"))
            if (dia_disponivel == 1) or (dia_disponivel == 11) or (dia_disponivel == 12) or (dia_disponivel == 13) or (dia_disponivel == 17):  
                print("Dia indiponivel")
                opc_sn = (input("Deseja tentar remarcar outro dia ? (S/N)"))
                if opc_sn == 'N':
                    break
            else:
                print("Dia disponivel!")
                break
    
    case 2:
        while True:
            print("Boleria imperial,disponibilidade de terça á sabado")
            
            dia_disponivel = int(input("Qual dia em maio planeja alugar um espaço para sua festa?"))
            if (dia_disponivel == 5) or (dia_disponivel == 12) or (dia_disponivel == 19) or (dia_disponivel == 26) or (dia_disponivel == 6) or (dia_disponivel == 13) or (dia_disponivel == 20) or (dia_disponivel == 27):  
                print("Dia indiponivel")
                opc_sn = (input("Deseja tentar remarcar outro dia ? (S/N)"))
                if opc_sn == 'N':
                    break
            else:
                print("Dia disponivel!")
                break
    
    case 3: 
         while True:
            print(" Lucas dos salgados,disponibilidade de terça á sábado")
            
            dia_disponivel = int(input("Qual dia em maio planeja alugar um espaço para sua festa?"))
            if (dia_disponivel == 5) or (dia_disponivel == 12) or (dia_disponivel == 19) or (dia_disponivel == 26) or (dia_disponivel == 6) or (dia_disponivel == 13) or (dia_disponivel == 20) or (dia_disponivel == 27):  
                print("Dia indiponivel")
                opc_sn = (input("Deseja tentar remarcar outro dia ? (S/N)"))
                if opc_sn == 'N':
                    break
            else:
                print("Dia disponivel!")
                break 
    case 4:
        if opc == 4:
            print("Programa finalizado")
                
            
    

            

