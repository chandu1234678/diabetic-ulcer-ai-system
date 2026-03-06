"""
Data quality validation script.
Identifies corrupted, low-quality, or mislabeled images that could cause false positives.
"""

import os
from PIL import Image
import numpy as np
import logging
from pathlib import Path
import json
from collections import defaultdict

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DataQualityValidator:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.quality_report = {
            'total_images': 0,
            'valid_images': 0,
            'corrupted_images': [],
            'low_resolution': [],
            'unusual_dimensions': [],
            'low_contrast': [],
            'possible_duplicates': [],
            'size_distribution': defaultdict(int),
            'image_stats': {}
        }
    
    def validate_image_integrity(self):
        """Check for corrupted or unreadable images."""
        logger.info("Validating image integrity...")
        
        for class_name in ['normal', 'ulcers']:
            class_dir = os.path.join(self.dataset_path, class_name)
            if not os.path.exists(class_dir):
                continue
            
            logger.info(f"Scanning {class_name} directory...")
            
            for filename in os.listdir(class_dir):
                if not filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                    continue
                
                self.quality_report['total_images'] += 1
                filepath = os.path.join(class_dir, filename)
                
                try:
                    with Image.open(filepath) as img:
                        # Check minimum size (128x128)
                        if img.size[0] < 128 or img.size[1] < 128:
                            self.quality_report['low_resolution'].append({
                                'file': filepath,
                                'size': img.size,
                                'class': class_name
                            })
                            logger.warning(f"Low resolution: {filename} ({img.size})")
                            continue
                        
                        # Check for unusually stretched images
                        aspect_ratio = img.size[0] / img.size[1]
                        if aspect_ratio < 0.3 or aspect_ratio > 3.0:
                            self.quality_report['unusual_dimensions'].append({
                                'file': filepath,
                                'size': img.size,
                                'aspect_ratio': aspect_ratio,
                                'class': class_name
                            })
                            logger.warning(f"Unusual aspect ratio: {filename} ({aspect_ratio:.2f})")
                        
                        # Check contrast
                        img_array = np.array(img.convert('L'))
                        contrast = img_array.std()
                        if contrast < 10:  # Very low contrast
                            self.quality_report['low_contrast'].append({
                                'file': filepath,
                                'contrast': float(contrast),
                                'class': class_name
                            })
                            logger.warning(f"Low contrast: {filename} (contrast: {contrast:.2f})")
                        
                        # Record image stats
                        key = f"{class_name}/{filename}"
                        self.quality_report['image_stats'][key] = {
                            'size': img.size,
                            'contrast': float(contrast),
                            'aspect_ratio': float(aspect_ratio)
                        }
                        
                        self.quality_report['valid_images'] += 1
                        self.quality_report['size_distribution'][f"{img.size[0]}x{img.size[1]}"] += 1
                
                except Exception as e:
                    self.quality_report['corrupted_images'].append({
                        'file': filepath,
                        'error': str(e),
                        'class': class_name
                    })
                    logger.error(f"Corrupted image: {filename} - {e}")
    
    def generate_report(self, output_path='data_quality_report.json'):
        """Generate quality report."""
        logger.info("\n" + "="*60)
        logger.info("DATA QUALITY REPORT")
        logger.info("="*60)
        
        logger.info(f"\nTotal images scanned: {self.quality_report['total_images']}")
        logger.info(f"Valid images: {self.quality_report['valid_images']}")
        logger.info(f"Corrupted images: {len(self.quality_report['corrupted_images'])}")
        logger.info(f"Low resolution images: {len(self.quality_report['low_resolution'])}")
        logger.info(f"Unusual dimensions: {len(self.quality_report['unusual_dimensions'])}")
        logger.info(f"Low contrast images: {len(self.quality_report['low_contrast'])}")
        
        # Resolution distribution
        logger.info("\nResolution distribution (top 10):")
        sorted_sizes = sorted(
            self.quality_report['size_distribution'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]
        for size, count in sorted_sizes:
            logger.info(f"  {size}: {count} images")
        
        # Save report
        with open(output_path, 'w') as f:
            json.dump(self.quality_report, f, indent=2)
        
        logger.info(f"\nReport saved to: {output_path}")
        
        # Recommendations
        if len(self.quality_report['corrupted_images']) > 0:
            logger.warning(f"\n⚠️  {len(self.quality_report['corrupted_images'])} corrupted images should be removed")
        
        if len(self.quality_report['low_resolution']) > 0:
            logger.warning(f"⚠️  {len(self.quality_report['low_resolution'])} low-resolution images should be removed")
        
        if len(self.quality_report['low_contrast']) > 0:
            logger.info(f"ℹ️  {len(self.quality_report['low_contrast'])} low-contrast images detected")
            logger.info("   Consider if these are legitimate 'normal' samples or mislabeled")
        
        return self.quality_report
    
    def remove_problematic_images(self, remove_corrupted=True, remove_low_res=True, remove_low_contrast=False):
        """Remove problematic images from dataset."""
        logger.info("\n" + "="*60)
        logger.info("REMOVING PROBLEMATIC IMAGES")
        logger.info("="*60)
        
        removed_count = 0
        
        if remove_corrupted:
            for item in self.quality_report['corrupted_images']:
                try:
                    os.remove(item['file'])
                    logger.info(f"Removed corrupted: {item['file']}")
                    removed_count += 1
                except:
                    pass
        
        if remove_low_res:
            for item in self.quality_report['low_resolution']:
                try:
                    os.remove(item['file'])
                    logger.info(f"Removed low-res: {item['file']}")
                    removed_count += 1
                except:
                    pass
        
        if remove_low_contrast:
            for item in self.quality_report['low_contrast']:
                try:
                    os.remove(item['file'])
                    logger.info(f"Removed low-contrast: {item['file']}")
                    removed_count += 1
                except:
                    pass
        
        logger.info(f"\nTotal images removed: {removed_count}")
        return removed_count


if __name__ == "__main__":
    import os
    # Get project root dynamically
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    dataset_path = os.path.join(project_root, "datasets", "images")
    report_path = os.path.join(project_root, "data_quality_report.json")
    
    logger.info(f"Dataset path: {dataset_path}")
    logger.info(f"Report path: {report_path}")
    
    validator = DataQualityValidator(dataset_path)
    validator.validate_image_integrity()
    report = validator.generate_report(report_path)
    
    # Optionally remove problematic images (uncomment to enable)
    # validator.remove_problematic_images(
    #     remove_corrupted=True,
    #     remove_low_res=True,
    #     remove_low_contrast=False
    # )
    
    logger.info("\nData quality validation complete!")
