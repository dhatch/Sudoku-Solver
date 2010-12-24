import argparse

def main():
    parser = argparse.ArgumentParser(description="Solves Suduko Puzzles.")
    parser.add_argument('filename', type=file, help="name of file to load for suduko puzzle")
    parser.add_argument("-v, --verbose", help='produce detailed output', action='store_true')
    args = parser.parse_args()
    

if __name__ == '__main__':
    main()