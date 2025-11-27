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
ENEMY_FIRE_PROB = 0.05  # 0.006
ENEMY_BULLET_SPEED = 8
ENEMY_INVERT_CHANCE = 0.05
ENEMY_DRIFT_CHANCE = 0.5

COLLISION_RADIUS = 10
HIGHSCORES_FILE = "highscores.txt"
SAVE_FILE = "savegame.txt"
TOP_N = 10

STATE = None  # usado apenas para callbacks do teclado

# =========================
# Top Resultados (Highscores)
# =========================


def ler_highscores(filename):
    ficheiro = open(filename, 'r+')

    highscores = ficheiro.read().split() # mete os valores numa lista [nome, valor]
    newHighscores = {}

    for score in range(len(highscores)):
        if score % 2 == 0:
            newHighscores.update({highscores[score]: highscores[score + 1]}) # mete a lista num dicionario

    ficheiro.close()

    return newHighscores


def atualizar_highscores(filename, score):
    highscores = ler_highscores(filename)

    with open(filename, "r+") as ficheiro:
        valores = highscores.values()

    for valor in valores:
        if (score > valor) and (valores.find(valor) == 0):
            valor = score
        elif (score > valor) and (score < (valores.find(valor) -1)):
            valor = score
    
    ficheiro.write()
    return highscores
            
            

# =========================
# Guardar / Carregar estado (texto)
# =========================


def guardar_estado_txt(filename, state):
    filename = open(state["files"]["save"], 'r+')
    filename.close()


def carregar_estado_txt(filename):
    print("[carregar_estado_txt] por implementar")


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


def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):  #still not done
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


def restaurar_balas(state, lista_pos, tipo):
    print("[restaurar_balas] por implementar")

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

    state["player_bullets"].append(criar_bala(xcor, ycor + PLAYER_BULLET_SPEED, "player_bullets"))


def gravar_handler():
    print("")


def terminar_handler():
    turtle.bye()
    print(ler_highscores(HIGHSCORES_FILE))
    atualizar_highscores(HIGHSCORES_FILE, STATE["score"])


# =========================
# Atualizações e colisões
# =========================


def atualizar_balas_player(state):  # DONE
    bullets = state["player_bullets"]

    for bullet in bullets:
        # andar com as bullets pra cima
        bullet.sety(bullet.ycor() + PLAYER_BULLET_SPEED)

        if (bullet.ycor() + PLAYER_BULLET_SPEED) >= BORDA_Y:  # se as bullets sairem das boudaries
            bullet.hideturtle()
            bullets.remove(bullet)


def atualizar_balas_inimigos(state):  # DONE
    bullets = state["enemy_bullets"]

    for bullet in bullets:
        # andar com as bullets pra cima
        bullet.sety(bullet.ycor() - ENEMY_BULLET_SPEED)

        if (bullet.ycor() - ENEMY_BULLET_SPEED) < -BORDA_Y:  # se as bullets sairem das boudaries
            bullet.hideturtle()
            bullets.remove(bullet)


def atualizar_inimigos(state):  # DONE
    enemyNum = 0

    for enemy in state["enemies"]:
        enemy.sety(enemy.ycor() - ENEMY_FALL_SPEED)  # os enemies caem tds

        driftNum = round(random.random(), 1)  # drift
        invNum = round(random.random(), 2) # invert

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
                enemy.setx(enemy.xcor() + ENEMY_DRIFT_STEP)
            elif state["enemy_moves"][enemyNum] == "Left":
                enemy.setx(enemy.xcor() - ENEMY_DRIFT_STEP)

        enemyNum += 1


def inimigos_disparam(state):  # DONE
    for enemy in state["enemies"]:
        num = round(random.random(), 2)

        if num == ENEMY_FIRE_PROB:
            xcor = enemy.xcor()
            ycor = enemy.ycor()

            state["enemy_bullets"].append(criar_bala(
                xcor, ycor - ENEMY_BULLET_SPEED, "enemy_bullets"))


def verificar_colisoes_player_bullets(state):  # DONE
    bullets = state["player_bullets"]
    enemies = state["enemies"]

    for bullet in bullets:
        for enemy in enemies:
            if (bullet.ycor() > (enemy.ycor() - COLLISION_RADIUS)) and (bullet.ycor() < (enemy.ycor() + COLLISION_RADIUS)):
                if (bullet.xcor() > (enemy.xcor() - COLLISION_RADIUS)) and (bullet.xcor() < (enemy.xcor() + COLLISION_RADIUS)):
                    enemy.hideturtle()
                    enemies.remove(enemy)

                    bullet.hideturtle()
                    bullets.remove(bullet)

                    state["score"] += 1


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
        if (enemy.ycor() == -BORDA_Y):
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
        "enemy_moves": [],  # im using this variable to track the postion of the enemies
        "player_bullets": [],
        "enemy_bullets": [],
        "score": 0,
        "frame": 0,
        "files": {"highscores": HIGHSCORES_FILE, "save": SAVE_FILE}
    }

    # Construção inicial
    if loaded:
        print("[loaded=True] por implementar")
    else:
        print("New game!")
        state["player"] = criar_entidade(
            0, -280, "player")  # mudei aq (antes = -350)
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
