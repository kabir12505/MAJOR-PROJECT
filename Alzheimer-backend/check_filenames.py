
from pathlib import Path

root = Path(
    r"C:\Users\HP\OneDrive\Documents\GitHub\MAJOR-PROJECT\archive\OriginalDataset"
)

for folder in sorted(root.iterdir()):
    if folder.is_dir():
        files = sorted(
            f.name for f in folder.iterdir()
            if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}
        )

        print(f"\n{folder.name} — {len(files)} images")
        print("Sample filenames:")
        for name in files[:10]:
            print(" ", name)