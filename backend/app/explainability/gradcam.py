import torch
import torch.nn.functional as F
import numpy as np
import cv2

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

def generate_gradcam(model, input_tensor, target_layer=None):
    if target_layer is None:
        target_layer = model.resnet.layer4[-1]
    
    gradcam = GradCAM(model, target_layer)
    heatmap = gradcam.generate_heatmap(input_tensor)
    
    return heatmap
