from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.generics import GenericAPIView
from .models import User, AccessToken
from rest_framework.permissions import AllowAny
from rest_framework import viewsets

from .serializers import QuestionSerializer

# HelloWorld
def helloworldfunction(request):
    return render(request, 'index.html')


class QuestionView(APIView):
    @staticmethod
    def post(request, *args, **kwargs):
        print(request.data)
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # エラーなし
            try:
                question = serializer.save()
            except:
                # データベースエラー
                return Response({'error': 'サーバー接続が切れました'}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            response_data = {
               'question_id': str(question.question_id)
            }

            return Response(response_data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

