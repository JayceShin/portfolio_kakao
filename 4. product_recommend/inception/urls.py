from django.urls import path
from inception.views import CalView, QuizView, RecommendView, ImageView

urlpatterns = [
    path('cal/<str:num>', CalView.as_view(), name='inception'),
    path('quiz/<int:num>', QuizView.as_view(), name='inception'),
    path('recommend/<str:image>', RecommendView.as_view(), name='inception'),
    path('image', ImageView.as_view(), name='inception')
]