from orbit import Orbit
import orbit
import numpy as np

class Satellite():
    def __init__(self, orbit:Orbit, mass:float=100, cd:float =2.2, area:float=1):
        self.orbit= orbit
        self.mass = mass
        self.cd   = cd
        self.area = area
        self.X=[];self.Y=[];self.Z=[]
        self.Vx=[];self.Vy=[];self.Vz=[]

    def save_state(self,solution:np.ndarray):
        if self.X is None:
            self.X=[];self.Y=[];self.Z=[]
            self.Vx=[];self.Vy=[];self.Vz=[]    
    
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


if __name__ == "__main__":
    r0 = [-2384.46, 5729.01, 3050.46]
    v0 = [-7.36138, 2.98997, 1.64354]
    orbita = orbit.OrbitStateVector(r0,v0)

    sat = Satellite(orbita)

    print(sat.mass)