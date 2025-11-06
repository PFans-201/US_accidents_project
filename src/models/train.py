"""Model training module - to be implemented in Step 7."""

import logging
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def train_model(X_train, y_train, model_type='xgboost'):
    """
    Train a machine learning model.
    
    To be implemented in Step 7.
    """
    logger.info(f"Training {model_type} model...")
    raise NotImplementedError("To be implemented in Step 7")


if __name__ == "__main__":
    logger.info("Model training module - awaiting implementation")
