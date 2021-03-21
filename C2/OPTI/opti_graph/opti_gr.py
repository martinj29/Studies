import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

class Sommet(object):
    def __init__(self,nom):
        self._nom = nom
    @property
    def nom(self):
        return self._nom
    def __repr__(self):
        return str(self._nom)

class Arete(object):
    def __init__(self,nom,s1,s2,oriented=True,weight=1):
        """
        arete entre s1 et s2
        :param nom: nom
        :param s1: sommet d'origine
        :param s2: sommet d'arrivée
        :param oriented: arete orientée
        """
        self._nom   = nom
        self._s1    = s1
        self._s2    = s2
        self.weight = weight
    @property
    def tuple(self):
        return (self._s1,self._s2)
    @property
    def string_tuple(self):
        return (self.s1.nom,self.s2.nom)
    @property
    def s1(self):
        return self._s1
    @property
    def s2(self):
        return self._s2
    @property
    def nom(self):
        return self._nom

    def __repr__(self):
        return str(self._nom)



class Oriented_Graph(object):
    def __init__(self,X,A):
        """
        Crée l'objet Oriented_Graph
        :param X: sommets [liste de sommets]
        :param A: aretes [liste de arrete]
        """
        self._X = X
        self._A = A

    @property
    def X(self):
        return self._X
    @property
    def A(self):
        return self._A
    @property
    def string_sommets(self):
        return [x.nom for x in self._X]
    @property
    def incidence_matrix(self):
        # Initialisation
        if 1 :
            array = np.array([[0 for a in self._A] for s in self._X])
            df = pd.DataFrame(array, index=[s.nom for s in self._X], columns=[a.nom for a in self._A])

        # Work
        if 1 :
            for x in self._X:
                for a in self._A:
                    if   a.s1 == x : df.loc[x.nom,a.nom] =  1
                    elif a.s2 == x : df.loc[x.nom,a.nom] =  -1
                    else           : df.loc[x.nom,a.nom] =  0

        return df
    @property
    def adjacence_matrix(self):
        # Initialisation
        if 1 :
            array = np.array([[0 for a in self._X] for s in self._X])
            df = pd.DataFrame(array, index=[s.nom for s in self._X], columns=[a.nom for a in self._X])
            aretes = [a.string_tuple for a in self._A]

        # Work
        if 1 :
            for s1 in self._X:
                for s2 in self._X:
                    df.loc[s1.nom,s2.nom] = 1 if (s1.nom,s2.nom) in aretes else 0

        return df
    @property
    def classes_equivalence(self):
        d = {x.nom:None for x in self._X}
        def visiter(s, i):
            if d[s.nom] is None :
                d[s.nom] = i
                for next in self.successeur(s):
                    visiter(next, i)

        cpt = 1
        for x in self._X :
            visiter(x,cpt)
            cpt += 1

        return d
    @property
    def is_connex(self):
        d   = self.classes_equivalence
        all = set([d[key] for key in d])
        if len(all) == 1: return True
        else            : return False

    # Networkx
    if 1 :
        @property
        def kx(self):
            G = nx.DiGraph()
            for node in self._X :
                G.add_node(node)
            for edge in self._A :
                G.add_edge(edge.s1,edge.s2,weight=edge.weight)
            return G
        def kx_show(self):
            return nx.draw_networkx(self.kx)



    def successeur(self,x):
        # Initialisation
        if 1 :
            if isinstance(x,str):
                for xi in self._X:
                    if xi.nom == x:
                        somm = xi
                        break
            elif isinstance(x,Sommet):
                somm = x
            else :
                raise ValueError("la valeur renseignée n'est pas un sommet")

        # Work
        if 1 :
            sucess = []
            for arete in self._A :
                if arete.s1.nom == somm.nom:
                    sucess.append(arete.s2)

        return sucess
    def predecesseur(self,x):
        # Initialisation
        if 1:
            if isinstance(x, str):
                for xi in self._X:
                    if xi.nom == x:
                        somm = xi
                        break
            elif isinstance(x, Sommet):
                somm = x
            else:
                raise ValueError("la valeur renseignée n'est pas un sommet")

        # Work
        if 1 :
            l = []
            for s in self._X:
                if somm.nom in [a.nom for a in self.successeur(s)]:
                    l.append(s)

        return l
    def parcours_sommets(self,func_traitement=lambda s:None):
        visites = []
        def visiter(s,func):
            if not s.nom in visites :
                visites.append(s.nom)
                func(s)
                for next in self.successeur(s):
                    visiter(next,func)

        for x in self._X:
            visiter(x,func_traitement)

    def print_all_sucess(self):
        st = ""
        for s in self._X :
            st += f"gamma({s.nom}) = "+str([so.nom for so in self.successeur(s)])+'\n'
        return st

    def __repr__(self):
        string = "Graph Object\n"
        string += "Adjacence :\n" + str(self.adjacence_matrix)
        string += "\n\nIncidence :\n" + str(self.incidence_matrix)
        string += "\n\nSucesseurs :\n"+self.print_all_sucess()
        return string