if __name__ == '__main__':
    import pygame

    import utils
    from client import NetworkClient

    client = NetworkClient()
    username: str = ""

    pygame.init()
    background = pygame.image.load(r"cards\background.png")
    player_cards_surfaces = {}

    game_display = pygame.display.set_mode((1000, 700))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Watten")
    # Pygame now allows natively to enable key repeat:
    pygame.key.set_repeat(200, 25)

    while True:
        game_display.blit(background, (0, 0))
        events = pygame.event.get()

        if not username:
            username = utils.text_input(game_display, clock)
            client.server_connect(username)

        if not client.que.empty():
            recv: dict = client.que.get()
            print(recv)

            match recv.get("command"):
                case "PLAYER_NAMES":
                    player_names: list[str] = recv.get("players")

                case "NEW_CARD":
                    card_ids: list[int] = recv.get("cards")
                    player_cards_surfaces = utils.load_card_image(player_names, card_ids)

        if player_cards_surfaces.values():
            # [[x_start, x_step, y_start, y_step],...]
            player_card_coordinates = [
                [0, 225, 110, 480, 0],
                [1, -85, 0, 125, 110],
                [2, 225, 110, -85, 0],
                [3, 915, 0, 125, 110]]

            for player, x_start, x_step, y_start, y_step in player_card_coordinates:

                for card_surface in player_cards_surfaces.get(player_names[player]):
                    game_display.blit(card_surface, (x_start, y_start))
                    x_start += x_step
                    y_start += y_step

        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                break

        pygame.display.update()
        clock.tick(60)
