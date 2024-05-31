# Inicialização da lista de notas de NPS
notas_nps = []

# Inicialização da contagem de negócios fechados
negocios_fechados = 0

# Solicita ao usuário para inserir uma nota de NPS
try:
    print("Olá, tudo bem? Gostaríamos de saber o que você achou dos nossos produtos/serviços.")
    nota = int(input("Digite uma nota de 0-5 que representa a sua satisfação: ")).strip()
    feedback = input("Deixe seu comentário: ").strip()
    if 0 <= nota <= 5:
        notas_nps.append(nota)
        negocios_fechados += 1  # Incrementa um negócio fechado a cada nota recebida

        # Classificação dos respondentes
        promotores = len([nota for nota in notas_nps if nota >= 4])
        neutros = len([nota for nota in notas_nps if 2 <= nota <= 3])
        detratores = len([nota for nota in notas_nps if nota <= 1])

        # Cálculo das porcentagens
        total_respondentes = len(notas_nps)
        percentual_promotores = (promotores / total_respondentes) * 100
        percentual_detratores = (detratores / total_respondentes) * 100

        # Cálculo do NPS
        nps = percentual_promotores - percentual_detratores

        # Cálculo da média das notas
        media_nps = sum(notas_nps) / total_respondentes if total_respondentes > 0 else 0

        print(f"\nA média das notas do NPS é: {media_nps:.2f}")
        print(f"O NPS é: {nps:.2f}")
        print(f"O número de negócios fechados é: {negocios_fechados}")

    else:
        print("Por favor, digite uma nota válida entre 0 e 5.")
except ValueError:
    print("Entrada inválida. Por favor, digite um número entre 0 e 5.")