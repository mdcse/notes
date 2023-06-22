from rest_framework import serializers
from account.models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from account.utils import Utils


class UserRegistrationSerializer(serializers.ModelSerializer):
    # print("UserRegistrationSerializer called")
    password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}
        # print("Meta called")
        
    def validate(self, data):
        # print("validate called")
        password = data.get('password', None)
        password2 = data.get('password2', None)
        print(password)
        print(password2)
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
            
        return data
        
    def create(self, validated_data):
        user = User.objects.create_user(
              **validated_data
            )
        return user



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['password', 'email']


class UserDashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'tc']
        

        

class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']
        # extra_kwargs = {'password': {'write_only': True}}
        
    

    def validate(self, data):
    
        password = data.get('password', None)
        password2 = data.pop('password2', None)
        user = self.context.get('user')
        print(user)
        if password != password2:
            raise serializers.ValidationError(
                {'password': 'Passwords must match.'})
        user.set_password(password)
        user.save()
        return data

        
class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    
    class Meta:
        fields = ['email']
        
    def validate(self, data):
        email = data.get('email')
        user = User.objects.get(email=email)
        if not user:
            raise serializers.ValidationError(
                {'email': 'Email does not exist.'})
        uid = urlsafe_base64_encode(force_bytes(user.id))
        # print(user.id, uid)
        # print("user", user)
        token = PasswordResetTokenGenerator().make_token(user)
        # print("token", token)
        link = 'http://localhost:3000/api/user/reset/' + uid + '/' + token
        print("Password Reset Link", link)
        print(user.email)
        #Send Email
        body = 'Click the link to reset your password ' + link
        data = {
            'subject':'Reset Your Password',
            'body':body,
            'to_email':user.email
        }
        Utils.send_email(data)
        print("Email Sent")

        return data
    
class UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    password2 = serializers.CharField(max_length = 255, style = {'input_type':'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['password', 'password2']


    def validate(self, data):
        try:
            password = data.get('password')
            password2 = data.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            # print(uid)
            # print(token)

            if password != password2:
                raise serializers.ValidationError(
                    {'password': 'Passwords must match.'})
            id = smart_str(urlsafe_base64_decode(uid))
            print(id, uid)
            user = User.objects.get(id=id)
            print(user)
            if not PasswordResetTokenGenerator().check_token(user, token):
                print('token mimatched')
                raise ValueError({'message' : 'Token is invalid or Expired'})
            user.set_password(password)
            user.save()
        except DjangoUnicodeDecodeError:
            PasswordResetTokenGenerator().check_token(user, token)
            raise ValueError({'message' : 'Token is Modified or Expired'})
        return data
