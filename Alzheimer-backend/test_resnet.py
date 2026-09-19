
import torch
from torchvision.models import resnet50, ResNet50_Weights

# Load pretrained ResNet50
weights = ResNet50_Weights.DEFAULT
model = resnet50(weights=weights)

# Remove final classification layer
model.fc = torch.nn.Identity()
model.eval()

# Test with one dummy image
dummy_image = torch.randn(1, 3, 224, 224)

with torch.no_grad():
    features = model(dummy_image)

print("ResNet50 loaded successfully!")
print("Feature shape:", features.shape)