import numpy as np

DEFAULT_SIGMA = 10.0
DEFAULT_RHO = 28.0
DEFAULT_BETA = 8.0 / 3.0


def lorenz_derivative(state, sigma, rho, beta):
    x, y, z = state
    dx = sigma * (y - x)
    dy = x * (rho - z) - y
    dz = x * y - beta * z
    return np.array([dx, dy, dz], dtype=np.float64)


def rk4_step(state, dt, sigma, rho, beta):
    k1 = lorenz_derivative(state, sigma, rho, beta)
    k2 = lorenz_derivative(state + 0.5 * dt * k1, sigma, rho, beta)
    k3 = lorenz_derivative(state + 0.5 * dt * k2, sigma, rho, beta)
    k4 = lorenz_derivative(state + dt * k3, sigma, rho, beta)

    return state + (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)


class LorenzSystem:
    def __init__(
        self,
        initial_state=(1.0, 1.0, 1.0),
        sigma=DEFAULT_SIGMA,
        rho=DEFAULT_RHO,
        beta=DEFAULT_BETA,
        dt=0.005,
        max_points=10000
    ):
        self.sigma = sigma
        self.rho = rho
        self.beta = beta
        self.dt = dt

        self.state = np.array(initial_state, dtype=np.float64)
        self.max_points = max_points
        self.trajectory = np.zeros((max_points, 3), dtype=np.float32)
        self.count = 0

    def step(self):
        self.state = rk4_step(
            self.state,
            self.dt,
            self.sigma,
            self.rho,
            self.beta
        )
        #this will keep count growing, but the index within 0 to max_points
        idx = self.count % self.max_points
        self.trajectory[idx] = self.state.astype(np.float32)
        self.count += 1

        
        if self.count < self.max_points:
            self.trajectory[self.count] = self.state.astype(np.float32)
            self.count += 1

    def reset(self, new_initial_state=None):
        if new_initial_state is not None:
            self.state = np.array(new_initial_state, dtype=np.float64)
        self.count = 0

    def get_points(self):
        if self.count < self.max_points:
            return self.trajectory[:self.count]
        return self.trajectory
