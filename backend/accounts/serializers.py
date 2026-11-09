from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidateError

User = get_user_model()

class RegistrationSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    
    class Meta:
        model = User
        
        fields = ["id", "username", "email", "password",]
        
        read_only_fields = ["id"]
        
    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("An account with this email already exists")
        
        return value
    
    def validate(self, attrs):
        candidate_user = User(username=attrs["username"], email=attrs["email"])
        try:
            validate_password(attrs["password"], user=candidate_user)
        except DjangoValidateError as exc:
            raise serializers.ValidationError({
                "password": list(exc.messages)
            })
            
        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)