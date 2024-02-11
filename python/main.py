# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import orbit
from satellite import Satellite
import numpy as np
from scipy.integrate import DOP853, ode
import matplotlib.pyplot as plt
from dynamics import equation_of_motion

# %% [markdown]
# Initialize Orbit using one of the following methods:
# - Classical Elements
# - State Vector
# 
# If necessary, implement the conversion to State Vector for the following:
# - Delaunay Elements
# - Equinoctial Elements
# 
# These functionalities should be added from the Orbit abstract class in orbit.py

# %%
# Input variables into Orbit class from classical 
# orbital elements or position and velocity
a  = 6378 + 480
e  = 0.01
i  = 2
w  = 30
RA = 45
TA = 40
orbit1 = orbit.OrbitElements(a,e,i,w,RA,TA)

# Get central body according to orbit
R, mu = orbit1.get_central_body()

# Select perturbations
orbit1.activate_perturbation([])

# Satellite in orbit
sat1 = Satellite()

# %% [markdown]
# Simulation set up

# %%
# Define simulation time (s)
time_end  = 12*3600
step      = 10
times     = np.linspace(0,time_end,1000)

# Tune control law used
Kp = 0
Ki = 0
Kd = 0

# %% [markdown]
# Simulation

# %%
# Simulate orbit
solver  = ode(equation_of_motion)
solver.set_integrator('DOP853')
solver.set_f_params(orbit1,sat1)
solver.set_initial_value(orbit1.initial_state,0)

X=[];Y=[];Z=[];Vx=[];Vy=[];Vz=[]

for time in times:
    solver.integrate(time)
    X.append(solver.y[0])
    Y.append(solver.y[1])
    Z.append(solver.y[2])
    Vx.append(solver.y[3])
    Vy.append(solver.y[4])
    Vz.append(solver.y[5])



# %%
# Plot graphics and return coordinates in ECI frame

plt.figure(1)
plt.subplot(311)
plt.plot(times/3600,X,label='X')
plt.ylim([-7_000,7_000])
plt.legend()

plt.subplot(312)
plt.plot(times/3600,Y,label='Y')
plt.ylim([-7_000,7_000])
plt.ylabel("Position (km)")
plt.legend()

plt.subplot(313)
plt.plot(times/3600,Z,label='Z')
plt.ylim([-7_000,7_000])
plt.xlabel("Time (h)")
plt.legend()

tri = plt.figure(3)
ax = tri.add_subplot(111,projection='3d')
ax.plot(X,Y,Z, label='3D')
ax.set_xlim((-7000,7000))
ax.set_ylim((-7000,7000))
ax.set_zlim((-7000,7000))
ax.legend()

plt.show()



# %%
