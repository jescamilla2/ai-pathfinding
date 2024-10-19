import argparse # module to read arguments from the command line

def main():
    # create a parser object
    parser = argparse.ArgumentParser('A-Star', description='A* search algorithm')

    # add the arguments
    parser.add_argument('filename', type=str, help='file containing the grid')
    parser.add_argument('heuristic', type=str, default=None, help='specifies the heuristic to be used: manhattan/euclidean')

    # parse the arguments
    args = parser.parse_args()

    print(f"Argument 1: {args.filename}")
    if args.heuristic:
        print(f"Argument 2: {args.heuristic}")
    else:
        print("Argument 2 was not provided.")

if __name__ == '__main__':
    # execute only if run as a script
    main()