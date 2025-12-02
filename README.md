# Projecto_01_IPRP

naquela funcao temos de fazer as outras funcoes pq assim comecamos logo o jogo tas a ver. em vez de dar return no pre_state que ate podia funcionar mas acho que nao é suposto fazermos assim. acho que temos de fazer as funcoes criar_entidade(player), spawn_inimigos_em_grelha() e restaurar_balas() tas a ver

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

