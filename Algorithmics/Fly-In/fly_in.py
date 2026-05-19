from srcs.game_engine import GameEngine
import sys


def main() -> None:
    if len(sys.argv) > 2:
        print("Too much arguments.\nRun only python3 fly_in.py.")
        sys.exit(1)
    game_engine = GameEngine(1920, 1080)
    game_engine.game_loop()


if __name__ == "__main__":
    main()
