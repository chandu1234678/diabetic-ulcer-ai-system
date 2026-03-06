"""
Master retraining orchestrator.
Runs the complete pipeline: validate → analyze → retrain → verify
"""

import os
import sys
import subprocess
import json
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('retraining_pipeline.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class RetrainingPipeline:
    def __init__(self, project_root='../../', dataset_path='datasets/images', model_dir='model_weights'):
        self.project_root = project_root
        self.dataset_path = os.path.join(project_root, dataset_path)
        self.model_dir = os.path.join(project_root, model_dir)
        self.scripts_dir = os.path.dirname(os.path.abspath(__file__))
        self.results = {}
        
        # Create backup timestamp
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def log_header(self, title):
        """Print formatted header."""
        logger.info("\n" + "="*70)
        logger.info(f"  {title}".center(70))
        logger.info("="*70)
    
    def run_command(self, script_name, description):
        """Run a Python script and capture results."""
        self.log_header(description)
        
        script_path = os.path.join(self.scripts_dir, script_name)
        
        if not os.path.exists(script_path):
            logger.error(f"Script not found: {script_path}")
            return False
        
        try:
            env = os.environ.copy()
            env['PYTHONUNBUFFERED'] = '1'
            
            result = subprocess.run(
                [sys.executable, script_path],
                cwd=self.scripts_dir,
                capture_output=False,
                text=True,
                timeout=3600  # 1 hour timeout
            )
            
            if result.returncode == 0:
                logger.info(f"[OK] {description} completed successfully")
                return True
            else:
                logger.error(f"[FAIL] {description} failed with code {result.returncode}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error(f"[FAIL] {description} timed out after 1 hour")
            return False
        except Exception as e:
            logger.error(f"[FAIL] Error running {description}: {e}")
            return False
    
    def backup_old_model(self):
        """Backup the current production model."""
        self.log_header("BACKING UP CURRENT MODEL")
        
        old_model = os.path.join(self.model_dir, 'cnn_ulcer_model.pth')
        backup_model = os.path.join(
            self.model_dir,
            f'cnn_ulcer_model_backup_{self.timestamp}.pth'
        )
        
        if os.path.exists(old_model):
            try:
                import shutil
                shutil.copy2(old_model, backup_model)
                logger.info(f"[OK] Model backed up to: {backup_model}")
                self.results['backup'] = backup_model
                return True
            except Exception as e:
                logger.error(f"[FAIL] Failed to backup model: {e}")
                return False
        else:
            logger.warning(f"No existing model to backup at: {old_model}")
            return True
    
    def step1_validate_data(self):
        """Step 1: Validate dataset quality."""
        return self.run_command(
            'validate_data_quality.py',
            'STEP 1: DATA QUALITY VALIDATION'
        )
    
    def step2_analyze_baseline(self):
        """Step 2: Analyze baseline model false positives."""
        return self.run_command(
            'analyze_false_positives.py',
            'STEP 2: BASELINE FALSE POSITIVE ANALYSIS'
        )
    
    def step3_retrain_model(self):
        """Step 3: Retrain with production improvements."""
        return self.run_command(
            'retrain_production_model.py',
            'STEP 3: PRODUCTION MODEL RETRAINING'
        )
    
    def step4_analyze_improved(self):
        """Step 4: Analyze improved model."""
        return self.run_command(
            'analyze_false_positives.py',
            'STEP 4: IMPROVED MODEL ANALYSIS'
        )
    
    def deploy_new_model(self):
        """Deploy the newly trained model."""
        self.log_header("DEPLOYING NEW MODEL")
        
        new_model = os.path.join(self.model_dir, 'ulcer_detection_model_production.pth')
        prod_model = os.path.join(self.model_dir, 'cnn_ulcer_model.pth')
        
        if not os.path.exists(new_model):
            logger.error(f"New model not found: {new_model}")
            return False
        
        try:
            import shutil
            shutil.copy2(new_model, prod_model)
            logger.info(f"[OK] New model deployed to: {prod_model}")
            self.results['deployment'] = prod_model
            return True
        except Exception as e:
            logger.error(f"[FAIL] Deployment failed: {e}")
            return False
    
    def generate_summary(self):
        """Generate retraining summary report."""
        self.log_header("RETRAINING SUMMARY")
        
        summary = {
            'timestamp': self.timestamp,
            'steps_completed': self.results,
            'model_location': os.path.join(self.model_dir, 'cnn_ulcer_model.pth'),
            'backup_location': os.path.join(self.model_dir, f'cnn_ulcer_model_backup_{self.timestamp}.pth'),
            'training_history': os.path.join(self.model_dir, 'training_history.json'),
            'reports': {
                'data_quality': 'data_quality_report.json',
                'false_positive_analysis': 'false_positive_analysis/false_positive_analysis.json'
            }
        }
        
        summary_file = os.path.join(self.project_root, f'retraining_summary_{self.timestamp}.json')
        
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"\n[OK] Summary report saved: {summary_file}")
        
        # Print quick summary
        logger.info("\nKey Results:")
        logger.info(f"  • New model: {summary['model_location']}")
        logger.info(f"  • Backup saved: {summary['backup_location']}")
        logger.info(f"  • Training history: {summary['training_history']}")
        logger.info(f"\nTo review improvements:")
        logger.info(f"  • Cat {summary['reports']['false_positive_analysis']}")
        logger.info(f"  • Compare specificity, false positive rate metrics")
    
    def run_full_pipeline(self, skip_steps=None, deploy=True):
        """Run the complete retraining pipeline."""
        
        if skip_steps is None:
            skip_steps = []
        
        self.log_header("STARTING FULL RETRAINING PIPELINE")
        logger.info(f"Project root: {self.project_root}")
        logger.info(f"Dataset: {self.dataset_path}")
        logger.info(f"Model directory: {self.model_dir}")
        
        success = True
        
        # Backup
        if not self.backup_old_model():
            success = False
        
        # Step 1: Validate data
        if 'validate' not in skip_steps:
            if self.step1_validate_data():
                self.results['step1_validate'] = 'completed'
            else:
                logger.warning("Data validation had issues, continuing anyway...")
                self.results['step1_validate'] = 'warning'
        
        # Step 2: Analyze baseline
        if 'analyze_baseline' not in skip_steps:
            if self.step2_analyze_baseline():
                self.results['step2_analyze_baseline'] = 'completed'
            else:
                logger.warning("Baseline analysis failed, continuing with retraining...")
                self.results['step2_analyze_baseline'] = 'failed'
        
        # Step 3: Retrain
        if 'retrain' not in skip_steps:
            if self.step3_retrain_model():
                self.results['step3_retrain'] = 'completed'
            else:
                logger.error("Retraining failed!")
                success = False
        
        # Step 4: Analyze improved model
        if 'analyze_improved' not in skip_steps:
            if self.step4_analyze_improved():
                self.results['step4_analyze_improved'] = 'completed'
            else:
                logger.warning("Improved analysis failed")
                self.results['step4_analyze_improved'] = 'failed'
        
        # Deploy
        if deploy and success:
            if self.deploy_new_model():
                self.results['deployment'] = 'completed'
            else:
                logger.error("Deployment failed!")
                success = False
        
        # Generate summary
        self.generate_summary()
        
        if success:
            self.log_header("RETRAINING PIPELINE COMPLETED SUCCESSFULLY")
            logger.info("\nNext steps:")
            logger.info("1. Review the false_positive_analysis reports")
            logger.info("2. Test the new model in production")
            logger.info("3. Monitor false positive rate over time")
        else:
            self.log_header("RETRAINING PIPELINE COMPLETED WITH ERRORS")
            logger.error("Please review the logs above for issues")
        
        return success


def main():
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Retrain diabetic ulcer detection model'
    )
    parser.add_argument(
        '--skip',
        type=str,
        nargs='+',
        choices=['validate', 'analyze_baseline', 'retrain', 'analyze_improved'],
        help='Skip specific steps'
    )
    parser.add_argument(
        '--no-deploy',
        action='store_true',
        help='Skip detailed analysis, only retrain'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Skip validation and baseline analysis'
    )
    
    args = parser.parse_args()
    
    skip_steps = args.skip or []
    
    if args.quick:
        skip_steps.extend(['validate', 'analyze_baseline'])
    
    pipeline = RetrainingPipeline()
    success = pipeline.run_full_pipeline(
        skip_steps=skip_steps,
        deploy=not args.no_deploy
    )
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
