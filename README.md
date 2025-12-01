# Projecto_01_IPRP

m8: resolvi o problema em que no savegame ficavam varios enemy_moves


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

