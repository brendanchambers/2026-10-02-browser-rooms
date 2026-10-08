# Generate 3D space for browser use (exploratory)

## Planned milestones

- Generate plain square room
- Visualize locally in browser
- Generate a more complex space

## Links

Engines  
- (Visionary) https://github.com/Visionary-Laboratory/visionary  
Models  
- (Flux 2) https://huggingface.co/black-forest-labs  
- (HunyuanWorld) https://huggingface.co/tencent/HunyuanWorld-Mirror  
Datasets  
- https://huggingface.co/datasets/spatialverse/InteriorGS  
- Nithins03/us-architectural-floorplan-sft  
- https://huggingface.co/datasets/sylvainHellin/ifc-bench  
Emerging alternatives to collision meshes  
- Splat-CBF: Safe Next-Best-View Control in 3D Gaussian-Splat Maps https://arxiv.org/abs/2609.23100

### Generate (experimental)
`uv run --with modal modal run explore/floorplan.py`

### A framework for navigable 3DGS

- Renderer: Three.js + GaussianSplats3D (or PlayCanvas/SuperSplat).
- Physics: Rapier.js (WebAssembly). It is significantly faster and more stable than Ammo.js/Cannon.js for continuous ground-clamping raycasts required for wheeled vehicles.
- Collision Mesh: Pre-process the 3DGS .ply using SuGaR to generate a simplified low-poly OBJ of the floor and walls. Load this into Rapier.js as static colliders.
- Robot Controller: Create a Rapier dynamic cylinder, apply physics impulses based on WASD input (simulating Ackermann steering), and sync the Three.js 3DGS camera to the cylinder's transform every frame.



