import checkers
from minimax_agent import MinimaxAgent


def main():
    agent_blue_wins = 0
    num_plays = 10

    for i in range(num_plays):
        game = checkers.Game(loop_mode=True)
        game.setup()
        agent_blue = MinimaxAgent(color=checkers.BLUE, game=game, depth=2)
        agent_red = MinimaxAgent(color=checkers.RED, game=game, depth=2)

        while True:  # main game loop
            if game.turn == checkers.BLUE:
                agent_blue.make_move(board=game.board)
            else:
                agent_red.make_move(board=game.board)

            if game.endit:
                print('END GAME ====================')
                if game.turn == checkers.RED:
                    agent_blue_wins += 1
                break

            game.update()

    print(f'Agent Blue won {agent_blue_wins} times out of {num_plays}!\n'
          f'{agent_blue_wins / num_plays}%')


if __name__ == '__main__':
    main()
