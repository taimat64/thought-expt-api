from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'username', 'email')
        extra_kwargs = {'password': {'write_only': True}}

        def create(self, validated_data):
            user = User.objects.create_user(**validated_data)
            return user
        
class LoginSerializer(serializers.Serializer):
    user_id = serializers.CharField(max_length=255, write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    def validate(self, data):
        user_id = data.get('user_id')
        password = data.get('password')
        userid = User.objects.get(user_id=user_id)
        re_password = User.objects.get(password=password)
        if user_id == userid.user_id:
            if password == re_password.password:
                return data
            
            else:
                raise serializers.ValidationError('ログイン失敗')

