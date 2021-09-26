from rest_framework.serializers import ModelSerializer
from inception.models import Quiz, Question, Calculator, RecommendResult, JoinList


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = ('name', 'description')


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class CalculatorSerializer(ModelSerializer):
    class Meta:
        model = Calculator
        fields = '__all__'


class RecommendSerializer(ModelSerializer):
    class Meta:
        model = RecommendResult
        fields = '__all__'


class JoinSerializer(ModelSerializer):
    class Meta:
        model = JoinList
        fields = '__all__'


