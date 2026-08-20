# Overview
In this tutorial, Physics-Informed Neural Networks (PINNs) are used to reconstruct mean-flow using the first-order flow statistics. A PyTorch implementation of $[1]$ and the baseline used in $[2]$ is provided, where sparse observational data is used to reconstruct the mean velocity fields of the canonical setting of 2D periodic hills at a Reynolds number of 5600, where flow features such as separation, recirculation and reattachment can be observed. The sparse observational data is obtained from direct numerical simulation (DNS) data from $[3]$.

### References

- $[1]$ L. Sliwinski and G. Rigas, Mean flow reconstruction of unsteady flows using physics-informed neural
networks, Data-Centric Eng. 4, e4 (2023). https://doi.org/10.1017/dce.2022.37
- $[2]$ Y. Patel, V. Mons, O. Marquet, and G. Rigas, Turbulence model augmented physics-informed neural networks
for mean-flow reconstruction, Phys. Rev. Fluids 9, 034605 (2024). https://doi.org/10.1103/PhysRevFluids.9.034605
- $[3]$ H. Xiao, J. L. Wu, S. Laizet, and L. Duan, Flows over periodic hills of parameterized geometries: A
dataset for data-driven turbulence modeling from direct simulations, Comput. Fluids 200, 104431 (2020). https://doi.org/10.1016/j.compfluid.2020.104431

### Link to Dataset

- https://github.com/xiaoh/para-database-for-PIML
