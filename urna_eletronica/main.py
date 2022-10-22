Frd = input("Voce quer fraudar (S/N)?\n")

fraude = True if Frd.lower() == 's' else False

def processaVoto():
    qtdVotosCandidato1 = 0
    qtdVotosCandidato2 = 0
    qtdVotosNulos = 0
    qtdVotosBrancos = 0
    eleitor = 1
    while eleitor <= 15:
        print(f"\nEleitor {eleitor}")
        voto = input("Digite seu voto para presidente: ")
        if voto == '13':
            print("Voce Votou no Lula\n")
            qtdVotosCandidato1 += 1
        elif  voto == '22':
            print("Voce Votou no Bolsonaro\n")
            qtdVotosCandidato2 += 1
        elif  voto.lower() == 'branco' or voto.lower() == 'b':
            print("Voce Votou em branco\n")
            qtdVotosBrancos += 1
        else:
            print("Seu voto é nulo\n")
            qtdVotosNulos += 1
        eleitor += 1
    return qtdVotosBrancos, qtdVotosCandidato1, qtdVotosCandidato2, qtdVotosNulos

def fraudaVoto(qtdVotosCandidato1, qtdVotosCandidato2):
    totalVotos = qtdVotosCandidato1+qtdVotosCandidato2
    qtdVotosCandidato1 = round(totalVotos*0.52)
    qtdVotosCandidato2 = round(totalVotos*0.48)
    if qtdVotosCandidato1 == qtdVotosCandidato2:
        qtdVotosCandidato1 += 1
        qtdVotosCandidato2 -= 1
    return qtdVotosCandidato1, qtdVotosCandidato2

if __name__ == '__main__':
    qtdVotosBrancos, qtdVotosCandidato1, qtdVotosCandidato2, qtdVotosNulos = processaVoto()
    if fraude:
        qtdVotosCandidato1, qtdVotosCandidato2 = fraudaVoto(qtdVotosCandidato1, qtdVotosCandidato2)

    print(f"""
          Resultado:
          
          Candidato Lula Final: {qtdVotosCandidato1}
          Candidato Bolsonaro Final: {qtdVotosCandidato2}
          Candidato Lula (%): {round((qtdVotosCandidato1/(qtdVotosCandidato1+qtdVotosCandidato2))*100,2)}%
          Candidato Bolsonaro (%): {round((qtdVotosCandidato2/(qtdVotosCandidato1+qtdVotosCandidato2))*100,2)}%
          Nulos: {qtdVotosNulos}
          Brancos: {qtdVotosBrancos}
          Total de votos contabilizados: {qtdVotosBrancos+qtdVotosCandidato1+qtdVotosCandidato2+qtdVotosNulos}
          """)
    