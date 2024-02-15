# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# # Orbital Mechanics and Control
# ## Import Packages

# %%
import orbit
from satellite import Satellite
from dynamics import equation_of_motion
from plots import *

import numpy as np
from scipy.integrate import ode, DOP853
from math import pi

# %% [markdown]
# ## Input variables
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
# Curtis - Example 4.3
a = 6578
e = 0.1712
i = 0
w = 20.07
RA = 255.3
TA = 28.45

orbit0 = orbit.OrbitElements(a,e,i,w,RA,TA)
orbit1 = orbit.OrbitElements(a,e,i+50,w,RA,TA)

R, mu = orbit0.get_central_body()       # Get central body according to orbit
orbit0.activate_perturbation(["J2"])  # Select perturbations
orbit1.activate_perturbation(["J2"])  # Select perturbations

sat0 = Satellite(orbit0,name="Leader")
sat1 = Satellite(orbit1,name="follower")

satellites = [sat0, sat1]

# %% [markdown]
# ## Time setup

# %%
# Define simulation time in seconds
t0        = 0
time_end  = 3600*24
time_step = 10
times     = np.arange(0,time_end,step=time_step)

# %% [markdown]
# ## Linear Control

# %%
# Tune control law used
Kp = 0
Ki = 0
Kd = 0

# %% [markdown]
# ## Simulation

# %%
# Simulate orbit
from typing import List
first = ode(equation_of_motion)
second = ode(equation_of_motion)
list_solver = [first, second]

for sat, solver in zip(satellites,list_solver):
    solver.set_integrator('DOP853')
    solver.set_f_params(sat.get_orbit(),sat)
    solver.set_initial_value(sat.get_orbit().get_initial_state(),t0)
    
for time in times:
    for sat,solver in zip(satellites,list_solver):
        solver.integrate(time)

        sat.save_state(solver.y)

# %% [markdown]
# ## Plots

# %%
plot_error(satellites,times)

# %%
plot3d(satellites,times)


