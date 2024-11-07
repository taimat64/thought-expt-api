from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Question
from .serializers import *
from accounts.models import User

class QuestionView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = QuestionPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                question = serializer.save()  # シリアライザが自動的にuser_idを設定して保存
            except Exception as e:
                return Response({'error': 'サーバー接続が切れました', 'details': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            response_data = {
                'question_id': str(question.question_id)
            }
            return Response(response_data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        queryset = Question.objects.all()
        serializer = ListQuestionsSerializer(queryset, many=True)
        responce_data = {
            'questions': serializer.data 
        }
        return Response(responce_data)
    

class QuestionDetailView(APIView):
    def get(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        try:
            question = Question.objects.get(question_id=question_id)
            serializer = QuestionSerializer(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        

class UserAnswerView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UserAnswerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user_answer = serializer.save()  # シリアライザが自動的にuser_idを設定して保存
            except Exception as e:
                return Response({'error': 'サーバー接続が切れました', 'details': str(e)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            
            response_data = {
                'question_id': str(user_answer.question_id)
            }
            return Response(response_data, status=HTTP_201_CREATED)
        
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    
class QuestionDetailAnswerView(APIView):
    def get(self, request, *args, **kwargs):
        question_id = kwargs.get('question_id')
        try:
            question = Question.objects.get(question_id=question_id)
            serializer = QuestionDetailSerializer(question)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response({"error": "Question not found"}, status=status.HTTP_404_NOT_FOUND)
        