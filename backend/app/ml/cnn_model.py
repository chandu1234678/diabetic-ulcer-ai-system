import torch
import torch.nn as nn
import torchvision.models as models
from torchvision.models import resnet18, ResNet18_Weights

class UlcerCNNModel(nn.Module):
    def __init__(self, num_classes=2, pretrained=True):
        super(UlcerCNNModel, self).__init__()
        
        if pretrained:
            weights = ResNet18_Weights.DEFAULT
        else:
            weights = None
        
        self.resnet = resnet18(weights=weights)
        num_ftrs = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_ftrs, num_classes)
        
    def forward(self, x):
        return self.resnet(x)
    
    def get_features(self, x):
        x = self.resnet.conv1(x)
        x = self.resnet.bn1(x)
        x = self.resnet.relu(x)
        x = self.resnet.maxpool(x)
        
        x = self.resnet.layer1(x)
        x = self.resnet.layer2(x)
        x = self.resnet.layer3(x)
        x = self.resnet.layer4(x)
        
        x = self.resnet.avgpool(x)
        features = torch.flatten(x, 1)
        
        return features

def create_model(num_classes=2, pretrained=True):
    return UlcerCNNModel(num_classes=num_classes, pretrained=pretrained)
