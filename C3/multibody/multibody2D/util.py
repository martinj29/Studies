
def print_mat(mat, id=None, nchar=None):
    if nchar is None:
        for line in mat:
            for num in line:
                print(f"{num}"+" "*(5-len(str(num))), end=' ')
            print()
        return

    format = f".{nchar}f"

    for line in mat:
        for num in line:
            print(f"{num:{format}}",end='\t')
        print()
