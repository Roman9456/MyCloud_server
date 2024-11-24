from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    """
    Custom exception handler for formatting error responses.
    This handler is used to modify the default error response structure.
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Modify the error response to include custom 'error' structure
        response.data = {
            'error': {
                'code': response.status_code,  # Error code (HTTP status code)
                'message': response.data.get('detail', 'Server error')  # Error message, default to 'Server error'
            }
        }
    
    return response
