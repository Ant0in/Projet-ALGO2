
import os


def gridReader(filename: str) -> list[list[int]]:

    assert(os.path.exists(filename) and os.path.isfile(filename)), '[E] path is not valid.'
    
    try:
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
        return [[int(i) for i in c.split()] for c in [l.strip() for l in lines]]

    except Exception as e:
        print(f'[E] An error occured : {e}')
        exit(1)


if __name__ == '__main__':

    exemplePath: str = r'../resources/exemple1.txt' 
    print(gridReader(exemplePath))