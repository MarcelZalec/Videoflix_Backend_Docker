from rest_framework import serializers
from django.contrib.auth import authenticate
from auth_app.models import CustomUserModel


class RegistrationSerializer(serializers.ModelSerializer):
    repeated_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUserModel
        fields = ['email','remember', 'provider', 'password', 'repeated_password']

    def validate(self, data):
        """
        Validate the input data before creating a user.

        - Checks if the passwords match.
        - Ensures the email is not already in use.
        """
        if data['password'] != data['repeated_password']:
            raise serializers.ValidationError({'error': 'Passwords do not match!'})
        
        if CustomUserModel.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError(
                {'error': 'This email is already in use!'})
            
        return data
    
    def create(self, validated_data):
        """
        Remove the repeated password and create a new user.
        
        :param validated_data: Dictionary of validated input fields
        :return: Newly created user instance
        """
        validated_data.pop('repeated_password')
        user = CustomUserModel.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    remember = serializers.BooleanField(required=False)
    
    def validate(self, data):
        """
        Validates the given data for a login request.

        :param data: A dictionary of the given data
        :return: The validated data with the user object added
        :raises: serializers.ValidationError if the credentials are invalid
        :raises: serializers.ValidationError if either email or password is empty
        """
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("Invalid login credentials")
        else:
            raise serializers.ValidationError("Both fields must be filled")

        data['user'] = user
        return data


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)