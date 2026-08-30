# Overview
In this tutorial, Physics-Informed Neural Networks (PINNs) are used to reconstruct mean flow using the first-order flow statistics. A PyTorch implementation of methodology set out by Sliwinski and Rigas $[1]$ has been provided, where sparse observational data is used to reconstruct the mean velocity fields of the canonical setting of 2D periodic hills at a Reynolds number of 5600, where flow features such as separation, recirculation and reattachment can be observed. The sparse observational data has been obtained from direct numerical simulation (DNS) data from Xiao et al. $[3]$.

### Learning Objectives

1. Understand the methodology behind PINNs and their use in mean flow reconstruction from sparse observational data.
2. Create and load the data required to train a PINN.
3. Tune the hyperparameters of a PINN using a simple grid search.
4. Train and post-process a PINN, and validate its performance by comparing the results with DNS data. 

### References

- $[1]$ L. Sliwinski and G. Rigas. (2023). Mean flow reconstruction of unsteady flows using physics-informed neural
networks, Data-Centric Eng. 4, e4. https://doi.org/10.1017/dce.2022.37
- $[2]$ Y. Patel, V. Mons, O. Marquet, and G. Rigas. (2024). Turbulence model augmented physics-informed neural networks
for mean-flow reconstruction. Phys. Rev. Fluids 9, 034605. https://doi.org/10.1103/PhysRevFluids.9.034605
- $[3]$ H. Xiao, J. L. Wu, S. Laizet, and L. Duan. (2020). Flows over periodic hills of parameterized geometries: A
dataset for data-driven turbulence modeling from direct simulations. Comput. Fluids 200, 104431. https://doi.org/10.1016/j.compfluid.2020.104431

### Link to Dataset

- https://github.com/xiaoh/para-database-for-PIML
