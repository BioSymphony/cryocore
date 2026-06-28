# CryoCore PyMOL map+model hero (headless, window-free). Placeholders: {{MAP}} {{MODEL}} {{LEVEL}} {{OUT}}
# Run:  pymol -cq this.pml
# Note: "model" is a reserved PyMOL object name -> coordinates are loaded as "mol".
load {{MAP}}, emap
load {{MODEL}}, mol
bg_color white
set ray_opaque_background, 1
set antialias, 2
set ray_shadows, 1
set cartoon_fancy_helices, 1
hide everything
show cartoon, mol
set cartoon_ring_mode, 3
set cartoon_ring_finder, 1
util.cbc mol
show sticks, mol and organic
isomesh density, emap, {{LEVEL}}, mol, carve=2.5
color grey70, density
set mesh_width, 0.4, density
orient mol
zoom mol, 3
png {{OUT}}, width=1000, height=1000, dpi=200, ray=1
quit
