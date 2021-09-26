from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view(['GET'])
def index(request):
    message = "This is the test url"
    return Response(data=message, status=status.HTTP_200_OK)

