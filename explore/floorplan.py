"""Generate floorplan images using FLUX.2-klein-4B on Modal."""

import modal

app = modal.App("floorplan-generator")

image = modal.Image.debian_slim(python_version="3.12").pip_install(
    "diffusers",
    "transformers",
    "torch",
    "accelerate",
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
    """Generate a simple cubic room floorplan."""
    from pathlib import Path

    prompt = "Render a plain cubic room with a single arched doorway centered on one wall."
    output_path = "data/2D/latest.png"

    image_bytes = generate_floorplan.remote(prompt, output_path)

    # Save locally
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_bytes(image_bytes)
    print(f"Floorplan saved to: {output_path}")
