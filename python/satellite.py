from orbit import Orbit
import orbit
import numpy as np

class Satellite():
    def __init__(self, orbit:Orbit, name:str="",mass:float=100, cd:float=2.2, area:float=1):
        self.orbit= orbit
        self.name = name
        self.mass = mass
        self.cd   = cd
        self.area = area
        self.X=[];self.Y=[];self.Z=[]
        self.Vx=[];self.Vy=[];self.Vz=[]

    def get_orbit(self):
        return self.orbit

    def save_state(self,solution:np.ndarray):
        X  = solution[0]
        Y  = solution[1]
        Z  = solution[2]
        Vx = solution[3]
        Vy = solution[4]
        Vz = solution[5]

        self.X.append(X)
        self.Y.append(Y)
        self.Z.append(Z)
        self.Vx.append(Vx)
        self.Vy.append(Vy)
        self.Vz.append(Vz)

    def get_state(self):
        return [self.X,self.Y,self.Z,self.Vx,self.Vy,self.Vz]

    def unpack_position(self):
        # Unpack positions
        X,Y,Z,*rest = self.get_state()
        return X,Y,Z

    def unpack_velocity(self):
        # Unpack positions
        X,Y,Z,Vx,Vy,Vz = self.get_state()
        return Vx,Vy,Vz

if __name__ == "__main__":
    r0 = [-2384.46, 5729.01, 3050.46]
    v0 = [-7.36138, 2.98997, 1.64354]
    orbita = orbit.OrbitStateVector(r0,v0)

    sat = Satellite(orbita)

    print(sat.mass)