# Projecto_01_IPRP

falta a funcao do bullet invert

darkModern

{Yassine: 12 Andre: 10 Bernardo: 3}


no atualizar highscores eu acho que ele esta a ler e a escrever o numero no sitio do anterior mas ainda falta que ele meta o anterior no numero a seguir e que ele de input no gajo que fez o recorde

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

for valor in valores:  # substitui os valores e nomes
            if score > valor:
                if valores.index(valor) == 0:  # se o score for melhor que o 1o lugar
                    valores.insert(0, score)  # insert do score no inicio
                    valores.pop(-1)  # remove o ultimo valor
                    newNome = str(input('Digite o nome do recordista: '))
                    nomes.insert(0, newNome)
                    nomes.pop(-1)

                else:  # se for maior do que qqr lugar sem ser o 1o
                    valores.insert(0, score)  # insert do score no inicio
                    valores.pop(-1)  # remove o ultimo valor
                    newNome = str(input('Digite o nome do recordista: '))
                    nomes.insert(0, newNome)
                    nomes.pop(-1)