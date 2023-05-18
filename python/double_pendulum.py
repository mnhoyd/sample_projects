from scipy.integrate import solve_ivp
import numpy as np
import matplotlib.pyplot as plt
from pendulum import SolveMethodNotCalled 

class DoublePendulum:
    """ A class for double pendulums. """
    def __init__(self, L1=1, L2=1, M1=1, M2=1, g=9.81):
        """ A method for initializing objects. """
        self.L1, self.L2, self.M1, self.M2, self.g = L1, L2, M1, M2, g

    def __call__(self, t, y):
        """ A method for calculating the derivatives. """
        L1, L2, g = self.L1, self.L2, self.g
        theta1, omega1, theta2, omega2 = y
        dtheta1, dtheta2 = omega1, omega2
        delta = theta2 - theta1

        domega1 = (L1*omega1**2*np.sin(delta)*np.cos(delta) 
                + g*np.sin(theta2)*np.cos(delta) 
                + L2*omega2**2*np.sin(delta)
                - 2*g*np.sin(theta1))/(2*L1 - L1*np.cos(delta)**2)

        domega2 = (-L2*omega2**2*np.sin(delta)*np.cos(delta)
                + 2*g*np.sin(theta1)*np.cos(delta)
                - 2*L1*omega1**2*np.sin(delta)
                - 2*g*np.sin(theta2))/(2*L2 - L2*np.cos(delta)**2)

        return dtheta1, domega1, dtheta2, domega2

    def solve(self, u0, T, dt, angle='rad'):
        """ A method for solving the ODE using SciPy. """
        if angle == 'deg':
            u0 = np.radians(u0)
        solution = solve_ivp(self,
                        (0, T), 
                        u0, 
                        t_eval=np.arange(0, T+dt, dt),
                        method='Radau')
        self.dt = dt
        self._t = solution.t
        self._theta1 = solution.y[0]
        self._theta2 = solution.y[2]

    @property
    def t(self):
        try:
            return self._t
        except AttributeError:
            raise SolveMethodNotCalled('Objektet har ingen t! ' \
                                    + 'Solve har ikke blitt kalt!')

    @property
    def theta1(self):
        try:
            return self._theta1
        except AttributeError:
            raise SolveMethodNotCalled('Objektet har ingen theta1! ' \
                                    + 'Solve har ikke blitt kalt!')

    @property
    def theta2(self):
        try:
            return self._theta2
        except AttributeError:
            raise SolveMethodNotCalled('Objektet har ingen theta2! ' \
                                    + 'Solve har ikke blitt kalt!')
    @property
    def x1(self):
        return self.L1*np.sin(self.theta1)
    
    @property
    def y1(self):
        return -self.L1*np.cos(self.theta1)

    @property
    def x2(self):
        return self.x1 + self.L2*np.sin(self.theta2)

    @property
    def y2(self):
        return self.y1 - self.L2*np.cos(self.theta2)
    
    @property
    def potential(self):
        P1 = self.M1*self.g*(self.y1 + self.L1)
        P2 = self.M2*self.g*(self.y2 + self.L1 + self.L2)
        return P1 + P2
    
    @property
    def vx1(self):
        return np.gradient(self.x1, self.t)

    @property
    def vx2(self):
        return np.gradient(self.x2, self.t)

    @property
    def vy1(self):
        return np.gradient(self.y1, self.t)

    @property
    def vy2(self):
        return np.gradient(self.y2, self.t)
    
    @property
    def kinetic(self):
        K1 = 0.5*self.M1*(self.vx1**2 + self.vy1**2)
        K2 = 0.5*self.M2*(self.vx2**2 + self.vy2**2)
        return K1 + K2


if __name__ == '__main__':
    dp = DoublePendulum()

    u0 = (np.pi + 0.000001, 0, 0, 0)
    T = 10
    dt = 1E-2

    dp.solve(u0, T, dt)
    
    plt.plot(dp.t, dp.potential,
            color='springgreen',
            label='Potential')
    plt.plot(dp.t, dp.kinetic,
            color='dodgerblue',
            label='Kinetic')
    total = dp.potential + dp.kinetic
    plt.plot(dp.t, total,
            color='darksalmon',
            label='Total')
    plt.title('Plot of the energies for a double pendulum')
    plt.xlabel('Time [$s$]')
    plt.ylabel('Energy [$J$]')
    plt.legend()
    plt.grid(True)
    plt.show()
    