import matplotlib.pyplot as plt
import numpy as np
from satellite import Satellite
from typing import List

def plot_position(satellites:List[Satellite], times:np.ndarray):
    # Plot graphics and return coordinates in ECI frame
    for idx,sat in enumerate(satellites):
        fig,axs = plt.subplots(3,sharex=True,sharey=True)
        
        X,Y,Z = sat.unpack_position()

        if sat.name:
            fig.suptitle(f"Position of satellite {sat.name}")
        else:
            fig.suptitle(f"Position of satellite {idx}")

        axs[0].plot(times/3600,X)
        axs[0].set_ylabel("X (km)")
        
        axs[1].plot(times/3600,Y)
        axs[1].set_ylabel("Y (km)")

        axs[2].plot(times/3600,Z)
        axs[2].set_ylabel("Z (km)")
        axs[2].set_xlabel("Time (h)")

        plt.show()


def plot_altitude(sat:Satellite, times:np.ndarray, R: float):
    X,Y,Z = sat.unpack_position()

    plt.figure(2)
    plt.title("Altitude")
    alt = [np.sqrt(X[i]**2 + Y[i]**2 + Z[i]**2) - R for i in range(len(times))]
    plt.plot(times/(3600*24), alt)
    plt.xlabel("Time (days)")
    plt.ylabel("Altitude (km)")
    plt.ylim(bottom=0)

def plot3d(satellites:List[Satellite], times:np.ndarray):
    tri = plt.figure(33)
    ax = tri.add_subplot(111,projection='3d')
    tri.suptitle("Position 3D")

    for idx,sat in enumerate(satellites):    
        X,Y,Z = sat.unpack_position()
        limits = get_max_limits(X,Y,Z)

        if sat.name:
            ax.plot(X,Y,Z, label=sat.name)
        else:
            ax.plot(X,Y,Z, label=f"Satellite {idx}")
        
        ax.set_xlim(limits)
        ax.set_ylim(limits)
        ax.set_zlim(limits)

    plt.legend()
    plt.show()

def plot_error(satellites:List[Satellite], times:np.ndarray):
    sat_leader = satellites[0]
    X0,Y0,Z0 = sat_leader.unpack_position()

    # Plot graphics and return coordinates in ECI frame
    for idx,sat in enumerate(satellites[1:]):
        fig,axs = plt.subplots(3,sharex=True,sharey=True)
        X,Y,Z = sat.unpack_position()

        if sat.name:
            fig.suptitle(f"Error position of satellite {sat.name}")
        else:
            fig.suptitle(f"Error position of satellite {idx+1}")

        X_error = [x-x0 for x,x0 in zip(X,X0)]
        Y_error = [y-y0 for y,y0 in zip(Y,Y0)]
        Z_error = [z-z0 for z,z0 in zip(Z,Z0)]

        axs[0].plot(times/3600, X_error)
        axs[0].set_ylabel("\u0394X (km)")
        
        axs[1].plot(times/3600, Y_error)
        axs[1].set_ylabel("\u0394Y (km)")

        axs[2].plot(times/3600, Z_error)
        axs[2].set_ylabel("\u0394Z (km)")

        tri = plt.figure(23)
        ax = tri.add_subplot(111,projection='3d')
        tri.suptitle("Error position 3D")
        if sat.name:
            ax.plot(X_error,Y_error,Z_error, label=sat.name)
        else:
            ax.plot(X_error,Y_error,Z_error, label=f"Satellite {idx}")

        plt.show()

def get_max_limits(X:float,Y:float,Z:float):
    limit = max(max(X),max(Y),max(Z))
    limits = [-limit, limit]

    return limits