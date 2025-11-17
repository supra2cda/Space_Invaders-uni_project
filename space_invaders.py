import turtle
import random
import time
import os
import sys

# =========================
# Parâmetros / Constantes
# =========================
LARGURA, ALTURA = 600, 800 #mudei antes tava 900
BORDA_X = (LARGURA // 2) - 20
BORDA_Y = (ALTURA // 2) - 10

PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 16

ENEMY_ROWS = 3
ENEMY_COLS = 10
ENEMY_SPACING_X = 28 #mudei antes tava 60
ENEMY_SPACING_Y = 10 #mudei antes tava 60
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

# =========================
# Top Resultados (Highscores)
# =========================
def ler_highscores(filename):
    print("[ler_highscores] por implementar")

def atualizar_highscores(filename, score):
    print("[atualizar_highscores] por implementar")

# =========================
# Guardar / Carregar estado (texto)
# =========================
def guardar_estado_txt(filename, state):
    print("[guardar_estado_txt] por implementar")

def carregar_estado_txt(filename):
    print("[carregar_estado_txt] por implementar")
    

# =========================
# Criação de entidades (jogador, inimigo e balas)
# =========================
def criar_entidade(x,y,tipo): #DONE
    t = turtle.Turtle(visible=False)
    if tipo == "player":
        t.shape("player.gif")
    else:
        t.shape("enemy.gif")
    
    #meter o gajo na posicao certa => 0, -275 +/- e po-lo no dict
    t.penup()
    t.goto(x, y)

    t.showturtle()
    return t 

def criar_bala(x, y, tipo): #DONE
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

def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None): #DONE
   posicoes_existentes = []

   for i in range(ENEMY_ROWS):
       for j in range(ENEMY_COLS):
        y = ENEMY_START_Y - ((ENEMY_SIZE+ENEMY_SPACING_Y) * i)
        x = -BORDA_X + ((ENEMY_SIZE+ENEMY_SPACING_X) * j)
   
        state["enemies"].append(criar_entidade(x, y, "enemy"))
        posicoes_existentes.append([x, y])
        state["enemy_moves"] = posicoes_existentes

def restaurar_balas(state, lista_pos, tipo): #GRAVAR A POSTIÇÃO DAS BALAS(PLAYER E ENEMY)
    print("[restaurar_balas] por implementar")

# =========================
# Handlers de tecla 
# =========================
def mover_esquerda_handler(): #DONE
    player = STATE["player"]
    
    new_x = player.xcor() - PLAYER_SPEED #mover para a esquerda
    
    if new_x > -BORDA_X: #garantir que n passa a borda
        player.setx(new_x)
    else:
        player.setx(-BORDA_X)

def mover_direita_handler(): #DONE
    player = STATE["player"]

    new_x = player.xcor() + PLAYER_SPEED #mover para a direita
    
    if new_x < BORDA_X: #garantir que n passa a borda
        player.setx(new_x)
    else:
        player.setx(BORDA_X)

def disparar_handler(): #DONE
    player = STATE["player"]
    
    xcor = player.xcor()
    ycor = player.ycor()
    
    state["player_bullets"].append(criar_bala(xcor, ycor + PLAYER_BULLET_SPEED, "player_bullets"))

def gravar_handler():
    print("[gravar_handler] por implementar")

def terminar_handler():
    print("[terminar_handler] por implementar")

# =========================
# Atualizações e colisões
# =========================
def atualizar_balas_player(state): #DONE
    bullets = state["player_bullets"]

    for bullet in bullets:
        bullet.sety(bullet.ycor() + PLAYER_BULLET_SPEED) #andar com as bullets pra cima
     
        if (bullet.ycor() + PLAYER_BULLET_SPEED) >= BORDA_Y: #se as bullets sairem das boudaries
            bullet.hideturtle()
            bullets.remove(bullet)

def atualizar_balas_inimigos(state): #DONE
    bullets = state["enemy_bullets"]

    for bullet in bullets:
        bullet.sety(bullet.ycor() - ENEMY_BULLET_SPEED) #andar com as bullets pra cima
     
        if (bullet.ycor() - ENEMY_BULLET_SPEED) >= -BORDA_Y: #se as bullets sairem das boudaries
            bullet.hideturtle()
            bullets.remove(bullet)

def atualizar_inimigos(state): #DONE
    for enemy in state["enemies"]:
        enemy.sety(enemy.ycor() - ENEMY_FALL_SPEED) #os enemies caem tds

        num = round(random.random(), 1) #drift
        lftOrRgt = random.random()

        if num == ENEMY_DRIFT_CHANCE and lftOrRgt < 0.5:
            enemy.setx(enemy.xcor() + ENEMY_DRIFT_STEP)
        elif num == ENEMY_DRIFT_CHANCE and lftOrRgt > 0.5:
            enemy.setx(enemy.xcor() - ENEMY_DRIFT_STEP)
       
def inimigos_disparam(state):
    print("[inimigos_disparam] por implementar")

def verificar_colisoes_player_bullets(state):
    print("[verificar_colisoes_player_bullets] por implementar")

def verificar_colisoes_enemy_bullets(state):
    print("[verificar_colisoes_enemy_bullets] por implementar")

def inimigo_chegou_ao_fundo(state):
    print("[inimigo_chegou_ao_fundo] por implementar")

def verificar_colisao_player_com_inimigos(state):
    print("[verificar_colisao_player_com_inimigos] por implementar")

# =========================
# Execução principal
# =========================
if __name__ == "__main__":
    # Pergunta inicial: carregar?
    filename = input("Carregar jogo? Se sim, escreva nome do ficheiro, senão carregue Return: ").strip()
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
        "enemy_moves": [], #im using this variable to track the postion of the enemies
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
        state["player"] = criar_entidade(0, -280,"player") #mudei aq (antes = -350)
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