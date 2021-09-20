# disc-flow-animation

The code hosted on this repository generates an animation of a rigid disc that rotates passively under channel-flow turbulence.

The solver [Incompact3D](https://github.com/xcompact3d) is used to perform a Direct Numerical Simulation of a turbulent channel fitted with a free-to-move solid disc on the wall.

A collection of two-dimensional snapshots of the shear-stress field at the wall are stored in the directory 'flow_snapshots' and used as input to the script 'animation_disc.py'.

The [Matplotlib](https://www.matplotlib.org) library is then used to render the flow field snapshots into animation frames and export the resulting video to file.

<figure class="video_container">
  <video 
  width="100%" 
  height="auto" 
  max-width="1280" 
  max-height="720" 
  muted 
  playsinline 
  autoplay 
  loop>
    <source src="disc.mp4" type="video/mp4">
  </video>
</figure>

More complete information on the flow physics and the numerical methods can be found in:

Olivucci P, Wise DJ, Ricco P, 
[Reduction of turbulent skin-friction drag by passively rotating discs](https://doi.org/10.1017/jfm.2021.533), 
J. Fluid Mech., 2021.
