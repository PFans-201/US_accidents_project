"""Model evaluation module - to be implemented in Step 8."""

import logging
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def evaluate_model(model, X_test, y_test):
    """
    Evaluate a trained model.
    
    To be implemented in Step 8.
    """
    logger.info("Evaluating model...")
    raise NotImplementedError("To be implemented in Step 8")


if __name__ == "__main__":
    logger.info("Model evaluation module - awaiting implementation")
