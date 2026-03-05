import torch
import torch.nn as nn

class MultimodalUlcerModel(nn.Module):
    def __init__(self, image_feature_dim=2048, num_clinical_features=4, num_classes=2):
        super(MultimodalUlcerModel, self).__init__()
        
        self.image_fc = nn.Sequential(
            nn.Linear(image_feature_dim, 512),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        self.clinical_fc = nn.Sequential(
            nn.Linear(num_clinical_features, 64),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        self.fusion_fc = nn.Sequential(
            nn.Linear(512 + 64, 256),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, num_classes)
        )
    
    def forward(self, image_features, clinical_features):
        x_image = self.image_fc(image_features)
        x_clinical = self.clinical_fc(clinical_features)
        
        x = torch.cat([x_image, x_clinical], dim=1)
        x = self.fusion_fc(x)
        
        return x

def create_multimodal_model(image_feature_dim=2048, num_clinical_features=4, num_classes=2):
    return MultimodalUlcerModel(image_feature_dim, num_clinical_features, num_classes)
