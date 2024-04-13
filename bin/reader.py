
import os

def gridReader(filename: str) -> list[list[int]]:

    assert(os.path.exists(filename) and os.path.isfile(filename)), '[E] path is not valid.'
    
    try:
        with open(filename, encoding='utf-8') as f:
            lines = f.readlines()
        # On récupère chacun des caractères dans les lignes qu'on transforme en int.
        # On renvoie une Matrice IxJ.
        return [[int(i) for i in c.split()] for c in [l.strip() for l in lines]]

    except Exception as e:
        print(f'[E] An error occured : {e}')
        exit(1)