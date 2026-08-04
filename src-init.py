"""
DERS-X: Calibrated Multimodal Distress-Like Affect Modeling
"""

from .config import Config
from .dataset import HFIEMOCAPDataset, collate_fn
from .model import DERSXModel, DistressRepresentationBlock
from .trainer import run_loso_experiment, fit_one_setting
from .metrics import eval_emotion_metrics, eval_distress_metrics, expected_calibration_error
from .utils import set_seed, mean_std, save_latex_table

__all__ = [
    "Config",
    "HFIEMOCAPDataset",
    "collate_fn",
    "DERSXModel",
    "DistressRepresentationBlock",
    "run_loso_experiment",
    "fit_one_setting",
    "eval_emotion_metrics",
    "eval_distress_metrics",
    "expected_calibration_error",
    "set_seed",
    "mean_std",
    "save_latex_table",
]

__version__ = "1.0.0"