Lumerical photonic inverse design module lumopt2
================================================

As photonic components become increasingly complex, traditional design cycles involving manually varying a small set of parameters become less effective in finding the optimal device design. While parameter sweeps and traditional optimization techniques allows for further exploration of the design space, the time required exponentially increases as the number of design parameters increase. Towards that end, specialized methods are required to anticipate strong candidates which allows for faster convergence towards a satisfactory design.

The Lumerical photonic inverse design module is a Python module included within Lumerical FDTD is built for efficient optimization of photonic components. Leveraging the adjoint method, you can calculate the gradient with respect to all parameters with only two FDTD simulations, enabling you to quickly adjust your design to achieve specified figures of merit.

With only simple Python scripting, you can set up an optimization session based on an FDTD simulation, map simulation parameters to optimization parameters, and run the inverse design with a variety of resources.

