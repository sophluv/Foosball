import turtle as t
import functools
import random

LARGURA_JANELA = 1024
ALTURA_JANELA = 600
DEFAULT_TURTLE_SIZE = 40
DEFAULT_TURTLE_SCALE = 3
RAIO_JOGADOR = DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
RAIO_BOLA = DEFAULT_TURTLE_SIZE / 2
PIXEIS_MOVIMENTO = 90
LADO_MAIOR_AREA = ALTURA_JANELA / 3
LADO_MENOR_AREA = 50
RAIO_MEIO_CAMPO = LADO_MAIOR_AREA / 4
START_POS_BALIZAS = ALTURA_JANELA / 4
BOLA_START_POS = (5, 5)


def jogador_cima(estado_jogo, jogador):
    x, y = estado_jogo[jogador].position()
    y += PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def jogador_baixo(estado_jogo, jogador):
    x, y = estado_jogo[jogador].position()
    y -= PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def jogador_direita(estado_jogo, jogador):
    x, y = estado_jogo[jogador].position()
    x += PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def jogador_esquerda(estado_jogo, jogador):
    x, y = estado_jogo[jogador].position()
    x -= PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def desenha_linhas_campo():
    """Função responsável por desenhar as linhas do campo,
    nomeadamente a linha de meio campo, o círculo central, e as balizas."""
    t.ht()
    t.pencolor("WHITE")
    t.pensize(10)

    t.pu()
    t.goto(0, ALTURA_JANELA / 2)
    t.pd()
    t.seth(270)
    t.fd(ALTURA_JANELA)

    t.pu()
    t.goto(0, 0 - RAIO_MEIO_CAMPO)
    t.pd()
    t.seth(0)
    t.circle(RAIO_MEIO_CAMPO * 2)

    t.pu()
    t.goto(LARGURA_JANELA / 2, START_POS_BALIZAS)
    t.pd()
    t.seth(180)

    for i in range(2):
        t.fd(LADO_MENOR_AREA)
        t.left(90)
        t.fd(LADO_MAIOR_AREA)
        t.left(90)

    t.pu()
    t.goto(-LARGURA_JANELA / 2, START_POS_BALIZAS)
    t.pd()
    t.seth(0)

    for i in range(2):
        t.fd(LADO_MENOR_AREA)
        t.right(90)
        t.fd(LADO_MAIOR_AREA)
        t.right(90)
    t.ht()
    pass


def criar_bola():
    bola = t.Turtle()
    bola.shape("circle")
    bola.color("black")
    bola.shapesize(RAIO_BOLA / 10)
    bola.penup()
    bola.goto(BOLA_START_POS)

    direcao_x = random.choice([-1, 1])
    direcao_y = random.choice([-1, 1])

    posicao_anterior = None

    return {
        "bola": bola,
        "direcao_x": direcao_x,
        "direcao_y": direcao_y,
        "posicao_anterior": posicao_anterior,
    }


def cria_jogador(x_pos_inicial, y_pos_inicial, cor):
    jogador = t.Turtle()
    jogador.shape("circle")
    jogador.color(cor)
    jogador.shapesize(
        stretch_wid=DEFAULT_TURTLE_SCALE, stretch_len=DEFAULT_TURTLE_SCALE
    )
    jogador.penup()
    jogador.goto(x_pos_inicial, y_pos_inicial)

    return jogador


def init_state():
    estado_jogo = {}
    estado_jogo["bola"] = None
    estado_jogo["jogador_vermelho"] = None
    estado_jogo["jogador_azul"] = None
    estado_jogo["var"] = {
        "bola": [],
        "jogador_vermelho": [],
        "jogador_azul": [],
    }
    estado_jogo["pontuacao_jogador_vermelho"] = 0
    estado_jogo["pontuacao_jogador_azul"] = 0
    return estado_jogo


def cria_janela():
    # create a window and declare a variable called window and call the screen()
    janela = t.Screen()
    janela.title("Foosball Game")
    janela.bgcolor("green")
    janela.setup(width=LARGURA_JANELA, height=ALTURA_JANELA)
    janela.tracer(0)
    return janela


def cria_quadro_resultados():
    # Code for creating pen for scorecard update
    quadro = t.Turtle()
    quadro.speed(0)
    quadro.color("Blue")
    quadro.penup()
    quadro.hideturtle()
    quadro.goto(0, 260)
    quadro.write(
        "Player A: 0\t\tPlayer B: 0 ", align="center", font=("Monaco", 24, "normal")
    )
    return quadro


def terminar_jogo(estado_jogo):
    print("Adeus")

    estado_jogo["total_jogos"] += 1

    resultado_jogo = f"{estado_jogo['pontuacao_jogador_vermelho']} - {estado_jogo['pontuacao_jogador_azul']}"

    # Atualizar ou criar o arquivo de histórico de resultados
    atualizar_resultados(estado_jogo["total_jogos"], resultado_jogo)

    # Fechar a janela do Turtle
    estado_jogo["janela"].bye()


def atualizar_resultados(total_jogos, resultado_jogo):
    # Nome do arquivo de histórico de resultados
    arquivo_resultados = "historico_resultados.txt"

    # Verificar se o arquivo existe
    try:
        with open(arquivo_resultados, "r") as file:
            # Leia as linhas existentes para verificar se o cabeçalho já foi escrito
            linhas = file.readlines()
            if not linhas or not linhas[0].startswith("NJogo"):
                # Se não existir cabeçalho, adicione-o
                linhas.insert(0, "NJogo,JogadorVermelho,JogadorAzul\n")
    except FileNotFoundError:
        # Se o arquivo não existir, crie-o e adicione o cabeçalho
        linhas = ["NJogo,JogadorVermelho,JogadorAzul\n"]

    with open(arquivo_resultados, "a") as file:
        file.write(
            f"{total_jogos},{resultado_jogo.split(' - ')[0]},{resultado_jogo.split(' - ')[1]}\n"
        )


def setup(estado_jogo, jogar):
    janela = cria_janela()
    janela.listen()
    if jogar:
        janela.onkeypress(
            functools.partial(jogador_cima, estado_jogo, "jogador_vermelho"), "w"
        )
        janela.onkeypress(
            functools.partial(jogador_baixo, estado_jogo, "jogador_vermelho"), "s"
        )
        janela.onkeypress(
            functools.partial(jogador_esquerda, estado_jogo, "jogador_vermelho"), "a"
        )
        janela.onkeypress(
            functools.partial(jogador_direita, estado_jogo, "jogador_vermelho"), "d"
        )
        janela.onkeypress(
            functools.partial(jogador_cima, estado_jogo, "jogador_azul"), "Up"
        )
        janela.onkeypress(
            functools.partial(jogador_baixo, estado_jogo, "jogador_azul"), "Down"
        )
        janela.onkeypress(
            functools.partial(jogador_esquerda, estado_jogo, "jogador_azul"), "Left"
        )
        janela.onkeypress(
            functools.partial(jogador_direita, estado_jogo, "jogador_azul"), "Right"
        )
        janela.onkeypress(functools.partial(terminar_jogo, estado_jogo), "Escape")
        quadro = cria_quadro_resultados()
        estado_jogo["quadro"] = quadro
    desenha_linhas_campo()
    bola = criar_bola()
    jogador_vermelho = cria_jogador(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "red")
    jogador_azul = cria_jogador(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0, "blue")
    estado_jogo["total_jogos"] = 0
    estado_jogo["janela"] = janela
    estado_jogo["bola"] = bola
    estado_jogo["jogador_vermelho"] = jogador_vermelho
    estado_jogo["jogador_azul"] = jogador_azul


def update(estado_jogo):
    estado_jogo["quadro"].clear()
    estado_jogo["quadro"].write(
        "Player A: {}\t\tPlayer B: {} ".format(
            estado_jogo["pontuacao_jogador_vermelho"],
            estado_jogo["pontuacao_jogador_azul"],
        ),
        align="center",
        font=("Monaco", 24, "normal"),
    )


def movimenta_bola(estado_jogo):
    bola = estado_jogo["bola"]

    if bola is None or "bola" not in bola or not isinstance(bola["bola"], t.Turtle):
        print("Erro: Bola não está definida corretamente.")
        return

    posicao_atual = bola["bola"].position()

    direcao_x = bola["direcao_x"]
    direcao_y = bola["direcao_y"]

    nova_posicao_x = posicao_atual[0] + direcao_x
    nova_posicao_y = posicao_atual[1] + direcao_y

    # Atualizar a posição da bola
    bola["bola"].goto(nova_posicao_x, nova_posicao_y)
    bola["posicao_anterior"] = posicao_atual

    # Verificar colisões após a atualização da posição
    verifica_toque_jogador_azul(estado_jogo)
    verifica_toque_jogador_vermelho(estado_jogo)
    verifica_colisoes_ambiente(estado_jogo)
    verifica_golos(estado_jogo)


def verifica_colisoes_ambiente(estado_jogo):
    bola = estado_jogo["bola"]

    if bola is None:
        print("Erro: Bola não está definida.")
        return

    posicao_atual = bola["bola"].position()

    direcao_x = bola["direcao_x"]
    direcao_y = bola["direcao_y"]

    # Limites da área de jogo
    LIMITE_SUPERIOR = ALTURA_JANELA / 2
    LIMITE_INFERIOR = -ALTURA_JANELA / 2
    LIMITE_DIREITO = LARGURA_JANELA / 2
    LIMITE_ESQUERDO = -LARGURA_JANELA / 2

    # Raio da bola
    RAIO_BOLA = 10  # Adapte conforme necessário

    # Verificar colisões com os limites do ambiente
    if (
        posicao_atual[1] + RAIO_BOLA >= LIMITE_SUPERIOR
        or posicao_atual[1] - RAIO_BOLA <= LIMITE_INFERIOR
    ):
        # Colisão com o limite superior ou inferior, inverter a direção vertical (y)
        bola["direcao_y"] *= -1

    if (
        posicao_atual[0] + RAIO_BOLA >= LIMITE_DIREITO
        or posicao_atual[0] - RAIO_BOLA <= LIMITE_ESQUERDO
    ):
        # Colisão com o limite direito ou esquerdo, inverter a direção horizontal (x)
        bola["direcao_x"] *= -1


def verifica_golo_jogador_vermelho(estado_jogo):
    # Constantes para as coordenadas da linha de golo da baliza do jogador vermelho
    LINHA_GOLO_JOGADOR_VERMELHO = -ALTURA_JANELA / 2

    # Obter informações sobre a bola do estado do jogo
    bola = estado_jogo["bola"]

    if bola is None:
        print("Erro: Bola não está definida.")
        return

    # Obter a posição anterior da bola
    posicao_anterior = bola.get("posicao_anterior")  # Use get for safety

    if posicao_anterior is None:
        print("Erro: A posição anterior da bola não está definida. vermelho")
        return

    # Verificar se a bola cruzou a linha de golo da baliza do jogador vermelho
    if posicao_anterior[1] >= LINHA_GOLO_JOGADOR_VERMELHO > bola["posicao_anterior"][1]:
        # Atualizar a pontuação do jogador vermelho
        estado_jogo["pontuacao_jogador_vermelho"] += 1

        # Criar um arquivo de replay para análise pelo VAR
        criar_arquivo_replay(estado_jogo)

        # Reiniciar o jogo com a bola ao centro
        reiniciar_jogo(estado_jogo)


def verifica_golo_jogador_azul(estado_jogo):
    # Constantes para as coordenadas da linha de golo da baliza do jogador azul
    LINHA_GOLO_JOGADOR_AZUL = ALTURA_JANELA / 2

    # Obter informações sobre a bola do estado do jogo
    bola = estado_jogo["bola"]

    if bola is None:
        print("Erro: Bola não está definida.")
        return

    # Obter a posição anterior da bola
    posicao_anterior = bola.get("posicao_anterior")  # Use get for safety

    if posicao_anterior is None:
        print("Erro: A posição anterior da bola não está definida. azul")
        return

    # Verificar se a bola cruzou a linha de golo da baliza do jogador azul
    if posicao_anterior[1] <= LINHA_GOLO_JOGADOR_AZUL < bola["posicao_anterior"][1]:
        # Atualizar a pontuação do jogador azul
        estado_jogo["pontuacao_jogador_azul"] += 1

        # Criar um arquivo de replay para análise pelo VAR
        criar_arquivo_replay(estado_jogo)

        # Reiniciar o jogo com a bola ao centro
        reiniciar_jogo(estado_jogo)


def criar_arquivo_replay(estado_jogo):
    # Obter informações sobre a bola, jogador vermelho e jogador azul do estado do jogo
    bola = estado_jogo["bola"]
    jogador_vermelho = estado_jogo["jogador_vermelho"]
    jogador_azul = estado_jogo["jogador_azul"]

    # Criar o nome do arquivo de replay
    nome_arquivo = f"replay_golo_jv_{estado_jogo['pontuacao_jogador_vermelho']}_ja_{estado_jogo['pontuacao_jogador_azul']}.txt"

    # Escrever as coordenadas no arquivo
    with open(nome_arquivo, "w") as file:
        file.write(f"{bola[0]},{bola[1]}\n")
        file.write(f"{jogador_vermelho[0]},{jogador_vermelho[1]}\n")
        file.write(f"{jogador_azul[0]},{jogador_azul[1]}\n")


def reiniciar_jogo(estado_jogo):
    # Configurar a bola de volta ao centro
    estado_jogo["bola"] = (0, 0)

    # Configurar as direções da bola para valores iniciais (pode ser aleatório)
    estado_jogo["direcao_x"] = 1
    estado_jogo["direcao_y"] = 1

    # Atualizar as coordenadas dos jogadores para suas posições iniciais (pode ser aleatório)
    estado_jogo["jogador_vermelho"] = (-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)
    estado_jogo["jogador_azul"] = (((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def verifica_toque_jogador_azul(estado_jogo):
    # Obter informações sobre a bola e jogador azul do estado do jogo
    bola = estado_jogo.get("bola")

    if bola is None or "bola" not in bola or not isinstance(bola["bola"], t.Turtle):
        print("Erro: Bola não está definida corretamente.")
        return

    jogador_azul = estado_jogo.get("jogador_azul")

    if jogador_azul is None or not isinstance(jogador_azul, t.Turtle):
        print("Erro: Jogador azul não está definido corretamente.")
        return

    # Obter as coordenadas da bola e do jogador azul
    posicao_bola = bola["bola"].position()
    posicao_jogador_azul = jogador_azul.position()

    # Calcular as coordenadas da área de toque do jogador azul
    area_toque_x_min = posicao_jogador_azul[0] - RAIO_JOGADOR
    area_toque_x_max = posicao_jogador_azul[0] + RAIO_JOGADOR
    area_toque_y_min = posicao_jogador_azul[1] - RAIO_JOGADOR
    area_toque_y_max = posicao_jogador_azul[1] + RAIO_JOGADOR

    # Verificar se a bola está dentro da área de toque do jogador azul
    if (
        area_toque_x_min <= posicao_bola[0] <= area_toque_x_max
        and area_toque_y_min <= posicao_bola[1] <= area_toque_y_max
    ):
        # Inverter a direção da bola ao ser tocada pelo jogador azul
        estado_jogo["bola"]["direcao_x"] *= -1
        estado_jogo["bola"]["direcao_y"] *= -1


def verifica_toque_jogador_vermelho(estado_jogo):
    # Obter informações sobre a bola e jogador vermelho do estado do jogo
    bola = estado_jogo["bola"]

    if bola is None or "bola" not in bola or not isinstance(bola["bola"], t.Turtle):
        print("Erro: Bola não está definida corretamente.")
        return

    jogador_vermelho = estado_jogo.get("jogador_vermelho")

    if jogador_vermelho is None or not isinstance(jogador_vermelho, t.Turtle):
        print("Erro: Jogador vermelho não está definido corretamente.")
        return

    # Obter as coordenadas da bola e do jogador vermelho
    posicao_bola = bola["bola"].position()
    posicao_jogador_vermelho = jogador_vermelho.position()

    # Calcular as coordenadas da área de toque do jogador vermelho
    area_toque_x_min = posicao_jogador_vermelho[0] - RAIO_JOGADOR
    area_toque_x_max = posicao_jogador_vermelho[0] + RAIO_JOGADOR
    area_toque_y_min = posicao_jogador_vermelho[1] - RAIO_JOGADOR
    area_toque_y_max = posicao_jogador_vermelho[1] + RAIO_JOGADOR

    # Verificar se a bola está dentro da área de toque do jogador vermelho
    if (
        area_toque_x_min <= posicao_bola[0] <= area_toque_x_max
        and area_toque_y_min <= posicao_bola[1] <= area_toque_y_max
    ):
        # Inverter a direção da bola ao ser tocada pelo jogador vermelho
        estado_jogo["bola"]["direcao_x"] *= -1
        estado_jogo["bola"]["direcao_y"] *= -1


def guarda_posicoes_para_var(estado_jogo):
    estado_jogo["var"]["bola"].append(estado_jogo["bola"]["objecto"].pos())
    estado_jogo["var"]["jogador_vermelho"].append(estado_jogo["jogador_vermelho"].pos())
    estado_jogo["var"]["jogador_azul"].append(estado_jogo["jogador_azul"].pos())


def main():
    estado_jogo = init_state()
    setup(estado_jogo, True)
    while True:
        estado_jogo["janela"].update()
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo["jogador_vermelho"] is not None:
            print("a verificar az")
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo["jogador_azul"] is not None:
            print("a verificar ver")
            verifica_toque_jogador_vermelho(estado_jogo)
        movimenta_bola(estado_jogo)
        update(estado_jogo)  # Update the score display


if __name__ == "__main__":
    main()
