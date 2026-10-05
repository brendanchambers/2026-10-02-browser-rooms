"""Generate floorplan images from scene graphs using FLUX.2-klein-4B on Modal."""

import modal
import json

app = modal.App("floorplan-from-scene-graph")

image = modal.Image.debian_slim(python_version="3.12").pip_install(
    "diffusers",
    "transformers",
    "torch",
    "accelerate",
    "datasets",
)

@app.function(
    image=image,
    gpu="a10g",
    timeout=600,
)
def generate_floorplan(prompt: str, output_path: str = "data/floorplan.png"):
    """Generate a floorplan image from a text prompt."""
    from diffusers import DiffusionPipeline
    import torch
    from pathlib import Path

    pipe = DiffusionPipeline.from_pretrained(
        "black-forest-labs/FLUX.2-klein-4B",
        torch_dtype=torch.bfloat16,
    )
    pipe.to("cuda")

    image = pipe(
        prompt=prompt,
        num_inference_steps=20,
        guidance_scale=3.5,
    ).images[0]

    # Save to temporary location and return bytes
    import io
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    return buf.getvalue()

@app.local_entrypoint()
def main():
    """Generate a floorplan from the 13th entry in the semantic dataset."""
    from pathlib import Path
    from datasets import load_dataset

    # Load the semantic dataset
    ds = load_dataset("Nithins03/us-architectural-floorplan-sft")

    # Get the assistant response message from the 14th entry (index 13)
    content = ds['train'][13]['messages'][2]['content']
     # Extract scene graph from the entry
    scene_graph = json.dumps(json.loads(content.split('```')[1].split('json')[1]), indent=1)

    # Create a prompt from the scene graph
    prompt = f"Generate a floorplan from the following scene graph: {scene_graph}"

    print(f"Scene graph: {scene_graph}")
    print(f"Generating floorplan from scene graph...")

    output_path = "data/2D/scene_graph_13.png"

    image_bytes = generate_floorplan.remote(prompt, output_path)

    # Save locally
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_bytes(image_bytes)
    print(f"Floorplan saved to: {output_path}")
