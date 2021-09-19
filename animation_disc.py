'''
This script generates an animation of a rigid disc that rotates passively under 
channel-flow turbulence.

Reference:
Olivucci P, Wise DJ, Ricco P, 
Reduction of turbulent skin-friction drag by passively rotating discs, 
J. Fluid Mech., 2021.
https://doi.org/10.1017/jfm.2021.533
'''

import numpy as np

from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable
from matplotlib.patches import Circle, Rectangle, Arrow
from matplotlib.collections import QuadMesh


def read_binary(path: str, shape: tuple) -> np.ndarray:
    '''
    Reads a Fortran-ordered binary file into a numpy array.

    @param path: path to the input file.
    @param shape: shape of the array.

    @return: ndarray of the desired shape.
    '''

    dt = np.dtype(np.float64)
    u = np.fromfile(path, dtype=dt)

    return np.reshape(u, shape, order='F')


def plot_secchi_disc(centre: tuple, radius: float, theta_deg: float) -> None:
    '''
    Draws a Secchi disc rotated by theta_deg degrees.
    '''
    
    alp = 0.6   # Black transparency

    # Draws a circle:
    p2 = Circle(centre, radius=radius, color='k', ls='-', lw=0.5, fill=False, 
                alpha=alp, transform=plt.gca().transData)

    # Draws black and white quadrants:
    opts = {'angle':theta_deg, 'fill':True, 'lw':0., 'alpha':alp}
    p3 = Rectangle(centre,  radius,  radius, color='k', **opts)
    p4 = Rectangle(centre, -radius, -radius, color='k', **opts)
    p5 = Rectangle(centre,  radius, -radius, color='w', **opts)
    p6 = Rectangle(centre, -radius,  radius, color='w', **opts)
    
    plt.plot(centre[0],centre[1], marker='+', ms=10, ls='None',c='k', alpha=alp)
    plt.gca().add_patch(p2)

    for p in (p3,p4,p5,p6): p.set_clip_path(p2); plt.gca().add_patch(p)

    
def plot_field(x: np.ndarray, z: np.ndarray, field: np.ndarray, 
               ylim=(None, None)) -> QuadMesh:
    '''
    Plots the flow field and return matplotlib object 

    @param x, z: spatial coords as arrays of shape (N,) and (M,) respectively.
    @param field: array of shape (N,M) storing flow field data.
    @param ylim: colormap range min and max.

    @return surf: matplotlib mesh object subsequently used for plotting.
    '''

    # Plot options:
    plt.xlim(x[0], x[-1])
    plt.ylim(z[0], z[-1])
    plt.gca().set_aspect(1, adjustable='box')

    # Plot field:
    surf = plt.pcolormesh(x, z, field, 
                          vmin=ylim[0], 
                          vmax=ylim[1], 
                          shading='gouraud', 
                          # cmap='cool',
                          edgecolor=None,
                          # clip_on=True,
                          # alpha=0.4,
                          zorder=2,
                          rasterized=True)

    # #add colorbar:
    # divider = make_axes_locatable(plt.gca())
    # cax = divider.append_axes("right", size="2%", pad=0.05)
    # plt.colorbar(surf, cax=cax, orientation="vertical")

    return surf


def pcolormesh_alpha_map(pcmesh, alpha: np.ndarray) -> None:
    '''
    Changes a color mesh transparency level according to the given alpha mesh.
    Adapted from https://stackoverflow.com/questions/52100747

    @param pcmesh: input pcolormesh object
    @param alpha:   
    '''
    plt.gcf().canvas.draw()         # Generate face color array
    rgba = pcmesh.get_facecolor()   # Gets rgba face colors
    rgba[:,3] = alpha.ravel()       # Write alpha values
    pcmesh.set_facecolor(rgba)      # Update face colors
    plt.gcf().canvas.draw()         # Apply modifications


def plot_loop(i: int, x: np.ndarray, z: np.ndarray, *args):
    '''
    Reads and plots the i-th flow field snapshot.
    '''

    # Read flow field:
    shp = (len(x), 1, len(z))
    xz_slice = read_binary(field_data % str(i).zfill(6), shp)[:,0,:]
    
    # Define disc centre and calculate moment:
    centre = (0.5*x[-1], 0.5*z[0])
    rz = np.meshgrid(z) - centre[1]
    z_moment = xz_slice * rz / 180

    # Clear fig:
    plt.gcf().clf()

    # Labels and style:
    plt.style.use(['grayscale', './animation.mplstyle'])
    plt.title('$t = %4.2f$' % (i*0.0025), 
        horizontalalignment='left',
        verticalalignment='bottom')
    plt.xlabel('$x^+$')
    plt.ylabel('$z^+$')

    # Plot disc and field:
    plot_secchi_disc(centre, 180, theta_deg[i])
    surf = plot_field(x, z, xz_slice.transpose(), ylim=(0,15))

    # Apply magnitude-scaled transparency:
    alpha = np.abs(z_moment.transpose())/17
    alpha[(alpha > 1)] = 1
    pcolormesh_alpha_map(surf, alpha)

    print('Frame no.', i)


if __name__=="__main__":

    ### Plot configuration:
    
    # Input files:
    data_dir = '/home/paolo/shef-phd/dns/sharc/freely_tests/freely_D2/raw-data/'
    field_data= data_dir+'dudy/dudy%s.dat'
    time_data = data_dir+'disc_000001.dat'

    # Load time history file:
    theta_deg = 180.0*np.loadtxt(time_data,usecols=(4,))/np.pi

    # Define coordinates:
    x = 180*np.linspace(0, 4*np.pi, 256)
    z = 180*np.linspace(0, 4*np.pi/3, 128)[::-1]

    # Define frames and frame rate:
    # frames = np.arange(100,38700,100)
    frames = np.arange(100,5000,100)
    fps = 30

    export = 'mp4' # choose export video format (mp4, gif, html)

    # Instantiate plotting environment:
    fig = plt.figure(figsize=(8,4.5))


    ### Set up animation loop:
    animation = FuncAnimation(fig, 
                              plot_loop, 
                              frames, 
                              fargs=(x, z, field_data, time_data, theta_deg), 
                              interval=1000/fps
                              )

    ### Render animation:
    animation.save('disc.'+export, fps=fps)