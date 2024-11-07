from django.urls import path
from .views import *
urlpatterns = [
    path('', QuestionView.as_view(), name='questions'),
    path('<uuid:question_id>/', QuestionDetailView.as_view(), name='question-detail'),
    path('answer/', UserAnswerView.as_view(), name='answer')
]
