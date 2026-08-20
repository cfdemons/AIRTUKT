import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import torch
from scipy.interpolate import griddata

def gen_hill_points(input, alpha=1., bottom_flat_length=5.142):
    'Calculate the shape of the periodic hill'

    streamwise_length = (3.858*alpha+bottom_flat_length)
    x = np.array(np.copy(input)).reshape(-1,1)*28.0
    y = np.copy(x)
    h = np.zeros_like(x)
    
    
    for i in range(x.shape[0]):

        if (x[i] > streamwise_length*28.0/2.0):
            x[i] = (streamwise_length*28.0/2.0) - (x[i] - (streamwise_length*28.0/2.0))
        
        if (x[i]/alpha>=0) and (x[i]/alpha<9):
            h[i] = np.minimum(28., 2.8e+01 + 0.0e+00*(x[i]/alpha) + \
                              6.775070969851e-03*(x[i]/alpha)**2 - 2.124527775800e-03*(x[i]/alpha)**3)
        elif (x[i]/alpha>=9) and (x[i]/alpha<14):
            h[i] = 2.507355893131E+01 + 9.754803562315E-01*(x[i]/alpha) - \
                   1.016116352781E-01*(x[i]/alpha)**2 + 1.889794677828E-03*(x[i]/alpha)**3
        elif (x[i]/alpha>=14) and (x[i]/alpha<20):
            h[i] = 2.579601052357E+01 + 8.206693007457E-01*(x[i]/alpha) - \
                   9.055370274339E-02*(x[i]/alpha)**2 + 1.626510569859E-03*(x[i]/alpha)**3
        elif (x[i]/alpha>=20) and (x[i]/alpha<30):
            h[i] = 4.046435022819E+01 - 1.379581654948E+00*(x[i]/alpha) + \
                   1.945884504128E-02*(x[i]/alpha)**2 - 2.070318932190E-04*(x[i]/alpha)**3
        elif (x[i]/alpha>=30) and (x[i]/alpha<40):
            h[i] = 1.792461334664E+01 + 8.743920332081E-01*(x[i]/alpha) - \
                   5.567361123058E-02*(x[i]/alpha)**2 + 6.277731764683E-04*(x[i]/alpha)**3
        elif (x[i]/alpha>=40) and (x[i]/alpha<=54):
            h[i] = np.maximum(0., 5.639011190988E+01 - 2.010520359035E+00*(x[i]/alpha) + \
                              1.644919857549E-02*(x[i]/alpha)**2 + 2.674976141766E-05*(x[i]/alpha)**3)                             
        else:
            h[i] = 0
    hout = h/28.0
    xout = y/28.0
    return np.concatenate((xout, hout),axis=1)


def gen_sparse_grid(dx, dy, dns_data, dist_from_top=0., dist_from_inlet = 0., alpha=1., bottom_flat_length=5.142, domain_height=3.036):

    #Creates a grid of sparse collocated points used

    streamwise_length = (3.858*alpha+bottom_flat_length) - dist_from_inlet # Streamwise length not including distance away from inlet

    nx = math.floor((streamwise_length)/dx) # Defines the maximum number of points in the x-axis (nx+1)
    X = np.linspace(0+dist_from_inlet,dx*nx, (nx+1)).reshape(-1,1)
    
    output = np.empty((0,2))
    domain_height_top = domain_height - dist_from_top # Domain height not including distance away from top wall
    dns_points = dns_data[['x','y']].to_numpy()

    for i in range(X.shape[0]):

        hill_point = gen_hill_points(X[i].item(), alpha, bottom_flat_length)

        ny = math.floor((domain_height_top-hill_point[:,1].item())/dy)


        Y_points = np.linspace(domain_height_top,domain_height_top-(dy*ny), (ny+1))
        X_points = np.full(Y_points.shape, X[i].item())
        new_points = np.stack((X_points,Y_points),axis=1)
        output = np.append(output, new_points, axis=0)

    #Find index of points in dns data that are closest to centroid of KMean clusters
    distances = np.linalg.norm((dns_points[:, None, :]-output), axis=2)

    index_vector = np.argmin(distances, axis=0)
    sparse_points = dns_data.iloc[index_vector]
    
    return sparse_points[['x','y']].to_numpy(), sparse_points[['u_mean','v_mean']].to_numpy()

def is_inside_domain(x_data, y_data, alpha=1., bottom_flat_length=5.142, domain_height=3.036, eps=0.):

    #Returns True if data is inside computational domain and returns False otherwise

    y_bottom = gen_hill_points(x_data, alpha, bottom_flat_length)[:,1]
    y_bottom = y_bottom.reshape(-1)
    y_top = np.full((y_data.shape),domain_height)

    return (y_data >= y_bottom+eps) & (y_data <= y_top-eps)

def plot_computational_domain(alpha=1.0, bottom_flat_length=5.142, domain_height=3.036):
    
    streamwise_length = (3.858*alpha+bottom_flat_length)
    x_hill = np.linspace(0, streamwise_length, 5000)
    hill_points = gen_hill_points(x_hill, alpha, bottom_flat_length)
    x_hill = hill_points[:,0]
    y_hill = hill_points[:,1]
    inlet = np.array([[0, 0], [1, domain_height]])
    outlet = np.array([[streamwise_length, streamwise_length], [1, domain_height]])
    top = np.array([[0, streamwise_length], [domain_height, domain_height]])
    plt.plot(x_hill, y_hill, 'k')
    plt.plot(inlet[0], inlet[1], 'k')
    plt.plot(outlet[0], outlet[1], 'k')
    plt.plot(top[0], top[1], 'k')

    None

def print_loss_stats(model, epoch, iter, is_adam=False, is_lbfgs=False):

    if is_adam:
        print(f'ADAM Epoch: {epoch}, Total Loss (Log10):  {round(np.log10(model.losses[-1]).item(), 4)}')

    if is_lbfgs:
        print(f'L-BFGS Iteration: {iter}, Total Loss (Log10):  {round(np.log10(model.losses[-1]).item(), 4)}')

    print(f'PDE Loss (Log10): {round(np.log10(model.pde_losses[-1]), 4)},',
          f'Data Loss (Log10): {round(np.log10(model.data_losses[-1]), 4)},',
          f'Wall Loss (Log10): {round(np.log10(model.wall_losses[-1]), 4)},',
          f'Periodic Inlet/Outlet BC Loss (Log10): {round(np.log10(model.periodic_losses[-1]),4)},',
          f'Mass Flow Inlet BC Loss (Log10): {round(np.log10(model.massflow_losses[-1]),4)}'
    )

    return None

def compare_flow_fields(X, Y, U_approx, U_exact, V_approx, V_exact, sparse_data, domain_height=3.036):
    
    U_l2 = abs(U_exact - U_approx)**2
    V_l2 = abs(V_exact - V_approx)**2
    
    plt.figure(figsize=(24,10))
    plt.subplot(231)

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = U_approx, cmap='viridis')
    plt.colorbar()
    plt.plot(sparse_data[:,0], sparse_data[:,1],'ro' ,markersize=2)
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)
    plt.ylabel('$y/H$')
    plt.title(r'Approximate Mean $\overline{U}$ Velocity (PINN)')

    plt.subplot(232)

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = U_exact, cmap='viridis')
    plt.colorbar()
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)

    plt.title(r'Exact Mean $\overline{U}$ Velocity (DNS)')

    plt.subplot(233)

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = U_l2, cmap='viridis')
    plt.colorbar()
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)

    plt.title(r'L2 Error For Mean $\overline{U}$ Velocity (PINN)')


    plt.subplot(234)

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = V_approx, cmap='viridis')
    plt.colorbar()
    plt.plot(sparse_data[:,0], sparse_data[:,1],'ro' ,markersize=2)
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)
    plt.ylabel('$y/H$')
    plt.xlabel('$x/H$')
    plt.title(r'Approximate Mean $\overline{V}$ Velocity (PINN)')

    plt.subplot(235)

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = V_exact, cmap='viridis')
    plt.colorbar()
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)
    plt.xlabel('$x/H$')
    plt.title(r'Exact Mean $\overline{V}$ Velocity (DNS)')


    plt.subplot(236)

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = V_l2, cmap='viridis')
    plt.colorbar()
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)
    plt.xlabel('$x/H$')
    plt.title(r'L2 Error For Mean $\overline{V}$ Velocity (PINN)')

    plt.tight_layout()

    return None

def plot_streamwise_profile(X, Y, U_approx, U_exact, domain_height=3.036, dx=0.75):

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = U_approx, cmap='viridis')
    plt.colorbar()

    plot_computational_domain()

    x = 0.

    plt.plot(x+U_exact[torch.isclose(X,torch.Tensor([x]))], Y[torch.isclose(X,torch.Tensor([x]))],'-',c='k', label='DNS Solution')
    plt.plot(x+U_approx[torch.isclose(X,torch.Tensor([x]))], Y[torch.isclose(X,torch.Tensor([x]))],'--' ,c='r', label='PINN Solution')

    x += dx
    
    while x < 9.:
        
        #Plot streamwise velocity at x = x + dx until end of streamwise length is reached
        
        plt.plot(x+U_exact[torch.isclose(X,torch.Tensor([x]))], Y[torch.isclose(X,torch.Tensor([x]))],'-',c='k')
        plt.plot(x+U_approx[torch.isclose(X,torch.Tensor([x]))], Y[torch.isclose(X,torch.Tensor([x]))],'--' ,c='r')
        
        x += dx

    plt.ylabel('$y/H$')
    plt.xlabel('$x/H$')
    plt.title(r'Approximate Mean $\overline{U}$ Velocity (PINN) with Streamwise Velocity Profiles')
    plt.legend(loc=(0.9,-0.15))

    return None

def plot_recirculation_streamline(X, Y, U_approx, U_exact, nx=500, ny=750, domain_height = 3.036, eps=0.):

    x = np.linspace(min(X),max(X),nx)
    y = np.linspace(min(Y),max(Y),ny)

    x_grid, y_grid = np.meshgrid(x, y)
    XY_grid = np.stack((x_grid.flatten(),y_grid.flatten()),axis=1)

    not_in_domain_indices = is_inside_domain(XY_grid[:,0],XY_grid[:,1],eps=eps)

    U_approx_grid=griddata(np.stack((X,Y),axis=1),U_approx,XY_grid[not_in_domain_indices])
    U_exact_grid=griddata(np.stack((X,Y),axis=1),U_exact,XY_grid[not_in_domain_indices])

    grid_approx = -10*np.ones_like(x_grid.flatten())
    grid_exact = -10*np.ones_like(x_grid.flatten())

    grid_approx[not_in_domain_indices] = U_approx_grid
    grid_exact[not_in_domain_indices] = U_exact_grid

    plt.rc('lines', markersize=1)
    plt.scatter(X,Y, c = U_approx, cmap='viridis')
    plt.colorbar()
    plt.contour(x_grid,y_grid, grid_exact.reshape(x_grid.shape), levels=[0.], colors='k', linewidths=1.25)
    plt.contour(x_grid,y_grid, grid_approx.reshape(x_grid.shape), levels=[0.], colors='r', linewidths=1.25, linestyles = 'dashed')
    plot_computational_domain()
    plt.ylim(0.,domain_height)
    plt.xlim(0.,9.)
    plt.xlabel('$x/H$')
    plt.ylabel('$y/H$')
    plt.title(r'Approximate Mean $\overline{U}$ Velocity (PINN) With Streamline Dividing Recirculation Zone')
    
    return None

def plot_streamlines(X, Y, U_approx, U_exact):
    
    plt.figure(figsize=(16,5))
    plt.subplot(121)
    plot_streamwise_profile(X, Y, U_approx, U_exact)
    plt.subplot(122)
    plot_recirculation_streamline(X, Y, U_approx, U_exact)
    plt.tight_layout()

    return None