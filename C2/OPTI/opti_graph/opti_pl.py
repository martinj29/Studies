import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class PLMatrix():
    def __init__(self, xi, ei, Z, C, S):
        # Initialisations
        if 1 :
            self._hbase     = xi
            self._base      = ei
            self._Z         = np.array(Z,dtype=float)
            self._C         = np.array(C,dtype=float)
            self._S         = np.array(S,dtype=float)
            self._point     = [0,0]
            self._var_point = xi
            self._header    = self._base + self._hbase

    def __repr__(self):
        return str(self.matrix)
    @property
    def matrix(self):
        df = pd.DataFrame(self._C, columns=self._header, index=self._base)
        df = df.assign(solutions=self._S)
        df.loc["Z"] = self._Z
        return df
    @property
    def inside_mat(self):
        return self.matrix.loc[self.base_names]
    @property
    def base_names(self):
        return self._base
    @property
    def hbase_names(self):
        return [h for h in self._header if h not in self.base_names]
    @property
    def grad_Z(self):
        return np.array(list(self.matrix.loc["Z"].values)[:-1])
    @property
    def can_continue(self):
        return True in [g>0 for g in self.grad_Z]

    def print(self):
        print(self.matrix)
    def switch(self,vare,vars):
        """
        Echange une variable entrante et une variable sortante de base
        :param vare: variable entrante
        :param vars: variable sortante
        :return:
        """
        assert vare not in self._base
        assert vare in self._hbase
        assert vars not in self._hbase
        assert vars in self._base

        ib     = self._base.index(vars)
        ihb    = self._hbase.index(vare)
        ipivotx = (self._header).index(vare)
        ipivoty = ib

        # Remplacement des noms
        self._hbase[ihb] = vars
        self._base[ib]   = vare

        # Normalisation du pivot
        pivot = self._C[ipivoty][ipivotx]
        self._C[ipivoty] = self._C[ipivoty]/pivot
        self._S[ipivoty] = self._S[ipivoty]/pivot

        # Annulation des lignes
        n_lignes = len(self._C)

        for i in range(n_lignes):
            if i != ipivoty :
                val  = self._C[i][ipivotx]
                self._C[i] = self._C[i]-val*self._C[ipivoty]
                self._S[i] = self._S[i]-val*self._S[ipivoty]

        # Annulation dans Z
        zannul  = self._Z[ipivotx]
        self._Z[:-1] = self._Z[:-1]-zannul*self._C[ipivoty]
        self._Z[-1]  = self._Z[-1]+zannul*self._S[ipivoty]

        # MAJ de point
        if self._header[-2] in self._hbase : self._point[0] = 0
        else                              : self._point[0] = self._S[self._base.index(self._header[-2])]

        if self._header[-1] in self._hbase : self._point[1] = 0
        else                              : self._point[1] = self._S[self._base.index(self._header[-1])]

class PLSimplex():
    def __init__(self, *args):
        if len(args) != 0 :
            self.mat       = PLMatrix(*args) # matrice courante (change)
            self._init_mat = PLMatrix(*args) # martice initiale (immobile)

    def launch(self):
        print("######### Début du Simplex #########")
        print("Matrice initiale : ")
        print("Point",self.mat._point)
        print(self.mat)
        current_mat = self.mat

        while current_mat.can_continue :
            print()
            entering_base = current_mat.matrix.columns[list(current_mat.grad_Z).index(max(current_mat.grad_Z))]
            quitting_base = self.quitting(entering_base)
            current_mat.switch(entering_base,quitting_base)
            print(f"Variable entrante : {entering_base}")
            print(f"Variable sortante : {quitting_base}")
            print(current_mat)
            print(f"Point : ({current_mat._point[0]},{current_mat._point[1]})")

    def launch_graph(self,xlim,ylim,dx=100):

        # Initialisations
        if 1 :
            fig  = plt.figure()
            ax   = fig.add_subplot(111)

            mat          = self._init_mat
            styles       = ['b-', 'r-', 'g-', 'y-', 'bo', 'ro', 'go', 'yo']
            xaxis, yaxis = tuple(mat.hbase_names)
            gZ           = mat.matrix.loc['Z'][[xaxis, yaxis]]
            constraints  = mat.base_names
            resized_mat  = mat.inside_mat[[xaxis, yaxis]]
            solutions    = mat.matrix["solutions"][constraints]

            x_range = np.linspace(0,xlim,dx)
            y_range = np.linspace(0,ylim,dx)

        # Properties
        if 1 :
            ax.set_aspect(aspect="equal")
            ax.set_xlabel("x1")
            ax.set_ylabel("x2")
            ax.set_xlim(-(1/10)*xlim,xlim)
            ax.set_ylim(-(1/10)*ylim,ylim)
            ax.spines['left'].set_position('zero')
            ax.spines['bottom'].set_position('zero')

        # Plot contraintes
        if 1 :
            assert len(constraints)<=len(styles), "Ajouter des styles ou boucler"

            for i,constraint in enumerate(constraints) :
                direction      = (resized_mat.loc[constraint]['x1'],resized_mat.loc[constraint]['x2'],solutions[constraint])
                str_constraint = f"{direction[0]}x1 + {direction[1]}x2 = {direction[2]}"

                if   direction[0] == 0 : ax.plot(x_range,np.array([direction[2]/direction[1]]*dx),styles[i],label=str_constraint)
                elif direction[1] == 0 : ax.plot(np.array([direction[2]/direction[0]]*dx),y_range,styles[i],label=str_constraint)
                else                   : ax.plot(x_range,(direction[2]-direction[0]*x_range)/direction[1],styles[i],label=str_constraint)

        # Plot Z
        if 1 :
            ax.quiver(0, 0, *gZ,label="grad(Z)")
            ax.plot(x_range,-gZ[0]*x_range/gZ[1],'k--',label=f"Z=0")
            ax.plot(x_range,(gZ[0]*gZ[1]-gZ[0]*x_range)/gZ[1],'k--',label=f"Z={gZ[0]*gZ[1]}")

        # Courbe optimale
        if 1 :
            pass

        fig.legend()
        return fig



    def str_stage(self,i):
        return f"Etape {i} : "
    def quitting(self,entering):
        # rapports
        if 1 :
            rapports  = {b:np.inf for b in self.mat.base_names}
            sols      = self.mat.matrix["solutions"]
            enter_col = self.mat.matrix[entering]

            for k in rapports :
                if enter_col[k] > 0 :
                    rapports[k] = sols[k]/enter_col[k]


        # choix du meilleur
        if 1 :
            return sorted(rapports.items(), key=lambda item: item[1])[0][0]

