from huggingface_hub import hf_hub_download
from pathlib import Path
import shutil


def main():
    repo_id = "spatialVerse/interiorGS"
    scene_id = "0001_839920"

    print(f"Accessing cached dataset {repo_id}...")

    # Use hf_hub_download which will use cached files if available
    ply_path = hf_hub_download(
        repo_id=repo_id,
        repo_type="dataset",
        filename=f"{scene_id}/3dgs_compressed.ply"
    )

    print(f"[OK] Found in cache: {ply_path}")

    # Create symlink in data/wip instead of copying
    output_dir = Path("data/wip") / scene_id
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / "3dgs_compressed.ply"

    # Remove existing file/symlink if it exists
    if output_file.exists():
        output_file.unlink()

    # Create symlink to cached file
    output_file.symlink_to(ply_path)

    print(f"[OK] Symlinked to: {output_file}")

    # Check file size
    file_size = Path(ply_path).stat().st_size / (1024 * 1024)
    print(f"     File size: {file_size:.2f} MB")

    # Also get the other files for this scene
    for filename in ["labels.json", "structure.json", "occupancy.json", "occupancy.png"]:
        try:
            file_path = hf_hub_download(
                repo_id=repo_id,
                repo_type="dataset",
                filename=f"{scene_id}/{filename}"
            )
            output_file = output_dir / filename
            if output_file.exists():
                output_file.unlink()
            output_file.symlink_to(file_path)
            print(f"[OK] Symlinked: {filename}")
        except Exception as e:
            print(f"[SKIP] {filename}: {e}")


if __name__ == "__main__":
    main()
