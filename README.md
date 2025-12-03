# Projecto_01_IPRP


def ler_highscores(filename):  # DONE
    with open(filename, 'r') as ficheiro:
        # mete os valores numa lista [nome, valor, nome, valor]
        highscores = ficheiro.read().split()

    nomes = []
    valores = []

    for i in highscores:
        if (highscores.index(i) % 2) == 0:
            nomes.append(str(i))

    for i in highscores:  # mete os valores todos numa lista
        if (highscores.index(i) % 2) != 0:
            valores.append(int(i))

    return nomes, valores


bullets = state["player_bullets"]
    enemies = state["enemies"]

    bullets_to_remove = []
    enemies_to_remove = []

    for bullet in bullets[:]:  # iterar sobre cópia segura
        for enemy in enemies[:]:
            if (bullet.ycor() > (enemy.ycor() - COLLISION_RADIUS)) and (bullet.ycor() < (enemy.ycor() + COLLISION_RADIUS)):
                if (bullet.xcor() > (enemy.xcor() - COLLISION_RADIUS)) and (bullet.xcor() < (enemy.xcor() + COLLISION_RADIUS)):
                    enemy.hideturtle()
                    enemies_to_remove.append(enemy)

                    bullet.hideturtle()
                    bullets_to_remove.append(bullet)

                    state["score"] += 1
                    break  # já removemos esta bala; passa para a próxima bala

    for e in enemies_to_remove:
        if e in enemies:
            enemies.remove(e)
    for b in bullets_to_remove:
        if b in bullets:
            bullets.remove(b)

