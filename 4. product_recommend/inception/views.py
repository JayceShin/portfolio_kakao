# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from inception.models import Question, Quiz, Calculator, RecommendResult, JoinList
from inception.serializer import QuestionSerializer, QuizSerializer, CalculatorSerializer, RecommendSerializer, JoinSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from inception.dbConnect import Con
from inception.retrain_run_inference import Train
from inception.imageAPI import Image
from datetime import datetime


# Create your views here.


class QuizView(APIView):

    def get_object(self):
        try:
            return Quiz.objects.all()
        except Quiz.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, num):
        queryset = self.get_object().filter(id=num)
        serializer = QuizSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        queryset = Quiz.objects.get(id=request.data['id'])
        queryset.delete()
        return Response(data='Delete', status=status.HTTP_410_GONE)

    def put(self, request):
        quiz = Quiz.objects.get(id= request.data['id'])
        serializer = QuizSerializer(quiz, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(data=serializer.errors, status=status.HTTP_404_NOT_FOUND)

'''
class QuizView(generics.ListAPIView
               , generics.ListCreateAPIView
               , generics.UpdateAPIView
               , generics.DestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
'''


class CalView(APIView):

    def get_object(self):
        try:
            return Calculator.objects.all()
        except Calculator.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, num):
        temp = Con()
        temp.insert(num)
        queryset = self.get_object().filter(num=num)
        serializer = CalculatorSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class RecommendView(APIView):

    def get_object(self):
        try:
            return JoinList.objects.all()
        except JoinList.DoesNotExist:
            raise status.HTTP_404_NOT_FOUND

    def get(self, request, image):
        train = Train()
        now = datetime.now()
        train.main(image, now)
        queryset = self.get_object().filter(time=now).order_by("result")
        serializer = JoinSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ImageView(APIView):
    def get(self, request):
        image = Image()
        image.getImage()
        return Response(status=status.HTTP_200_OK)