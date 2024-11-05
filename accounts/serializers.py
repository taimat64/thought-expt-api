from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'password', 'username', 'email')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
        
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        email_ = User.objects.get(email=email)
        re_password = User.objects.get(password=password)
        if email == email_.email:
            if password == re_password.password:
                return data
            
            else:
                raise serializers.ValidationError('ログイン失敗')

