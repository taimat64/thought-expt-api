from rest_framework import serializers
from .models import Question, User_Answer
from accounts.models import User
import uuid

#　問題
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('theme', 'thumbnail', 'question_text', 'choice1', 'choice2')

#　問題詳細
class QuestionDetailSerializer(serializers.ModelSerializer):
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('theme', 'thumbnail', 'question_text', 'choice1', 'choice2','answers')  # 必要なフィールドを追加

    def get_answers(self, obj):
        # User_Answerをquestion_idでフィルタリングして取得する
        user_answer = User_Answer.objects.filter(question_id=obj).first()  # question_idでフィルタリング
        if user_answer:
            return UserAnswerSerializer(user_answer).data  # シリアライズして返す
        return None  # ユーザーの回答がない場合はNoneを返す

#　問題投稿
class QuestionPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('user_id', 'theme', 'thumbnail', 'question_text', 'choice1', 'choice2')

    def create(self, validated_data):
        question = Question.objects.create(**validated_data)
        return question

#　問題一覧
class ListQuestionsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    count = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ('question_id', 'user_id', 'theme', 'thumbnail', 'username', 'count')

    def get_username(self, obj):
        username = User.objects.get(user_id=obj.user_id).username
        return username
        
    def get_count(self, obj):
    # 質問のIDに関連するUser_Answerをフィルタリングして、その件数をカウント
        count = User_Answer.objects.filter(question_id=obj.question_id).count()
        return count

# ユーザー回答
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Answer
        fields = ('question_id', 'user_id', 'choice', 'reason')
    def create(self, validated_data):
        user_answer = User_Answer.objects.create(**validated_data)
        return user_answer
    
