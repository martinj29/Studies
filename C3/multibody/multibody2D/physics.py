import numpy as np

norm = np.linalg.norm


class vector(np.ndarray):
    """
    DEPRECIATED

    Overlayer of numpy ndarray with some additions
    """

    def __new__(cls, input_array, orientation, name=None):
        """

        :param input_array:
        :param orientation: 'v' = 'vertical', 'h' = 'horizontal', 'u' = unit, m = 'matrix'
        :param name:
        """

        if orientation == 'v' or orientation == 'vertical':
            obj = np.asarray(input_array).view(cls).reshape((1, len(input_array)))
            obj = obj.T

        elif orientation == 'm' or orientation == 'matrix':
            obj = np.asarray(input_array).view(cls).reshape((1, len(input_array)))

        else:
            obj = np.asarray(input_array).view(cls)

        # add parameter :
        obj.name = name
        return obj

    def __array_finalize__(self, obj):
        if obj is None: return
        self.name = getattr(obj, 'name', None)

    def __str__(self):
        header = "["
        ending = "]"

        repr_ = ""
        if self.name is not None:
            header = f"{self.name} = ["
        repr_ += header

        if self.is_unit:
            # vecteur unitaire
            repr_ += str(self[0]) + ending

        elif self.is_horizontal:
            vals = list(self[0])
            for i, val in enumerate(vals):
                if i == len(vals) - 1:
                    repr_ += str(val) + ending
                else:
                    repr_ += str(val) + ' '

        elif self.is_vertical:
            vals = list(self.T[0])
            for i, val in enumerate(vals):
                if i != 0:
                    repr_ += " " * len(header)
                repr_ += str(val)
                if i < len(vals) - 1:
                    repr_ += '\n'
                else:
                    repr_ += ending

        elif self.is_matrix:
            for i, line in enumerate(self):
                if i != 0:
                    repr_ += " " * len(header)
                repr_ += ' '.join([str(x) + ' ' * (5 - len(str(x))) for x in line])
                repr_ += '\n' if i < len(self) - 1 else ''
            repr_ += ending
        return repr_

    def __rmul__(self, other):
        if isinstance(other, vector):
            if other.is_vertical and self.is_horizontal:
                # return vector([np.dot(self,other)[0,0]],'u')
                return np.dot(self, other)[0, 0]
        return super(vector, self).__rmul__(other)

    def __mul__(self, other):
        return self.__rmul__(other)

    @property
    def is_vertical(self):
        if len(self.shape) > 1 and self.shape[1] == 1:
            return True
        return False

    @property
    def is_unit(self):
        return self.is_vertical and self.is_horizontal

    @property
    def is_horizontal(self):
        if self.shape[0] == 1:
            return True
        return False

    @property
    def is_matrix(self):
        return self.is_unit or (not self.is_horizontal and not self.is_vertical)


class Body:
    def __init__(self, Qs=None, dQs=None, d2Qs=None):
        assert isinstance(Qs, np.ndarray) and isinstance(dQs, np.ndarray) and isinstance(d2Qs, np.ndarray)

        self.Qs = Qs
        self.dQs = dQs
        self.d2Qs = d2Qs


class Parameter:
    def __init__(self, xi_bmgt, w0_bmgt):
        self.xi_bmgt = xi_bmgt
        self.w0_bmgt = w0_bmgt


def masse_et_poids(m, Iz, g=9.81):
    return np.diag([m, m, Iz]), np.transpose(np.array([0, -m * g, 0]))


def rotation(Q_s):
    """
    calcule la matrice de rotation entre le solide s et le R0
    :param Q_s: 
    :return: R_0s
    """
    t = Q_s[3]
    c = np.cos(t)
    s = np.sin(t)
    R_0s = np.array([[c, -s],
                     [s, c]])
    return R_0s


def position_P_R0(Qs, GP_RS):
    G_R0 = Qs[0:2]

    # Angle du solide S
    theta = Qs[2, 0]
    c = np.cos(theta)
    s = np.sin(theta)

    # matrice de changement de base de RS vers R0
    R_0s = np.array([[c, -s], [s, c]])

    P_R0 = G_R0 + R_0s @ GP_RS
    return P_R0


def vitesse_P_R0(Qs, dQs, GP_RS):
    # Vitesse centre de gravité  du solide S dans R0
    dG_R0 = dQs[0:2]

    # angle et vitesse angulaire
    theta = Qs[2, 0]
    dtheta = dQs[2, 0]
    c = np.cos(theta)
    s = np.sin(theta)

    # dérivée de la matrice de rotation
    dR_0s = dtheta * np.array([[-s, -c], [c, -s]])

    # position de P dans R0
    dP_R0 = dG_R0 + dR_0s @ GP_RS
    return dP_R0


def acceleration_P_R0(Qs, dQs, d2Qs, GP_RS):
    # acceleration de G dans R0
    d2G_R0 = d2Qs[0:2]

    # Angle, v_angulaire, a_angulaire
    theta = Qs[2, 0]
    dtheta = dQs[2, 0]
    d2theta = d2Qs[2, 0]
    c = np.cos(theta)
    s = np.sin(theta)

    # Matrices de rotation
    d2R_0s = (dtheta ** 2) * np.array([[-c, s], [-s, -c]]) + d2theta * np.array([[-s, -c], [c, -s]])

    # Accel de P dans R0
    d2P_R0 = d2G_R0 + d2R_0s @ GP_RS
    return d2P_R0


def force_ressort_amortisseur(k, c, L0, Qs1, dQs1, GP_Rs1, Qs2, dQs2, GP_Rs2):
    # Position de P1 et P2 dans R0
    P1_R0 = position_P_R0(Qs1, GP_Rs1)
    P2_R0 = position_P_R0(Qs2, GP_Rs2)

    # Vitesse de P1 et P2 dans R0
    dP1_R0 = vitesse_P_R0(Qs1, dQs1, GP_Rs1)
    dP2_R0 = vitesse_P_R0(Qs2, dQs2, GP_Rs2)

    # Déformations
    P1P2 = P2_R0 - P1_R0
    d_P1P2 = dP2_R0 - dP1_R0
    Long_P1P2 = norm(P1P2)
    delta = Long_P1P2 - L0
    d_delta = norm(d_P1P2)

    # Direction de l'effort
    if not Long_P1P2 == 0:
        u = P1P2 / Long_P1P2
    else:
        u = P1P2

    F_P2_on_P1_in_S1 = (k * delta + c * d_delta) * u
    return F_P2_on_P1_in_S1


def PuissVirtEffort(Fext, Mext, Qs, GP_Rs):
    # Angles et dR_0s^t
    theta = Qs[2, 0]
    s = np.sin(theta)
    c = np.cos(theta)
    dR_0s_transp = np.array([[-s, c], [-c, -s]])

    # terme A_theta de la formulation de Lagrange
    B_theta = GP_Rs.T * dR_0s_transp * Fext + Mext

    # Effort généralisé
    B = np.array([[Fext], [B_theta]])
    return B


def piv(Qs, dQs, GP_RS):
    theta = Qs[2, 0]
    d_theta = dQs[2, 0]

    s = np.sin(theta)
    c = np.cos(theta)

    f1 = np.array([[-c, s], [-s, -c]])
    f2 = np.array([[-s - c], [c - s]])

    C = np.concatenate((np.eye(2), f2 * GP_RS), axis=1)
    D = -(d_theta ** 2) * f1 * GP_RS

    return C, D


def pivot(par, Qs1, dQs1, GP_RS1, Qs2, dQs2, GP_RS2):
    C1, D1 = piv(Qs1, dQs1, GP_RS1)
    C2, D2 = piv(Qs2, dQs2, GP_RS2)

    OP1_R0 = position_P_R0(Qs1, GP_RS1)
    OP2_R0 = position_P_R0(Qs2, GP_RS2)
    dOP1_R0 = vitesse_P_R0(Qs1, dQs1, GP_RS1)
    dOP2_R0 = vitesse_P_R0(Qs2, dQs2, GP_RS2)

    D = D2 - D1 - 2 * par.xi_bmgt * par.w0_bmgt * (dOP2_R0 - dOP1_R0) - (par.w0_bmgt ** 2) * (OP2_R0 - OP1_R0)
    return C1, C2, D
