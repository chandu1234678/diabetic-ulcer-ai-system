import torch
import torch.nn.functional as F
import numpy as np
import cv2
import os
import sys
from PIL import Image
import torchvision.transforms as transforms

class GradCAM:
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        self.target_layer.register_forward_hook(self.save_activations)
        self.target_layer.register_full_backward_hook(self.save_gradients)
    
    def save_activations(self, module, input, output):
        self.activations = output.detach()
    
    def save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0].detach()
    
    def generate_heatmap(self, input_tensor, target_class=None):
        self.model.eval()
        
        with torch.enable_grad():
            input_tensor.requires_grad_(True)
            output = self.model(input_tensor)
            
            if target_class is None:
                target_class = output.argmax(dim=1).item()
            
            self.model.zero_grad()
            score = output[0, target_class]
            score.backward()
        
        pooled_gradients = torch.mean(self.gradients, dim=[0, 2, 3])
        activations = self.activations[0]
        
        for i in range(activations.shape[0]):
            activations[i, :, :] *= pooled_gradients[i]
        
        heatmap = torch.mean(activations, dim=0).cpu().numpy()
        heatmap = np.maximum(heatmap, 0)
        heatmap /= (heatmap.max() + 1e-8)
        
        heatmap_resized = cv2.resize(heatmap, (224, 224))
        heatmap_resized = np.uint8(255 * heatmap_resized)
        
        return heatmap_resized.tolist()

def generate_gradcam(image_path, model_path):
    """
    Generate Grad-CAM heatmap for an image using a trained ResNet18 model.
    
    Args:
        image_path (str): Path to the input image
        model_path (str): Path to the saved model checkpoint
    
    Returns:
        tuple: (predicted_class, confidence, overlay_image)
    """
    # Load model
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    from app.ml.cnn_model import create_model
    
    model = create_model(num_classes=2, pretrained=False)
    checkpoint = torch.load(model_path, map_location='cpu')
    model.load_state_dict(checkpoint)
    model.eval()
    device = torch.device('cpu')
    model = model.to(device)
    
    # Load and preprocess image
    image = Image.open(image_path).convert('RGB')
    original_size = image.size  # (width, height)
    
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    
    input_tensor = transform(image).unsqueeze(0).to(device)
    
    # Get prediction
    with torch.no_grad():
        outputs = model(input_tensor)
        predicted_class_idx = outputs.argmax(dim=1).item()
        confidence = torch.softmax(outputs, dim=1)[0, predicted_class_idx].item()
    
    class_names = ['normal', 'ulcer']
    predicted_class = class_names[predicted_class_idx]
    
    # Generate Grad-CAM heatmap
    gradcam = GradCAM(model, model.resnet.layer4[-1])
    heatmap = gradcam.generate_heatmap(input_tensor, predicted_class_idx)
    heatmap = np.array(heatmap, dtype=np.uint8)
    
    # Resize heatmap to original image size
    heatmap_resized = cv2.resize(heatmap, (original_size[0], original_size[1]))
    
    # Load original image as numpy array
    img_array = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    # Apply colormap to heatmap
    heatmap_colored = cv2.applyColorMap(heatmap_resized, cv2.COLORMAP_JET)
    
    # Blend original image with heatmap
    overlay = cv2.addWeighted(img_array, 0.6, heatmap_colored, 0.4, 0)
    
    # Save result
    os.makedirs('outputs', exist_ok=True)
    cv2.imwrite('outputs/gradcam_result.png', overlay)
    
    return predicted_class, confidence, overlay
