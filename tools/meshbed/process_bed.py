import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np
import pandas as pd
import scipy.interpolate

plt.style.use('dark_background')

file = pd.read_csv('probedata_example.txt', sep=' ')

data = np.asarray(file)[:,0:3]

data = data[0::2,:]

X, Y = np.meshgrid(np.unique(data[:,0]), np.unique(data[:,1]))

Z = scipy.interpolate.griddata((data[:,0],data[:,1]),data[:,2],(X,Y), method='nearest')

#Regression
mx = len(np.unique(data[:,0]))
my = len(np.unique(data[:,1]))
m = mx * my
Xp = np.hstack(   ( np.reshape(X, (m, 1)) , np.reshape(Y, (m, 1)) ) )
Xp = np.hstack(   ( np.ones((m, 1)) , Xp ))
Zp = np.reshape(Z, (m, 1))

theta = np.dot(np.dot( np.linalg.pinv(np.dot(Xp.transpose(), Xp)), Xp.transpose()), Zp)

plane = np.reshape(np.dot(Xp, theta), (my, mx))
Z_delta = Z-plane

Xc = X.flatten()
Yc = Y.flatten()
A = np.array([Xc*0+1,Xc, Yc, Xc**2, Xc**2*Yc, Xc**2*Yc**2, Yc**2, Xc*Yc**2, Xc*Yc]).T
B = Z.flatten()
coeff, r, rank, s = np.linalg.lstsq(A, B, rcond=None)
curve = np.reshape(np.dot(A,coeff), (my, mx))

A = np.array([Xc*0+1,Xc, Yc, Xc*Yc]).T
coeff, r, rank, s = np.linalg.lstsq(A, B, rcond=None)
twist = np.reshape(np.dot(A,coeff), (my, mx))

fits = [('plane',plane), ('twist',twist), ('curve',curve)]

for fit in fits:
    fit_name = fit[0]
    fit_surf = fit[1]
    Z_delta = Z - fit_surf
    lift_surf = fit_surf - np.amin(fit_surf)
    
    print(f"Lifting plan ({fit_name} fit): FL={lift_surf[0,0]:.4f}, AL={lift_surf[-1,0]:.4f}, FR={lift_surf[0,-1]:.4f}, AR={lift_surf[-1,-1]:.4f}")
    
    fig = plt.figure(dpi=100)
    fig.suptitle(f"{fit_name} surface fit", fontsize=16)
    gs = fig.add_gridspec(3,3)
    #fig.set_size_inches(18.5, 10.5)
    ax1 = fig.add_subplot(gs[0,0], projection='3d')
    surf1 = ax1.plot_surface(X, Y, Z, cmap=cm.turbo, linewidth=0, antialiased=True)
    cbar1 = fig.colorbar(surf1, shrink=1, aspect=10, ax=ax1)
    cbar1.minorticks_on()
    ax1.set_title('raw data')
    ax1.azim = -75
    ax1.elev = 20
    ax1.zaxis.set_major_formatter('{x:.03f}')
    ax1.set_zlim(-0.02, 0.02)
    ax1.tick_params(axis='x', which='both', pad=-4)
    ax1.tick_params(axis='y', which='both', pad=-4)
    
    ax2 = fig.add_subplot(gs[1,0], projection='3d')
    surf2 = ax2.plot_surface(X, Y, fit_surf, cmap=cm.turbo, linewidth=0, antialiased=True)
    cbar2 = fig.colorbar(surf2, shrink=1, aspect=10, ax=ax2)
    cbar2.minorticks_on()
    # Customize the z axis.
    # ax2.set_zlim(-0.05, 0.05)
    # ax2.zaxis.set_major_locator(LinearLocator(10))
    # A StrMethodFormatter is used automatically
    ax2.set_zlim(-0.02, 0.02)
    ax2.zaxis.set_major_formatter('{x:.03f}')
    ax2.azim = -75
    ax2.elev = 20
    ax2.set_title('curve fit')
    ax2.tick_params(axis='x', which='major', pad=-4)
    ax2.tick_params(axis='y', which='major', pad=-4)
    
    ax4 = fig.add_subplot(gs[2,0], projection='3d')
    surf4 = ax4.plot_surface(X, Y, lift_surf, cmap=cm.inferno, linewidth=0, antialiased=True)
    cbar4 = fig.colorbar(surf4, shrink=1, aspect=10, ax=ax4)
    cbar4.minorticks_on()
    ax4.set_zlim(0,0.02)
    ax4.zaxis.set_major_formatter('{x:.03f}')
    ax4.azim = -75
    ax4.elev = 20
    ax4.set_title('lift plan')
    ax4.tick_params(axis='x', which='major', pad=-4)
    ax4.tick_params(axis='y', which='major', pad=-4)
    
    ax3 = fig.add_subplot(gs[:,1:], projection = '3d')
    surf3 = ax3.plot_surface(X,Y,Z_delta, rstride = 1, cstride = 1, cmap = cm.turbo, linewidth = 0)
    cbar3 = fig.colorbar(surf3, shrink=1, aspect=10, ax=ax3)
    cbar3.minorticks_on()
    ax3.zaxis.set_major_formatter('{x:.03f}')
    ax3.azim = -75
    ax3.elev = 20
    ax3.set_title('residual deviation')
    ax3.set_zlim(-0.02, 0.02)
    ax3.tick_params(axis='x', which='major', pad=-4)
    ax3.tick_params(axis='y', which='major', pad=-4)
    
    fig.tight_layout(pad=2.0)
    
    plt.show()
#plt.close('all') # clean up after using pyplot or else there can be memory and process problems