from rest_framework import serializers
from backend.models import *
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'password', 'account_reference', 'account_number', 'account_balance']
        

    def validate(self, data):
        password = data.get('password')
        try:
            # Use Django's password validation to ensure a strong password
            validate_password(password=password)
        except ValidationError as e:
            # Print the validation error details
            print(f"Validation error: {e.messages}")
            raise serializers.ValidationError(e.messages)

        return data

    def to_representation(self, instance):
        return {
            'status': 'error',
            'message': 'Validation error',
            'errors': self.errors,
        }

    def create(self, validated_data):
        try:
            # Try to create the user
            user = User.objects.create_user(**validated_data)
            return user
        except ValidationError as ve:
            # Handle validation error and include it in the response
            self.errors = ve.messages
            return None
        except Exception as e:
            # Print the error and raise the exception again
            print(f"Error creating user: {e}")
            raise e

class AirtimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airtime
        fields = ['user', 'amount', 'network', 'phone_number', 'successful']