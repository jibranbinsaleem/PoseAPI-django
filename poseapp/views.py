from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse, JsonResponse
from PIL import Image
import io
import secrets

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import APIKey, User
from .serializers import UserSerializer, GenerateApiKeySerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .functions import inferpoints





def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def index(request):
    return HttpResponse("Welcome to PoseApp!")

@swagger_auto_schema(
    method='post',
    request_body=UserSerializer,
    responses={
        201: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'message': openapi.Schema(type=openapi.TYPE_STRING, description="User created successfully"),
            },
        ),
        400: 'Bad request',
    },
)
@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=GenerateApiKeySerializer,
    responses={
        200: openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'api_key': openapi.Schema(type=openapi.TYPE_STRING, description='API key'),
                'api_secret': openapi.Schema(type=openapi.TYPE_STRING, description='API secret'),
            },
        ),
        403: 'User is not active',
        404: 'User not found',
        400: 'Bad request',
    },
)
@api_view(['POST'])
def generate_api_key(request):
    serializer = GenerateApiKeySerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        firebase_id = serializer.validated_data['firebase_id']

        try:
            user = User.objects.get(username=username, email=email, firebase_id=firebase_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_active:
            # Generate a new API key for the authenticated user
            api_key = secrets.token_urlsafe(16)
            api_secret = secrets.token_urlsafe(32)
            hashed_secret = make_password(api_secret)
            APIKey.objects.create(user=user, key=api_key, secret=hashed_secret)
            return Response({"api_key": api_key, "api_secret": api_secret}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "User is not active"}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
def infer(request):
    try:
        if 'file' not in request.FILES:
            return JsonResponse({"error": "No file part in the request"}, status=400)
        
        # Get the file from the request
        file = request.FILES['file']

        # Check if file is empty
        if file.name == '':
            return JsonResponse({"error": "No selected file"}, status=400)

        # Check if the file is an image
        if file and allowed_file(file.name):
            # Open the image file
            input_image = Image.open(io.BytesIO(file.read()))

            # Process the image
            keypoints = inferpoints(input_image)

            return JsonResponse(keypoints, safe=False, status=200)

        else:
            return JsonResponse({"error": "Invalid file type. Please upload an image file."}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)





# @api_view(['POST'])
# def login_user(request):
#     # Implement your login logic here
#     # This is just a placeholder
#     username = request.data.get('username')
#     password = request.data.get('password')
#     if username and password:
#         # Check if username and password are valid
#         # If valid, return authentication token or session ID
#         return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
#     return Response({"message": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)
