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
    @property
    def liste_successeurs(self):
        return {x:self.successeur(x) for x in self._X}
    @property
    def liste_predecesseurs(self):
        return {x: self.predecesseur(x) for x in self._X}

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
    def unoriented_sucesseurs(self,x):
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
                elif arete.s2.nom == somm.nom :
                    sucess.append(arete.s1)
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
    def unoriented_predecesseur(self,x):
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

        return [y for y in self._X if self.get_arete(y.nom,somm.nom,unorient=True) is not None]
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
    def get_sommet(self,nom_sommet):
        for x in self._X:
            if x.nom == nom_sommet :
                return x
        return
    def get_arete(self,nom_s1,nom_s2,unorient=False):
        for a in self._A:
            if not unorient :
                if a.s1.nom==nom_s1 and a.s2.nom==nom_s2:
                    return a
            else :
                if (a.s1.nom==nom_s1 and a.s2.nom==nom_s2) or (a.s1.nom==nom_s2 and a.s2.nom==nom_s1):
                    return a
        return

    def Moore_Dijkstra(self,start,end):
        S  = []
        S_ = [x.nom for x in self._X]
        pi = {x.nom:np.inf for x in self._X}

        print(f"Calcul du plus court chemin entre {start} et {end}")

        # Initialisation
        if 1 :
            cpt = 1
            pi[start.nom] = 0
            S.append(S_.pop(S_.index(start.nom)))
            succ = self.unoriented_sucesseurs(start)
            for s in succ :
                arr = self.get_arete(start.nom,s.nom,unorient=True)
                pi[s.nom] = arr.weight
            print("Initialisation : ")
            print("S  : ",S)
            print("S_ : ",S_)
            print("pi :",pi)

        # Algo
        while len(S_) != 0 :
            print(f"Iteration {cpt}")

            # sélection du sommet
            pi_inter_S_ = {x:pi[x] for x in pi if x in S_}
            s_min       = min(pi_inter_S_, key=pi_inter_S_.get)

            # ajout aux sommets traités
            S.append(S_.pop(S_.index(s_min)))

            # opérations sur le sommet
            succ = self.unoriented_sucesseurs(s_min)
            for s in succ :
                arr = self.get_arete(s_min,s.nom,unorient=True)
                pi[s.nom] = min(pi[s_min]+arr.weight,pi[s.nom])

            # affichage
            print("S  : ", S)
            print("S_ : ", S_)
            print("pi :", pi)

            cpt+=1
        print(f"le chemin min pour aller de {start} à {end} est de {pi[end.nom]}")

        somm    = end.nom
        chemin = [end.nom]
        while somm != start.nom :
            found = False
            pred = self.unoriented_predecesseur(somm)
            for s in pred :
                arr = self.get_arete(somm,s.nom,unorient=True)
                if pi[s.nom] + arr.weight == pi[somm] :
                    chemin.append(s.nom)
                    somm = s.nom
                    found = True
                    break
            if not found : raise ValueError("Cas impossible")
        print("le chemin : ",list(reversed(chemin)))




    def __repr__(self):
        string = "Graph Object\n"
        string += "Adjacence :\n" + str(self.adjacence_matrix)
        string += "\n\nIncidence :\n" + str(self.incidence_matrix)
        string += "\n\nSucesseurs :\n"+self.print_all_sucess()
        return string