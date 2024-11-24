from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
    """
    Custom exception handler for DRF.
    """
    # Call the default exception handler
    response = exception_handler(exc, context)

    # Log the exception
    if response is not None:
        logger.error(
            f"Exception occurred: {exc} (context: {context})"
        )
    else:
        logger.critical(f"Unhandled exception: {exc}")

    # Return the standard response
    return response
