import argparse
from sortpuz.solver import Solver


def main():
    parser = argparse.ArgumentParser(description="SortPuz Solver")
    parser.add_argument("-l", dest="level", required=True, default=1, metavar="level_number", type=int, help="Required, level number of the SortPuz")
    parser.add_argument("-q", dest="quick_solve", action="store_true", help="Optional, solve the puzzle quicker but might have longer steps")
    args = parser.parse_args()

    if 1 > args.level:
        print("level number must be greater than 0")
    else:
        solver = Solver(args.level, args.quick_solve)
        solver.solve()


if __name__ == "__main__":
    main()
