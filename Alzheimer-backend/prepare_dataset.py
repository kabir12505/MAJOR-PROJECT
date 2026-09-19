
from pathlib import Path
import pandas as pd

root = Path(
    r"C:\Users\HP\OneDrive\Documents\GitHub\MAJOR-PROJECT\archive\OriginalDataset"
)

classes = {
    "MildDemented": 1,
    "ModerateDemented": 1,
    "VeryMildDemented": 1,
    "NonDemented": 0,
}

rows = []

for folder_name, label in classes.items():
    folder = root / folder_name

    for image in folder.iterdir():
        if image.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}:
            rows.append({
                "image_path": str(image),
                "class_name": folder_name,
                "label": label
            })

df = pd.DataFrame(rows)
output = Path("metadata.csv")
df.to_csv(output, index=False)

print("Total images:", len(df))
print("\nClass counts:")
print(df["class_name"].value_counts())
print("\nBinary labels:")
print(df["label"].value_counts())
print("\nSaved to:", output.resolve())