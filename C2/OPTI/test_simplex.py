from opti_graph import PLSimplex


def test1():
    # Initialisations
    if 1 :
        xi = ["x1","x2"]
        ei = ["e1","e2","e3"]
        Z  = [0,0,0,3,5,0]
        C  = [[1.0,0.0,0.0,1.0,0.0],
              [0.0,1.0,0.0,0.0,2.0],
              [0.0,0.0,1.0,3.0,2.0]]
        S  = [4,12,18]

    s = PLSimplex(xi,ei,Z,C,S)
    s.launch()
def test2():
    # Initialisations
    if 1 :
        xi = ["x1","x2"]
        ei = ["e1","e2","e3","e4"]
        Z  = [0,0,0,0,5,3,0]
        C  = [[1,0,0,0,2,1],
              [0,1,0,0,1,1],
              [0,0,1,0,1,0],
              [0,0,0,1,0,1]]
        S  = [8,6,3,5]

    s = PLSimplex(xi,ei,Z,C,S)
    s.launch()
def test3():
    # Initialisations
    if 1 :
        xi = ["x1","x2"]
        ei = ["e1","e2","e3"]
        Z  = [0,0,0,5,6,0]
        C  = [[1,0,0,2,4],
              [0,1,0,1,2],
              [0,0,1,2,2]]
        S  = [7,4,6]

    s = PLSimplex(xi,ei,Z,C,S)
    s.launch()
def test4():
    # Initialisations
    if 1 :
        xi = ["x1","x2"]
        ei = ["e1","e2"]
        Z  = [0,0,2,1,0]
        C  = [[1,0,2,4],
              [0,1,3,2]]
        S  = [12,12]

    s = PLSimplex(xi,ei,Z,C,S)
    fig = s.launch_graph(5,5)
    fig.show()
    s.launch()
    return
def entrainement_partiel():
    # initialisation
    if 1 :
        xi = ["x1", "x2"]
        ei = ["e1", "e2", "e3"]
        Z = [0, 0, 0, 10, 6, 0]
        C = [[1, 0, 0, 1, 1],
             [0, 1, 0, 2, 1],
             [0, 0, 1, 0, 1]]
        S = [15, 20, 12]
        s = PLSimplex(xi, ei, Z, C, S)

    #Q4
    s.launch_graph(20,20)

    #Q4b
    s.launch()

    return

if __name__ == '__main__':
    #
    #test2()
    test4()
    #entrainement_partiel()