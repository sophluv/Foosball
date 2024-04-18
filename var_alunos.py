import foosball


def le_replay(nome_ficheiro):
    replay_data = {"bola": [], "jogador_vermelho": [], "jogador_azul": []}

    try:
        with open(nome_ficheiro, "r") as file:
            for i, linha in enumerate(file):
                partes = linha.strip().split(";")

                for j in range(len(partes)):
                    # verificar se existem coordenadas
                    if partes[j]:
                        coordenadas = tuple(
                            float(coord) for coord in partes[j].split(",")
                        )
                        # primeira linha
                        if i == 0:
                            replay_data["bola"].append(coordenadas)
                        # segunda linha
                        elif i == 1:
                            replay_data["jogador_vermelho"].append(coordenadas)
                        # terceira linha
                        elif i == 2:
                            replay_data["jogador_azul"].append(coordenadas)

    except FileNotFoundError:
        print(f"Ficheiro '{nome_ficheiro}' não encontrado!")

    return replay_data


def main():
    estado_jogo = foosball_alunos.init_state()
    foosball_alunos.setup(estado_jogo, False)
    estado_jogo["janela"].update()

    replay = le_replay("replay_golo_jv_0_ja_1.txt")

    for i in range(len(replay["bola"])):
        estado_jogo["jogador_vermelho"].setpos(replay["jogador_vermelho"][i])
        estado_jogo["jogador_azul"].setpos(replay["jogador_azul"][i])
        estado_jogo["bola"]["objeto"].setpos(replay["bola"][i])

        estado_jogo["janela"].update()
    estado_jogo["janela"].exitonclick()


if __name__ == "__main__":
    main()
