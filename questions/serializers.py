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
    user_answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('theme', 'thumbnail', 'question_text', 'choice1', 'choice2','user_answer')  # 必要なフィールドを追加

    def get_user_answer(self, obj):
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
    author = serializers.SerializerMethodField()
    class Meta:
        model = Question
        fields = ('question_id', 'user_id', 'theme', 'thumbnail','question_text', 'choice1', 'choice2', 'author')

    def get_author(self, obj):
        try:
            # `user_id` がUUID形式かを確認する
            user_id = uuid.UUID(str(obj.user_id))  # UUIDに変換できない場合、エラーをキャッチする
            # `user_id` で User オブジェクトを取得
            user = User.objects.get(user_id=user_id)
            return user.username
        except (User.DoesNotExist, ValueError):
            return None  # 無効なUUIDまたはユーザーが見つからない場合は None を返す
        

# ユーザー回答
class UserAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User_Answer
        fields = ('question_id', 'user_id', 'choice', 'reason')
    def create(self, validated_data):
        user_answer = User_Answer.objects.create(**validated_data)
        return user_answer
    
