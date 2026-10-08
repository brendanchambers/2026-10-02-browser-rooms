import json
from pathlib import Path
from datasets import load_dataset


def main():
    print("Loading spatialVerse/interiorGS dataset...")

    # Use streaming mode to avoid schema inconsistency issues
    print("Attempting streaming mode to inspect schema...")
    try:
        dataset_stream = load_dataset(
            "spatialVerse/interiorGS",
            streaming=True
        )
        print(f"Streaming dataset splits: {list(dataset_stream.keys())}")

        # Get first example and inspect it thoroughly
        first_split = list(dataset_stream.keys())[0]
        example = next(iter(dataset_stream[first_split]))

        print(f"\n=== Full Example Structure ===")
        for key, val in example.items():
            val_type = type(val).__name__
            if isinstance(val, (list, dict)):
                val_len = len(val) if hasattr(val, '__len__') else 'N/A'
                print(f"{key}: {val_type} (length: {val_len})")
            elif hasattr(val, 'shape'):
                print(f"{key}: {val_type} (shape: {val.shape})")
            elif hasattr(val, '__dict__'):
                print(f"{key}: {val_type} - {list(val.__dict__.keys())}")
            else:
                print(f"{key}: {val_type} - {val}")

        print(f"\n=== Detailed Inspection ===")
        # Check if there are any file paths or binary data
        for key, val in example.items():
            print(f"\n{key}:")
            if isinstance(val, dict):
                print(f"  Dict keys: {list(val.keys())}")
                for k, v in val.items():
                    print(f"    {k}: {type(v).__name__}")
            elif isinstance(val, list) and len(val) > 0:
                print(f"  First item type: {type(val[0]).__name__}")
                if isinstance(val[0], dict):
                    print(f"  First item keys: {list(val[0].keys())}")
            else:
                print(f"  Value: {val}")

    except Exception as e:
        print(f"\nError loading dataset: {e}")
        raise


if __name__ == "__main__":
    main()
