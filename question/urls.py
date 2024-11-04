from django.urls import path
from . import views
from .views import QuestionView

urlpatterns = [
    path('', views.helloworldfunction),
    path('questions/', QuestionView.as_view())
]
