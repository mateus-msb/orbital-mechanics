# Orbital Mechanics

## Overview
This repository aims to analyze the performance and numerical precision of an orbit propagator, incorporating simple perturbations (Atmospheric Drag and J2), while also facilitating the implementation of control laws in Python and Julia.

## Next Steps (14.02)
### General
- [ ] Document functions
- [ ] Document classes
- [ ] Cite references to each function
- [ ] Cite references to each equation


### Python 
- [x] Implement J2 Perturbation (14.02)
- [x] Implement multiple satellites (14.02)
- [x] Fix multiple satellites plots (14.02)
- [x] Implement error plot (15.02)
- [x] Implement relative orbits
- [ ] Implement time axis in plots
- [ ] Insert control law
- [ ] Input from .txt file
- [ ] Output to results/


### Julia
- [ ] Create structs (Orbit, Satellites, etc.)
- [ ] Implement basic orbit (ODE)
- [ ] Implement orbital perturbations
- [ ] Input from .txt file
- [ ] Output to results/


## References
The codes in this repository are based on the following references:
- Howard D. Curtis, "Orbital Mechanics for Engineering Students", 3rd Edition
- S. Mathavaraj & Radhakant Padhi, "Satellite Formation Flying: High Precision Guidance using Optimal and Adaptive Control Techniques"