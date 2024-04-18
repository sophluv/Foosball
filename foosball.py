import turtle as t
import functools
import random
import time
import math


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
    x, y = estado_jogo[jogador].pos()
    y += PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def jogador_baixo(estado_jogo, jogador):
    x, y = estado_jogo[jogador].pos()
    y -= PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def jogador_direita(estado_jogo, jogador):
    x, y = estado_jogo[jogador].pos()
    x += PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def jogador_esquerda(estado_jogo, jogador):
    x, y = estado_jogo[jogador].pos()
    x -= PIXEIS_MOVIMENTO
    estado_jogo[jogador].goto(x, y)


def desenha_linhas_campo():
    t.ht()
    t.pencolor("WHITE")
    t.pensize(10)

    t.pu()
    t.goto(0, ALTURA_JANELA / 2)
    t.pd()
    t.seth(270)
    t.fd(ALTURA_JANELA)

    t.pu()
    t.goto(0, 0 - RAIO_MEIO_CAMPO - DEFAULT_TURTLE_SIZE)
    t.pd()
    t.seth(0)
    t.circle(RAIO_MEIO_CAMPO * 2)

    t.pu()
    t.goto(LARGURA_JANELA / 2, START_POS_BALIZAS - DEFAULT_TURTLE_SIZE)
    t.pd()
    t.seth(180)

    for i in range(2):
        t.fd(LADO_MENOR_AREA)
        t.left(90)
        t.fd(LADO_MAIOR_AREA)
        t.left(90)

    t.pu()
    t.goto(-LARGURA_JANELA / 2, START_POS_BALIZAS - DEFAULT_TURTLE_SIZE)
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
    bola.shapesize(RAIO_BOLA / 20)
    bola.penup()
    bola.goto(BOLA_START_POS)

    # generar um angulo entre 0 e 360
    angulo = random.randrange(360)
    # converter para radianos
    direcao_x = math.cos(math.radians(angulo))
    direcao_y = math.sin(math.radians(angulo))

    return {"objeto": bola, "direcao_x": direcao_x, "direcao_y": direcao_y}


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
    janela = t.Screen()
    janela.title("Foosball Game")
    janela.bgcolor("green")
    janela.setup(width=LARGURA_JANELA, height=ALTURA_JANELA)
    janela.tracer(0)
    return janela


def cria_quadro_resultados():
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
    print("\n👋")

    resultado_jogo = f"{estado_jogo['pontuacao_jogador_vermelho']} - {estado_jogo['pontuacao_jogador_azul']}"
    atualizar_resultados(resultado_jogo)

    estado_jogo["janela"].bye()


def atualizar_resultados(resultado_jogo):
    arquivo_resultados = "historico_resultados.txt"
    # ver se o ficheiro existe, se não, cria um
    try:
        with open(arquivo_resultados, "r") as file:
            linhas = file.readlines()
    except FileNotFoundError:
        with open(arquivo_resultados, "w") as file:
            file.write("NJogo,JogadorVermelho,JogadorAzul\n")
        linhas = []

    # número total de jogos
    total_jogos = len(linhas)

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


def verifica_colisoes_ambiente(estado_jogo):
    bola = estado_jogo["bola"]
    posicao_atual = bola["objeto"].pos()

    LIMITE_SUPERIOR = ALTURA_JANELA / 2
    LIMITE_INFERIOR = -ALTURA_JANELA / 2
    LIMITE_DIREITO = LARGURA_JANELA / 2
    LIMITE_ESQUERDO = -LARGURA_JANELA / 2

    RAIO_BOLA = 10

    if (
        posicao_atual[1] + RAIO_BOLA >= LIMITE_SUPERIOR
        or posicao_atual[1] - RAIO_BOLA <= LIMITE_INFERIOR
    ):
        estado_jogo["bola"]["direcao_y"] *= -1

    if (
        posicao_atual[0] + RAIO_BOLA >= LIMITE_DIREITO
        or posicao_atual[0] - RAIO_BOLA <= LIMITE_ESQUERDO
    ):
        estado_jogo["bola"]["direcao_x"] *= -1


def verifica_golo_jogador_vermelho(estado_jogo):
    bola = estado_jogo["bola"]
    posicao_bola = bola["objeto"].pos()

    if (
        LARGURA_JANELA / 2
        - LADO_MENOR_AREA
        + DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
        < posicao_bola[0]
        and -LADO_MAIOR_AREA / 2 + DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
        < posicao_bola[1]
        < LADO_MAIOR_AREA / 2 - DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
    ):
        estado_jogo["pontuacao_jogador_vermelho"] += 1
        print("GOLO VERMELHO")

        # realçar a vermelho a pontuação do jogador que marcou
        estado_jogo["quadro"].clear()
        estado_jogo["quadro"].color("red")
        estado_jogo["quadro"].goto(0, 260)
        estado_jogo["quadro"].write(
            "Player A: {}\t\t             ".format(
                estado_jogo["pontuacao_jogador_vermelho"]
            ),
            align="center",
            font=("Monaco", 24, "bold"),
        )
        estado_jogo["quadro"].color("blue")
        estado_jogo["quadro"].goto(0, 260)
        estado_jogo["quadro"].write(
            "            \t\tPlayer B: {} ".format(
                estado_jogo["pontuacao_jogador_azul"]
            ),
            align="center",
            font=("Monaco", 24, "normal"),
        )
        estado_jogo["janela"].update()

        time.sleep(1)

        criar_arquivo_replay(estado_jogo)
        reiniciar_jogo(estado_jogo)


def verifica_golo_jogador_azul(estado_jogo):
    bola = estado_jogo["bola"]
    posicao_bola = bola["objeto"].pos()

    if (
        posicao_bola[0]
        < -LARGURA_JANELA / 2
        + LADO_MENOR_AREA
        - DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
        and -LADO_MAIOR_AREA / 2 + DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
        < posicao_bola[1]
        < LADO_MAIOR_AREA / 2 - DEFAULT_TURTLE_SIZE / DEFAULT_TURTLE_SCALE
    ):
        estado_jogo["pontuacao_jogador_azul"] += 1
        print("GOLO AZUL")

        # realçar a vermelho a pontuação do jogador que marcou

        estado_jogo["quadro"].clear()
        estado_jogo["quadro"].color("blue")
        estado_jogo["quadro"].goto(0, 260)
        estado_jogo["quadro"].write(
            "Player A: {}\t\t             ".format(
                estado_jogo["pontuacao_jogador_vermelho"]
            ),
            align="center",
            font=("Monaco", 24, "normal"),
        )
        estado_jogo["quadro"].color("red")
        estado_jogo["quadro"].goto(0, 260)
        estado_jogo["quadro"].write(
            "            \t\tPlayer B: {} ".format(
                estado_jogo["pontuacao_jogador_azul"]
            ),
            align="center",
            font=("Monaco", 24, "bold"),
        )
        estado_jogo["janela"].update()
        time.sleep(1)

        criar_arquivo_replay(estado_jogo)
        reiniciar_jogo(estado_jogo)


def verifica_golos(estado_jogo):
    verifica_golo_jogador_vermelho(estado_jogo)
    verifica_golo_jogador_azul(estado_jogo)


def movimenta_bola(estado_jogo):
    bola = estado_jogo["bola"]
    posicao_atual = bola["objeto"].pos()

    nova_posicao_x = posicao_atual[0] + bola["direcao_x"] / 1.5
    nova_posicao_y = posicao_atual[1] + bola["direcao_y"] / 1.5

    bola["objeto"].setx(nova_posicao_x)
    bola["objeto"].sety(nova_posicao_y)

    guarda_posicoes_para_var(estado_jogo)


def criar_arquivo_replay(estado_jogo):
    total_golos_jogador_vermelho = estado_jogo["pontuacao_jogador_vermelho"]
    total_golos_jogador_azul = estado_jogo["pontuacao_jogador_azul"]

    nome_arquivo = f"replay_golo_jv_{total_golos_jogador_vermelho}_ja_{total_golos_jogador_azul}.txt"

    with open(nome_arquivo, "w") as file:
        for posicao in estado_jogo["var"]["bola"]:
            file.write(f"{posicao[0]:.3f},{posicao[1]:.3f};")
        file.write("\n")

        for posicao in estado_jogo["var"]["jogador_vermelho"]:
            file.write(f"{posicao[0]:.3f},{posicao[1]:.3f};")
        file.write("\n")

        for posicao in estado_jogo["var"]["jogador_azul"]:
            file.write(f"{posicao[0]:.3f},{posicao[1]:.3f};")
        file.write("\n")

    estado_jogo["var"]["bola"].clear()
    estado_jogo["var"]["jogador_vermelho"].clear()
    estado_jogo["var"]["jogador_azul"].clear()


def reiniciar_jogo(estado_jogo):
    bola = estado_jogo["bola"]
    bola["objeto"].goto(0, 0)

    angulo = random.randrange(360)

    estado_jogo["bola"]["direcao_x"] = math.cos(math.radians(angulo))
    estado_jogo["bola"]["direcao_y"] = math.sin(math.radians(angulo))

    jogador_azul = estado_jogo.get("jogador_azul")
    jogador_vermelho = estado_jogo.get("jogador_vermelho")

    jogador_vermelho.goto(-((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)
    jogador_azul.goto(((ALTURA_JANELA / 2) + LADO_MENOR_AREA), 0)

    time.sleep(1)
    estado_jogo["quadro"].color("blue")
    estado_jogo["janela"].update()
    update(estado_jogo)


def verifica_toque_jogador_azul(estado_jogo):
    bola = estado_jogo["bola"]
    jogador_azul = estado_jogo.get("jogador_azul")

    posicao_bola_x = bola["objeto"].xcor()
    posicao_bola_y = bola["objeto"].ycor()
    posicao_bola = bola["objeto"].pos()
    posicao_jogador_azul = jogador_azul.pos()

    area_toque_x_min = posicao_jogador_azul[0] - RAIO_JOGADOR * 2
    area_toque_x_max = posicao_jogador_azul[0] + RAIO_JOGADOR * 2
    area_toque_y_min = posicao_jogador_azul[1] - RAIO_JOGADOR * 2
    area_toque_y_max = posicao_jogador_azul[1] + RAIO_JOGADOR * 2

    if (
        area_toque_x_min <= posicao_bola_x <= area_toque_x_max
        and area_toque_y_min <= posicao_bola_y <= area_toque_y_max
    ):
        vetor_jogador = (
            posicao_bola[0] - posicao_jogador_azul[0],
            posicao_bola[1] - posicao_jogador_azul[1],
        )

        comprimento_vetor = math.sqrt(vetor_jogador[0] ** 2 + vetor_jogador[1] ** 2)
        vetor_jogador = (
            vetor_jogador[0] / comprimento_vetor,
            vetor_jogador[1] / comprimento_vetor,
        )
        # calcular produto escalar da superfície do jogador
        produto_escalar = vetor_jogador[0] * 0

        vetor_bola = (
            vetor_jogador[0] - 2 * produto_escalar * 0,
            vetor_jogador[1] - 2 * produto_escalar * 1,
        )

        estado_jogo["bola"]["direcao_x"] = vetor_bola[0]
        estado_jogo["bola"]["direcao_y"] = vetor_bola[1]


def verifica_toque_jogador_vermelho(estado_jogo):
    bola = estado_jogo["bola"]

    jogador_vermelho = estado_jogo.get("jogador_vermelho")

    posicao_bola = bola["objeto"].position()
    posicao_jogador_vermelho = jogador_vermelho.position()

    area_toque_x_min = posicao_jogador_vermelho[0] - RAIO_JOGADOR * 2
    area_toque_x_max = posicao_jogador_vermelho[0] + RAIO_JOGADOR * 2
    area_toque_y_min = posicao_jogador_vermelho[1] - RAIO_JOGADOR * 2
    area_toque_y_max = posicao_jogador_vermelho[1] + RAIO_JOGADOR * 2

    if (
        area_toque_x_min <= posicao_bola[0] <= area_toque_x_max
        and area_toque_y_min <= posicao_bola[1] <= area_toque_y_max
    ):
        vetor_jogador = (
            posicao_bola[0] - posicao_jogador_vermelho[0],
            posicao_bola[1] - posicao_jogador_vermelho[1],
        )

        comprimento_vetor = math.sqrt(vetor_jogador[0] ** 2 + vetor_jogador[1] ** 2)
        vetor_jogador = (
            vetor_jogador[0] / comprimento_vetor,
            vetor_jogador[1] / comprimento_vetor,
        )

        # calcular produto escalar da superfície do jogador
        produto_escalar = vetor_jogador[0] * 0

        vetor_bola = (
            vetor_jogador[0] - 2 * produto_escalar * 0,
            vetor_jogador[1] - 2 * produto_escalar * 1,
        )

        estado_jogo["bola"]["direcao_x"] = vetor_bola[0]
        estado_jogo["bola"]["direcao_y"] = vetor_bola[1]


def guarda_posicoes_para_var(estado_jogo):
    estado_jogo["var"]["bola"].append(estado_jogo["bola"]["objeto"].pos())
    estado_jogo["var"]["jogador_vermelho"].append(estado_jogo["jogador_vermelho"].pos())
    estado_jogo["var"]["jogador_azul"].append(estado_jogo["jogador_azul"].pos())


def main():
    print("FOOSBALL ⚽\n")
    estado_jogo = init_state()
    setup(estado_jogo, True)
    while True:
        estado_jogo["janela"].update()
        if estado_jogo["bola"] is not None:
            movimenta_bola(estado_jogo)
        verifica_colisoes_ambiente(estado_jogo)
        verifica_golos(estado_jogo)
        if estado_jogo["jogador_vermelho"] is not None:
            verifica_toque_jogador_azul(estado_jogo)
        if estado_jogo["jogador_azul"] is not None:
            verifica_toque_jogador_vermelho(estado_jogo)


if __name__ == "__main__":
    main()
