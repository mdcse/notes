from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserDashboardSerializer, UserLoginSerializer, UserPasswordResetSerializer, UserRegistrationSerializer, UserChangePasswordSerializer, SendPasswordResetEmailSerializer
from django.contrib.auth import authenticate
from account.renderers import AuthRenders
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# Generate tokens for user manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    renderer_classes = (AuthRenders,)
    def post(self, request, format=None):
        print("User Registration called")
        # print(request.data['password'])
        # print(request.data['password2'])
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()  
            token = get_tokens_for_user(serializer.instance)
            return Response({'token':token, 'message':"Registration Successfull"}, status=status.HTTP_201_CREATED,)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserLoginView(APIView):
    renderer_classes = (AuthRenders,)
    def post(self, request, format=None):
        print("UserLoginView called")
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                print("user found")
                token = get_tokens_for_user(user)
                return Response({'token':token, 'message':'Login successfull'}, status=status.HTTP_200_OK)
            else:
                print("user not found")
                return Response({'ErrorDetail':'User name or password is incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # print("serializer not valid")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class UserDashboardView(APIView):
    renderer_classes = (AuthRenders,)
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print("UserDashboardView called")
        serializer = UserDashboardSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UserChangePasswordView(APIView):
    renderer_classes = (AuthRenders,)
    permission_classes = [IsAuthenticated]
    def patch(self, request, format=None):
        print("UserChangePasswordView called")
        serializer = UserChangePasswordSerializer(data=request.data, context = {'user':request.user})
        if serializer.is_valid():
            return Response({'message':'Password changed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


class SendPasswordResetEmailView(APIView):
    renderer_classes = (AuthRenders,)
    def post(self, request, format=None):
        print("SendPasswordResetEmail called")
        serializer = SendPasswordResetEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            return Response({'message':'Password Reset Email has been sent to your Email'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UserPasswordResetView(APIView):
    renderer_classes = (AuthRenders,)
    print("UserPasswordResetView Called")
    def post(self, request, uid, token, format = None):
        serializer = UserPasswordResetSerializer(data=request.data, context = {'uid':uid, 'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'message':'Password reset successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    