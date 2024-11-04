from rest_framework import serializers
from .models import User, Question, User_Answer

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ( 'theme', 'question_text', 'choice1', 'choice2')

        def create(self, validated_data):
            question = Question.objects.create(**validated_data)
            return question
        

