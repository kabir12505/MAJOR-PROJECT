
from pathlib import Path
import pandas as pd
import numpy as np
import torch

from PIL import Image
from torch.utils.data import Dataset, DataLoader
from torchvision.models import resnet50, ResNet50_Weights

# Paths
BASE_DIR = Path(__file__).resolve().parent
METADATA = BASE_DIR / "metadata.csv"
OUTPUT = BASE_DIR / "features.npz"

# Device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device:", device)

# Load pretrained ResNet50
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)
model.fc = torch.nn.Identity()
model = model.to(device)
model.eval()

# Use ResNet's required preprocessing
preprocess = weights.transforms()

class MRIDataset(Dataset):
    def __init__(self, dataframe):
        self.df = dataframe.reset_index(drop=True)

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        row = self.df.iloc[idx]
        image = Image.open(row["image_path"]).convert("RGB")
        image = preprocess(image)

        return image, int(row["label"])

df = pd.read_csv(METADATA)
dataset = MRIDataset(df)

loader = DataLoader(
    dataset,
    batch_size=16,
    shuffle=False,
    num_workers=0
)

all_features = []
all_labels = []

with torch.no_grad():
    for batch_idx, (images, labels) in enumerate(loader):
        images = images.to(device)

        features = model(images)

        all_features.append(features.cpu().numpy())
        all_labels.append(labels.numpy())

        if (batch_idx + 1) % 20 == 0:
            print(
                f"Processed {(batch_idx + 1) * 16}"
                f" / {len(dataset)} images"
            )

X = np.concatenate(all_features, axis=0)
y = np.concatenate(all_labels, axis=0)

np.savez_compressed(
    OUTPUT,
    X=X,
    y=y
)

print("\nFeature extraction complete!")
print("Features shape:", X.shape)
print("Labels shape:", y.shape)
print("Saved to:", OUTPUT)