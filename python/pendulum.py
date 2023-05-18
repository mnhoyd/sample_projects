import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

class Pendulum():
    """ A class for representing pendulums. """
    def __init__(self, L=1, M=1, g=9.81):
        """ A method for initializing the object. """
        self.M = M
        self.L = L
        self.g = g

    def __call__(self, t, y):
        """ A method for calculating the derivatives. """
        theta, omega = y
        dtheta = omega
        domega = -self.g/self.L*np.sin(theta)
        return dtheta, domega

    def solve(self, u0, T, dt, angle='rad'):
        """ A method for solving the ODE using SciPy. """
        if angle == 'deg':
            u0 = np.radians(u0)

        solution = solve_ivp(self,
                        (0, T), 
                        u0, 
                        t_eval=np.arange(0, T+dt, dt))
        self._t =  solution.t
        self._theta, self._omega = solution.y

    @property
    def t(self):
        try:
            return self._t
        except AttributeError:
            raise SolveMethodNotCalled('Objektet har ingen t! ' \
                                    + 'Solve har ikke blitt kalt!')

    @property
    def theta(self):
        try:
            return self._theta
        except AttributeError:
            raise SolveMethodNotCalled('Objektet har ingen theta! ' \
                                    + 'Solve har ikke blitt kalt!')

    @property
    def omega(self):
        try:
            return self._omega
        except AttributeError:
            raise SolveMethodNotCalled('Objektet har ingen omega! ' \
                                    + 'Solve har ikke blitt kalt!')
    
    @property
    def x(self):
        return self.L*np.sin(self.theta)
    
    @property
    def y(self):
        return -self.L*np.cos(self.theta)
    
    @property
    def potential(self):
        return self.M*self.g*(self.L + self.y)
    
    @property
    def vx(self):
        return np.gradient(self.x, self.t)
    @property
    def vy(self):
        return np.gradient(self.y, self.t)
    
    @property
    def kinetic(self):
        return 0.5*self.M*(self.vx**2 + self.vy**2)
    
class SolveMethodNotCalled(Exception):
    """ A class for raising exception when attributes don't exist. """
    pass

class DampenedPendulum(Pendulum):
    """ A class for representing a dampened pendulum. """
    def __init__(self, L=1, M=1, g=9.81, B=1):
        """ A method for storing attributes using the superclass. """
        super().__init__(L, M, g)
        self.B = B

    def __call__(self, t, y):
        """ A method for calculating the derivatives. """
        theta, omega = y
        dtheta = omega
        domega = -self.g/self.L*np.sin(theta) - self.B/self.M*omega
        return dtheta, domega

if __name__ == '__main__':
    pendel = Pendulum()
    pendel.solve((0.5,3), 4, 0.002)
    plt.plot(pendel.t, 
             pendel.theta, 
             color="springgreen")
    
    plt.title('Angle of a pendulum')
    plt.xlabel('Time [$s$]')
    plt.ylabel('Angle [$rad$]')
    plt.show()

    plt.figure()
    plt.plot(pendel.t, 
        pendel.kinetic, 
        color="salmon",
        label='Kinetic')
    
    plt.plot(pendel.t,
        pendel.potential, 
        color="lime",
        label='Potential')
    total_E = pendel.kinetic + pendel.potential
    
    plt.plot(pendel.t, 
        total_E,
        label='Total')
    plt.title('The energies of a pendulum')
    plt.xlabel('Time [$s$] $alpha$')
    plt.ylabel('Energy [$J$]')
    plt.legend()
    plt.show()
    
    dempet_pendel = DampenedPendulum()
    dempet_pendel.solve((0.5,3), 6, 0.002)
    plt.plot(dempet_pendel.t, dempet_pendel.theta, color="springgreen")
    plt.title('Angle of a dampened pendulum')
    plt.xlabel('Time [$s$]')
    plt.ylabel('Angle [$rad$]')
    
    plt.figure()
    plt.plot(dempet_pendel.t, 
        dempet_pendel.kinetic, 
        color="salmon",
        label='Kinetic')
    plt.plot(dempet_pendel.t,
        dempet_pendel.potential, 
        color="lime",
        label='Potential')
    total_E = dempet_pendel.kinetic + dempet_pendel.potential
    plt.plot(dempet_pendel.t, 
        total_E,
        label='Total')
    plt.title('The energies of a dampened pendulum')
    plt.xlabel('Time [$s$]')
    plt.ylabel('Energy [$J$]')
    plt.legend()
    plt.show()
    