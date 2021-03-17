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

if __name__ == '__main__':
    #test1()
    test2()
    #test3()