import argparse
from simulator import simulate

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", type=str)
    parser.add_argument("--cycles", type=int)
    return parser.parse_args()

def main():
    args = parse_arguments()
    simulate(args.input_file, args.cycles)

if __name__ == '__main__':
    main()