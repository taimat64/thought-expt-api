from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from .models import User, AccessToken
from rest_framework.permissions import AllowAny

from .serializers import RegisterSerializer, LoginSerializer

# HelloWorld
def helloworldfunction(request):
    return render(request, 'index.html')


class RegisterView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # パスワードと確認パスワードが一致しない場合
            # if serializer.validated_data['password'] != request.data['password_confirmation']:
            #     return Response({'error': 2}, status=HTTP_400_BAD_REQUEST)

            # Emailがすでに使われていた場合
            if User.objects.filter(email=serializer.validated_data['email']).exists(): 
                return Response({'error': 'Emailが既に使われています'}, status=HTTP_400_BAD_REQUEST)

            # エラーなし
            try:
                user = serializer.save()
            except:
                # データベースエラー
                return Response({'error': 'サーバー接続が切れました'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            response_data = {
                'uuid': str(user.user_id),  # UUIDの場合は文字列に変換
                'username': user.username,
                'email': user.email,
                'error': '',
            }

            return Response(response_data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    """ログインAPIクラス"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            user = User.objects.filter(email=email).first()
            if not user:
                return Response({'error': "ユーザーが存在しません。"}, status=HTTP_404_NOT_FOUND)

            token = AccessToken.create(user=user)
            return Response({'error': 0, 'token': token.token, 'email': email})
        
        return Response({'error': 1}, status=HTTP_400_BAD_REQUEST)
