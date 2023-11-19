import foosball_alunos


"""
Função que recebe o nome de um ficheiro contendo um replay, e que deverá
retornar um dicionário com as seguintes chaves:
bola - lista contendo tuplos com as coordenadas xx e yy da bola
jogador_vermelho - lista contendo tuplos com as coordenadas xx e yy da do jogador\_vermelho
jogador_azul - lista contendo tuplos com as coordenadas xx e yy da do jogador\_azul
"""


def le_replay(nome_ficheiro):
    replay_data = {"bola": [], "jogador_vermelho": [], "jogador_azul": []}

    try:
        with open(nome_ficheiro, "r") as file:
            for linha in file:
                partes = linha.split()

                if len(partes) == 3:
                    # obter as coordenadas e a cor do objeto
                    x, y, cor = map(float, partes)

                    # adicionar as coordenadas ao dicionário apropriado
                    if cor == 0:
                        replay_data["bola"].append((x, y))
                    elif cor == 1:
                        replay_data["jogador_vermelho"].append((x, y))
                    elif cor == 2:
                        replay_data["jogador_azul"].append((x, y))

    except FileNotFoundError:
        print(f"Arquivo não encontrado: {nome_ficheiro}")

    return replay_data

    pass


def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    replay = le_replay("replay_jogo_jv_2_ja.txt")
    for i in range(len(replay["bola"])):
        estado_jogo["janela"].update()
        estado_jogo["jogador_vermelho"].setpos(replay["jogador_vermelho"][i])
        estado_jogo["jogador_azul"].setpos(replay["jogador_azul"][i])
        estado_jogo["bola"]["objecto"].setpos(replay["bola"][i])
    estado_jogo["janela"].exitonclick()


if __name__ == "__main__":
    main()
