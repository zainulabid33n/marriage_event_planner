from rest_framework.response import Response


def custom_response(status=True, message="success", result=None):
    """Unified Response """
    return Response({'status': status, 'result': result, "message": message})
