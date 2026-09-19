
from pathlib import Path

dataset_path = Path(
    r"C:\Users\HP\OneDrive\Documents\GitHub\MAJOR-PROJECT\archive\OriginalDataset"
)

extensions = {".jpg", ".jpeg", ".png", ".bmp"}

print("Dataset folder:", dataset_path)
print("Exists:", dataset_path.exists())

for folder in sorted(dataset_path.iterdir()):
    if folder.is_dir():
        images = [
            f for f in folder.rglob("*")
            if f.is_file() and f.suffix.lower() in extensions
        ]
        print(f"{folder.name}: {len(images)} images")