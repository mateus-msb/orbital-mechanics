import numpy as np
from satellite import Satellite
from orbit import Orbit


def equation_of_motion(t,y,Orbit: Orbit,Satellite: Satellite):
        """
        Input variables:
        t:  time (to be used by the ODE solver)
        y:  state [X,Y,Z,vx,vy,vz]
        dy: state [vx,vy,vz,ax,ay,az]

        This function uses the Encke's method for
        orbital perturbations
        """
        
        """
        Variables (ECI):
        r:  position vector [X,Y,Z]
        v:  velocity vector [vx,vy,vz]
        r_norm: Euclidean norm of the position vector
        v_norm: Euclidean norm of the velocity vector
        
        R:  Radius of the central body
        mu: Gravitational parameter of the central body
        we: Central body radial velocity

        a0:     acceleration caused by the main gravitational forces
        a_drag: acceleration caused by the atmospheric drag
        a_J2:   acceleration caused by the central body oblateness (J2)
        """

        X,Y,Z,vx,vy,vz = y

        R  = Orbit.R
        mu = Orbit.mu
        we = np.array([0,0,Orbit.we])
        drag = Orbit.Drag
        J2   = Orbit.J2

        r = np.array([X,Y,Z])
        v = np.array([vx,vy,vz])
        r_norm = np.sqrt(X**2 + Y**2 + Z**2)

        a0 = -(mu/r_norm**3)*r
        a = a0

        if drag:
            a = a + a_drag(r,v,we,R,Satellite)

        if J2:
            a = a + a_J2(r,r_norm,R,mu,J2)
        
        dy = np.concatenate((v,a))
        return dy


def a_drag(r: np.ndarray,v: np.ndarray, we: np.ndarray, R: float, Satellite: Satellite):
    mass = Satellite.mass
    cd   = Satellite.cd
    area = Satellite.area

    r_norm = np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)

    Vrel        = v - np.cross(we,r)
    Vrel_norm   = np.sqrt(Vrel[0]**2 + Vrel[1]**2 + Vrel[2]**2)
    Vrel_versor = Vrel / Vrel_norm
    
    altitude = r_norm - R
    rho      = atmosphere(altitude)

    a_drag = - 0.5 * (cd*area/mass) * rho * (1000*Vrel_norm)**2 * Vrel_versor / 1000
    return a_drag


def a_J2(r: np.ndarray,r_norm: float, R: float, mu: float, J2: float):
    X,Y,Z = r
    
    fac = 3/2*J2*(mu/r_norm**2)*(R/r_norm)**2
    vec = np.array([(1 - 5*(Z/r_norm)**2)*(X/r_norm), (1 - 5*(Z/r_norm)**2)*(Y/r_norm), (3 - 5*(Z/r_norm)**2)*(Z/r_norm)])
    a_J2 = - fac*vec
    return a_J2


def atmosphere(z):
    """
    U.S. Standard Atmosphere 1976
    Curtis - D.41
    """
    # Geometric altitudes (km)
    h = np.array([0, 25, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140,
                  150, 180, 200, 250, 300, 350, 400, 450, 500, 600, 700, 800,
                  900, 1000])
    
    # Corresponding densities (kg/m^3) from USSA76
    r = np.array([1.225, 4.008e-2, 1.841e-2, 3.996e-3, 1.027e-3, 3.097e-4,
                  8.283e-5, 1.846e-5, 3.416e-6, 5.606e-7, 9.708e-8, 2.222e-8,
                  8.152e-9, 3.831e-9, 2.076e-9, 5.194e-10, 2.541e-10, 6.073e-11,
                  1.916e-11, 7.014e-12, 2.803e-12, 1.184e-12, 5.215e-13, 1.137e-13,
                  3.070e-14, 1.136e-14, 5.759e-15, 3.561e-15])
    
    # Scale heights (km)
    H = np.array([7.310, 6.427, 6.546, 7.360, 8.342, 7.583, 6.661, 5.927, 5.533,
                  5.703, 6.782, 9.973, 13.243, 16.322, 21.652, 27.974, 34.934,
                  43.342, 49.755, 54.513, 58.019, 60.980, 65.654, 76.377, 100.587,
                  147.203, 208.020])
    
    # Handle altitudes outside of the range
    if z > 1000:
        z = 1000
    elif z < 0:
        z = 0
    
    # Determine the interpolation interval
    for j in range(27):
        if z >= h[j] and z < h[j + 1]:
            i = j
    
    if z == 1000:
        i = 26
    
    # Exponential interpolation
    density = r[i] * np.exp(-(z - h[i]) / H[i])
    
    return density