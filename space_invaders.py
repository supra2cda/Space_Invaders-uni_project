import turtle
import random
import time
import os
import sys

# =========================
# Parâmetros / Constantes
# =========================
LARGURA, ALTURA = 600, 800  # mudei antes tava 900
BORDA_X = (LARGURA // 2) - 20
BORDA_Y = (ALTURA // 2) - 10

PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 16

ENEMY_ROWS = 3
ENEMY_COLS = 10
ENEMY_SPACING_X = 28  # mudei antes tava 60
ENEMY_SPACING_Y = 10  # mudei antes tava 60
ENEMY_SIZE = 32
ENEMY_START_Y = BORDA_Y - ENEMY_SIZE    # topo visível
ENEMY_FALL_SPEED = 0.5
ENEMY_DRIFT_STEP = 2
ENEMY_FIRE_PROB = 0.006
ENEMY_BULLET_SPEED = 8
ENEMY_INVERT_CHANCE = 0.05
ENEMY_DRIFT_CHANCE = 0.5

COLLISION_RADIUS = 10
HIGHSCORES_FILE = "highscores.txt"
SAVE_FILE = "savegame.txt"
TOP_N = 10

STATE = None  # usado apenas para callbacks do teclado

pre_state = {
        "player": None,
        "enemies": [],
        "enemy_moves": [],
        "player_bullets": [],
        "enemy_bullets": [],
        "score": 0,
        "frame": 0,
    }

# =========================
# Top Resultados (Highscores)
# =========================


def ler_highscores(filename):  # DONE
    with open(filename, 'r') as ficheiro:
        highscores = ficheiro.read().strip().split('\n')

    nomes = []
    valores = []

    for line in highscores:
        words = line.split()
        if len(words) >= 2:
            nome = ' '.join(words[:-1])
            valor = int(words[-1])
            nomes.append(nome)
            valores.append(valor)

    return nomes, valores


def atualizar_highscores(filename, score):  # DONE
    nomes, valores = ler_highscores(filename)
    highscores = []
    inserido = False
    i = 0

    while i < len(valores):  # se o score for maior dq algum existente
        if score > valores[i]:
            newNome = input('Digite o nome do recordista: ').strip()
            nomes.insert(i, newNome)
            valores.insert(i, score)
            inserido = True
            break
        i += 1

    if (inserido == False) and (len(valores) < TOP_N):  # se ainda nao houverem 10 top players
        newNome = input('Digite o nome do recordista: ').strip()
        nomes.append(newNome)
        valores.append(score)
        inserido = True

    if (len(nomes) > TOP_N):
        nomes = nomes[:TOP_N]
        valores = valores[:TOP_N]

    with open(filename, 'w') as ficheiro:
        num = min(len(nomes), len(valores))
        for i in range(num):
            ficheiro.write(f"{nomes[i]} {valores[i]}\n")


# =========================
# Guardar / Carregar estado (texto)
# =========================


def guardar_estado_txt(filename, state):  # DONE
    with open(filename, 'w') as ficheiro:
        ficheiro.write(f'{state["player"].pos()}\n')

        # escreve o numero de inimigos
        ficheiro.write(f'{len(state["enemies"])}\n')
        for enemy in state["enemies"]:
            # escreve a posicao de cada inimigo numa linha separada
            ficheiro.write(f'{enemy.pos()}\n')

        for direction in state["enemy_moves"]:  # left  right  left  right
            ficheiro.write(f'{direction}\n')

        # posicoes das balas do player
        ficheiro.write(f'{len(state["player_bullets"])}\n')
        for bullet in state["player_bullets"]:
            ficheiro.write(f'{bullet.pos()}\n')

        # posicoes das balas dos inimigos
        ficheiro.write(f'{len(state["enemy_bullets"])}\n')
        for bullet in state["enemy_bullets"]:
            ficheiro.write(f'{bullet.pos()}\n')

        ficheiro.write(f'{state["score"]}\n')
        ficheiro.write(f'{state["frame"]}\n')


def carregar_estado_txt(filename): # DONE
    if not filename or filename.strip() == "":
        return False

    with open(filename, 'r') as ficheiro:
        lines = ficheiro.readlines()

    position = eval(lines[0].strip())


    n_enemies = int(lines[1].strip())

    enemies_position = []
    for i in range(n_enemies):
        enemies_position.append(eval(lines[2 + i].strip()))

    enemies_direction = []
    for i in range(n_enemies):
        enemies_direction.append(lines[2 + n_enemies + i].strip())


    n_bullets_player = int(lines[2 + (n_enemies * 2)].strip())

    bullets_player_position = []
    for i in range(n_bullets_player):
        bullets_player_position.append(eval(lines[3 + (n_enemies * 2) + i].strip()))

    n_bullets_enemy = int(lines[3 + (n_enemies * 2) + n_bullets_player].strip())

    bullets_enemy_position = []
    for i in range(n_bullets_enemy):
        bullets_enemy_position.append(eval(lines[4 + (n_enemies * 2) + n_bullets_player + i].strip()))

    score = int(lines[4 + (n_enemies * 2) + n_bullets_player + n_bullets_enemy].strip())
    frame = int(lines[5 + (n_enemies * 2) + n_bullets_player + n_bullets_enemy].strip())

    pre_state["player"] = position # coloca td no dicionario pre_state
    pre_state["enemies"] = enemies_position
    pre_state["enemy_moves"] = enemies_direction
    pre_state["player_bullets"] = bullets_player_position
    pre_state["enemy_bullets"] = bullets_enemy_position
    pre_state["score"] = score
    pre_state["frame"] = frame


    return True

# =========================
# Criação de entidades (jogador, inimigo e balas)
# =========================


def criar_entidade(x, y, tipo):  # DONE
    t = turtle.Turtle(visible=False)
    if tipo == "player":
        t.shape("player.gif")
    else:
        t.shape("enemy.gif")

    # meter o gajo na posicao certa => 0, -275 +/- e po-lo no dict
    t.penup()
    t.goto(x, y)

    t.showturtle()
    return t


def criar_bala(x, y, tipo):  # DONE
    t = turtle.Turtle(visible=False)
    t.penup()

    if tipo == "player_bullets":
        t.color("red")

    elif tipo == "enemy_bullets":
        t.color("yellow")

    t.shape("square")
    t.shapesize(.5, .20)
    t.goto(x, y)
    t.showturtle()

    return t


def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):  # DONE
    if loaded == True:
        for enemy in range(len(posicoes_existentes)):
            x = posicoes_existentes[enemy][0]
            y = posicoes_existentes[enemy][1]

            state["enemies"].append(criar_entidade(x, y, "enemy"))
            state["enemy_moves"].append(dirs_existentes[enemy])

    else:
        for i in range(ENEMY_ROWS):
            for j in range(ENEMY_COLS):
                y = ENEMY_START_Y - ((ENEMY_SIZE+ENEMY_SPACING_Y) * i)
                x = -BORDA_X + ((ENEMY_SIZE+ENEMY_SPACING_X) * j)

                state["enemies"].append(criar_entidade(x, y, "enemy"))

                num = round(random.random(), 2)
                if num < 0.5:
                    state["enemy_moves"].append("Right")
                else:
                    state["enemy_moves"].append("Left")


def restaurar_balas(state, lista_pos, tipo):  # DONE
    for bullet in range(len(lista_pos)):
        x = lista_pos[bullet][0]
        y = lista_pos[bullet][1]

        if tipo == "player_bullets":
            state["player_bullets"].append(criar_bala(x, y, "player_bullets"))
        elif tipo == "enemy_bullets":
            state["enemy_bullets"].append(criar_bala(x, y, "enemy_bullets"))

# =========================
# Handlers de tecla
# =========================


def mover_esquerda_handler():  # DONE
    player = STATE["player"]

    new_x = player.xcor() - PLAYER_SPEED  # mover para a esquerda

    if new_x > -BORDA_X:  # garantir que n passa a borda
        player.setx(new_x)
    else:
        player.setx(-BORDA_X)


def mover_direita_handler():  # DONE
    player = STATE["player"]

    new_x = player.xcor() + PLAYER_SPEED  # mover para a direita

    if new_x < BORDA_X:  # garantir que n passa a borda
        player.setx(new_x)
    else:
        player.setx(BORDA_X)


def disparar_handler():  # DONE
    player = STATE["player"]

    xcor = player.xcor()
    ycor = player.ycor()

    STATE["player_bullets"].append(criar_bala(xcor, ycor + PLAYER_BULLET_SPEED, "player_bullets"))


def gravar_handler():  # DONE
    guardar_estado_txt(STATE["files"]["save"], STATE)
    print('O seu jogo foi guardado!')


def terminar_handler():  # DONE
    turtle.bye()
    atualizar_highscores(STATE["files"]["highscores"], STATE["score"])
    sys.exit(0)


# =========================
# Atualizações e colisões
# =========================


def atualizar_balas_player(state):  # DONE
    bullets = state["player_bullets"]

    for bullet in bullets:
        # andar com as bullets pra cima
        bullet.teleport(bullet.xcor(), bullet.ycor() + PLAYER_BULLET_SPEED)

        if (bullet.ycor() + PLAYER_BULLET_SPEED) >= BORDA_Y:  # se as bullets sairem das boudaries
            bullet.hideturtle()
            bullets.remove(bullet)


def atualizar_balas_inimigos(state):  # DONE
    bullets = state["enemy_bullets"]

    for bullet in bullets:
        # andar com as bullets pra cima
        bullet.teleport(bullet.xcor(), bullet.ycor() - ENEMY_BULLET_SPEED)

        if (bullet.ycor() - ENEMY_BULLET_SPEED) < -BORDA_Y:  # se as bullets sairem das boudaries
            bullet.hideturtle()
            bullets.remove(bullet)


def atualizar_inimigos(state):  # DONE
    enemyNum = 0

    for enemy in state["enemies"]:
        enemy.teleport(enemy.xcor(), enemy.ycor() -
                       ENEMY_FALL_SPEED)  # descer os inimigos

        driftNum = round(random.random(), 1)  # drift
        invNum = round(random.random(), 2)  # invert

        if invNum == ENEMY_INVERT_CHANCE:
            if state["enemy_moves"][enemyNum] == "Left":
                state["enemy_moves"][enemyNum] = "Right"
            elif state["enemy_moves"][enemyNum] == "Right":
                state["enemy_moves"][enemyNum] = "Left"

        if (state["enemy_moves"][enemyNum] == "Right") and (enemy.xcor() + ENEMY_DRIFT_STEP >= BORDA_X):
            state["enemy_moves"][enemyNum] = "Left"
        elif (state["enemy_moves"][enemyNum] == "Left") and (enemy.xcor() - ENEMY_DRIFT_STEP <= -BORDA_X):
            state["enemy_moves"][enemyNum] = "Right"

        if driftNum == ENEMY_DRIFT_CHANCE:
            if state["enemy_moves"][enemyNum] == "Right":
                enemy.teleport(enemy.xcor() + ENEMY_DRIFT_STEP, enemy.ycor())
            elif state["enemy_moves"][enemyNum] == "Left":
                enemy.teleport(enemy.xcor() - ENEMY_DRIFT_STEP, enemy.ycor())

        enemyNum += 1


def inimigos_disparam(state):  # DONE
    for enemy in state["enemies"]:
        num = round(random.random(), len(str(ENEMY_FIRE_PROB).split('.')[1])) # len(...) arredonda o numero para o numero de casas decimais

        if num == ENEMY_FIRE_PROB:
            xcor = enemy.xcor()
            ycor = enemy.ycor()

            state["enemy_bullets"].append(criar_bala(
                xcor, ycor - ENEMY_BULLET_SPEED, "enemy_bullets"))


def verificar_colisoes_player_bullets(state):  # DONE
    for bullet in state["player_bullets"]:
        for enemy in state["enemies"]:
            if (bullet.ycor() > (enemy.ycor() - COLLISION_RADIUS)) and (bullet.ycor() < (enemy.ycor() + COLLISION_RADIUS)):
                if (bullet.xcor() > (enemy.xcor() - COLLISION_RADIUS)) and (bullet.xcor() < (enemy.xcor() + COLLISION_RADIUS)):
                    if enemy in state["enemies"]:
                        state["enemy_moves"].pop(state["enemies"].index(enemy))

                        enemy.hideturtle()
                        state["enemies"].remove(enemy)

                        bullet.hideturtle()
                        state["player_bullets"].remove(bullet)

                        state["score"] += 1
                        break


def verificar_colisoes_enemy_bullets(state):  # DONE
    bullets = state["enemy_bullets"]
    player = state["player"]

    for bullet in bullets:
        if (bullet.ycor() < (player.ycor() + COLLISION_RADIUS)) and (bullet.ycor() > (player.ycor() - COLLISION_RADIUS)):
            if (bullet.xcor() > (player.xcor() - COLLISION_RADIUS)) and (bullet.xcor() < (player.xcor() + COLLISION_RADIUS)):
                return True


def inimigo_chegou_ao_fundo(state):  # DONE
    enemies = state["enemies"]

    for enemy in enemies:
        if (enemy.ycor() <= -BORDA_Y):
            return True


def verificar_colisao_player_com_inimigos(state):  # DONE
    enemies = state["enemies"]
    player = state["player"]

    for enemy in enemies:
        if (enemy.ycor() < (player.ycor() + COLLISION_RADIUS)) and (enemy.ycor() > (player.ycor() - COLLISION_RADIUS)):
            if (enemy.xcor() > (player.xcor() - COLLISION_RADIUS)) and (enemy.xcor() < (player.xcor() + COLLISION_RADIUS)):
                return True


# =========================
# Execução principal
# =========================
if __name__ == "__main__":
    # Pergunta inicial: carregar?
    filename = input(
        "Carregar jogo? Se sim, escreva nome do ficheiro, senão carregue Return: ").strip()
    loaded = carregar_estado_txt(filename)

    # Ecrã
    screen = turtle.Screen()
    screen.title("Space Invaders IPRP")
    screen.bgcolor("black")
    screen.setup(width=LARGURA, height=ALTURA, starty=0)
    screen.tracer(0)

    # Imagens obrigatórias
    for img in ["player.gif", "enemy.gif"]:
        if not os.path.exists(img):
            print("ERRO: imagem '" + img + "' não encontrada.")
            sys.exit(1)
        screen.addshape(img)

    # Estado base
    state = {
        "screen": screen,
        "player": None,
        "enemies": [],
        "enemy_moves": [],
        "player_bullets": [],
        "enemy_bullets": [],
        "score": 0,
        "frame": 0,
        "files": {"highscores": HIGHSCORES_FILE, "save": SAVE_FILE}
    }

    # Construção inicial
    if loaded:
        state["player"] = criar_entidade(pre_state["player"][0], pre_state["player"][1], "player") # criar player
        spawn_inimigos_em_grelha(state, pre_state["enemies"], pre_state["enemy_moves"]) # criar inimigos
        restaurar_balas(state, pre_state["player_bullets"], "player_bullets") # criar as balas
        restaurar_balas(state, pre_state["enemy_bullets"], "enemy_bullets")
    else:
        print("New game!")
        state["player"] = criar_entidade(0, -280, "player") # mudei aq (antes = -350)
        spawn_inimigos_em_grelha(state, None, None)

    # Variavel global para os keyboard key handlers
    STATE = state

    # Teclas
    screen.listen()
    screen.onkeypress(mover_esquerda_handler, "Left")
    screen.onkeypress(mover_direita_handler, "Right")
    screen.onkeypress(disparar_handler, "space")
    screen.onkeypress(gravar_handler, "g")
    screen.onkeypress(terminar_handler, "Escape")

    # Loop principal
    while True:
        atualizar_balas_player(STATE)
        atualizar_inimigos(STATE)
        inimigos_disparam(STATE)
        atualizar_balas_inimigos(STATE)
        verificar_colisoes_player_bullets(STATE)

        if verificar_colisao_player_com_inimigos(STATE):
            print("Colisão direta com inimigo! Game Over")
            terminar_handler()

        if verificar_colisoes_enemy_bullets(STATE):
            print("Atingido por inimigo! Game Over")
            terminar_handler()

        if inimigo_chegou_ao_fundo(STATE):
            print("Um inimigo chegou ao fundo! Game Over")
            terminar_handler()

        if len(STATE["enemies"]) == 0:
            print("Vitória! Todos os inimigos foram destruídos.")
            terminar_handler()

        STATE["frame"] += 1
        screen.update()
        time.sleep(0.016)
