import numpy as np
from central_body import CentralBody, get_solar_system_data
from typing import Literal

class Orbit():
    def __init__(self):
        # Central body definition
        # Earth as default
        self.R  = 6_378     # km
        self.mu = 398_600   # km3/s2
        self.we   = 7.2921159e-5 # Earth's angular velocity

        self.Drag = False
        self.J2   = False
        
        self.initialize()

    def initialize(self):
        raise NotImplementedError(f"initialize() not implemented in {self.__class__.__name__}")

    def change_central_body(self,new_central_body: CentralBody):
        solar_system_data = get_solar_system_data()
        
        self.R  = solar_system_data[new_central_body]["R"]
        self.mu = solar_system_data[new_central_body]["mu"]
        print(f"New central body: {new_central_body}") 
        print(f"Radius {self.R} km")
        print(f"Gravitational Parameter {self.mu} km3/s2")
        self.initialize()

    def get_central_body(self):
        """
        Return the radius and gravitational parameter of the central body
        for this orbit
        """
        return self.R, self.mu

    def activate_perturbation(self,perturbation: Literal["Drag","J2"]):
        if "Drag" in perturbation:
            self.Drag = True
            print("Using atmospheric drag.")

        if "J2" in perturbation:
            self.J2 = True
            print("Using Earth Oblateness J2")
        
    def deactivate_perturbation(self,perturbation: Literal["Drag","J2"]):
            if "Drag" in perturbation:
                self.Drag = False
                print("Not using atmospheric drag.")

            if "J2" in perturbation:
                self.J2 = False
                print("Not using Earth Oblateness J2")

class OrbitElements(Orbit):
    def __init__(self,a,e,i,w,RA,TA):
        """
        Classical Elements:
        a:  Semimajor-axis                        (km)
        e:  Eccentricity
        i:  Inclination                           (deg)
        w:  Argument of perigee                   (deg)
        RA: Right Ascencion of the Ascending Node (deg)
        TA: True Anomaly                          (deg)
        """
        self.a  = a
        self.e  = e
        self.i  = np.deg2rad(i)
        self.w  = np.deg2rad(w)
        self.RA = np.deg2rad(RA)
        self.TA = np.deg2rad(TA)
        super().__init__()

    
    def initialize(self):
        """
        Convert the classical elements to
        the state vector:
        X = [x,y,z,vx,vy,vz]

        Can be initialized in the following arrangements:
        x,y,z,vx,vy,vz
        [x,y,z],[vx,vy,vz]
        [x,y,z,vx,vy,vz]
        """
        h = np.sqrt(self.mu * self.a * np.absolute(1 - self.e**2))

        r_perifocal = (h**2 / (self.mu * (1 + self.e*np.cos(self.TA)))) * np.array([np.cos(self.TA),np.sin(self.TA),0])
        v_perifocal = (self.mu / h) * np.array([-np.sin(self.TA), (self.e + np.cos(self.TA)), 0])

        def rotation_Z(angle_radians): 
            return np.array([[np.cos(angle_radians), np.sin(angle_radians), 0],
                                [-np.sin(angle_radians), np.cos(angle_radians), 0],
                                [0, 0, 1]])
        def rotation_X(angle_radians):
            return np.array([[1, 0, 0],
                                [0, np.cos(angle_radians), np.sin(angle_radians)],
                                [0, -np.sin(angle_radians), np.cos(angle_radians)]])
    
        Q = (rotation_Z(self.w) @ rotation_X(self.i) @ rotation_Z(self.RA)).T
        
        r_ECI = Q @ r_perifocal
        v_ECI = Q @ v_perifocal
        
        self.initial_state = np.concatenate((r_ECI,v_ECI),axis=0)

        print("Initial condition")
        print(f"Position: {r_ECI}")
        print(f"Velocity: {v_ECI}\n")
        print(f"State Vector: {self.initial_state}\n")


class OrbitStateVector(Orbit):
    def __init__(self,*args):
        """
        State Vector:
        X = [x,y,z,vx,vy,vz]
        """
        super().__init__()
        if len(args) == 6:
            self.initial_state = np.array(args, dtype=float)
        elif len(args) == 2 and all(len(arg) == 3 for arg in args):
            self.initial_state = np.concatenate(args)
        elif len(args) == 1 and len(args[0]) == 6:
            self.initial_state = args[0]
        else:
            raise ValueError("Invalid input format.\nPlease provide 6 float values, 2 arrays of 3 elements each, or 1 array of 6 elements.")

    def initialize(self):
        pass


if __name__ == "__main__":
    # Problem 4.4 from Curtis 3rd Edition
    a  = 25384
    e  = 1.298
    i  = 90
    w  = 344.9
    RA = 51.34
    TA = 285.1
    orbit1 = OrbitElements(a,e,i,w,RA,TA)

    orbit2 = OrbitStateVector([0,0,-13000,4,5,6])

