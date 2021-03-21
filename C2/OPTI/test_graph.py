from opti_graph import Sommet,Arete,Oriented_Graph

def test1():

    # Sommets
    if 1 :
        a = Sommet("a")
        b = Sommet("b")
        c = Sommet("c")
        d = Sommet("d")

    # Aretes
    if 1 :
        a1 = Arete("a1",a,c)
        a2 = Arete("a2",b,a)
        a3 = Arete("a3",c,b)
        a4 = Arete("a4",a,d)
        a5 = Arete("a5",b,d)
        a6 = Arete("a6",d,c)

    g = Oriented_Graph([a,b,c,d],[a1,a2,a3,a4,a5,a6])
    g.successeur(a)
    g.incidence_matrix
    g.adjacence_matrix
    g.parcours_sommets(func_traitement=lambda s: print(s.nom))
    g.classes_equivalence
    g.is_connex
    a=1
def test2():
    # Sommets
    if 1:
        a = Sommet("1")
        b = Sommet("2")
        c = Sommet("3")
        d = Sommet("4")

    # Aretes
    if 1:
        a1 = Arete("a1", a, b)
        a2 = Arete("a2", a, c)
        a3 = Arete("a3", b, c)
        a4 = Arete("a4", b, d)
        g = Oriented_Graph([a, b, c, d], [a1, a2, a3, a4])
        print(g.successeur(a))
        print(g.incidence_matrix)
        print(g.adjacence_matrix)
        print(g.parcours_sommets(func_traitement=lambda s: print(s.nom)))
        print(g.classes_equivalence)
        print(g.is_connex)
def test3():
    # Sommets
    if 1:
        s1 = Sommet("1")
        s2 = Sommet("2")
        s3 = Sommet("3")
        s4 = Sommet("4")
        s5 = Sommet("5")

    # Aretes
    if 1:
        a1 = Arete("a1", s1, s3)
        a2 = Arete("a2", s1, s2)
        a3 = Arete("a3", s1, s4)
        a4 = Arete("a4", s3, s2)
        a5 = Arete("a5", s3, s4)
        a6 = Arete("a6", s3, s5)
        a7 = Arete("a7", s4, s2)
        a8 = Arete("a8", s4, s5)
        g = Oriented_Graph([s1, s2, s3, s4,s5], [a1, a2, a3, a4, a5, a6, a7, a8])
        print(g)
def test4():
    """
    test de networkx
    :return:
    """
    # Sommets
    if 1:
        s1 = Sommet("1")
        s2 = Sommet("2")
        s3 = Sommet("3")
        s4 = Sommet("4")
        s5 = Sommet("5")

    # Aretes
    if 1:
        a1 = Arete("a1", s1, s3)
        a2 = Arete("a2", s1, s2)
        a3 = Arete("a3", s1, s4)
        a4 = Arete("a4", s3, s2)
        a5 = Arete("a5", s3, s4)
        a6 = Arete("a6", s3, s5)
        a7 = Arete("a7", s4, s2)
        a8 = Arete("a8", s4, s5)
        g = Oriented_Graph([s1, s2, s3, s4,s5], [a1, a2, a3, a4, a5, a6, a7, a8])
        g.kx
        a=1

def entrainement_partiel():
    # Init
    if 1:
        s1 = Sommet("1")
        s2 = Sommet("2")
        s3 = Sommet("3")
        s4 = Sommet("4")
        s5 = Sommet("5")
        a1 = Arete("a1", s1, s3)
        a2 = Arete("a2", s1, s2)
        a3 = Arete("a3", s1, s4)
        a4 = Arete("a4", s3, s2)
        a5 = Arete("a5", s3, s4)
        a6 = Arete("a6", s3, s5)
        a7 = Arete("a7", s4, s2)
        a8 = Arete("a8", s4, s5)
        g = Oriented_Graph([s1, s2, s3, s4, s5], [a1, a2, a3, a4, a5, a6, a7, a8])

        lsomm = [Sommet("A"),Sommet("B"),Sommet("C"),Sommet("D"),Sommet("E"),Sommet("F"),Sommet("G")]
        larr = [Arete("a1", lsomm[0],lsomm[1],weight=12),
                Arete("a2", lsomm[3],lsomm[0],weight=9),
                Arete("a3", lsomm[0],lsomm[2],weight=20),
                Arete("a4", lsomm[3],lsomm[2],weight=8),
                Arete("a5", lsomm[3],lsomm[5],weight=21),
                Arete("a6", lsomm[1],lsomm[6],weight=13),
                Arete("a7", lsomm[6],lsomm[2],weight=2),
                Arete("a8", lsomm[6],lsomm[5],weight=5),
                Arete("a9", lsomm[6],lsomm[4],weight=9),
                Arete("a10", lsomm[5],lsomm[4],weight=3),
                Arete("a11", lsomm[2],lsomm[5],weight=11)]
        g2 = Oriented_Graph(lsomm,larr)


    #Q0
    if 1 :
        g.kx_show()
    #Q1a
    if 1 :
        print("Q1a ")
        print(g.incidence_matrix)
    #Q1b
    if 1 :
        print("Q1b")
        print(g.adjacence_matrix)
    #Q1c
    if 1 :
        print("Q1c")
        print(g.liste_successeurs)
        #print(g.liste_predecesseurs)
    #Q2
    if 1 :
        print("\nQ2")
        g2.Moore_Dijkstra(lsomm[0],lsomm[4])
        pass



    return


if __name__ == '__main__':
    #test1()
    #test2()
    #test3()
    #test4()
    entrainement_partiel()