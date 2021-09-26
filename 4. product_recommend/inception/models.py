from django.db import models

# Create your models here.


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(verbose_name='description', null=True)
    created_date = models.DateField(auto_now=True)
    url = models.URLField(verbose_name='url', null=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, null=True)
    question = models.TextField(verbose_name='question', null=True)
    choice1 = models.TextField(verbose_name='choice1', null=True)
    choice2 = models.TextField(verbose_name='choice1', null=True)
    choice3 = models.TextField(verbose_name='choice1', null=True)
    choice4 = models.TextField(verbose_name='choice1', null=True)
    choice5 = models.TextField(verbose_name='choice1', null=True)
    answer = models.CharField(max_length=10)


class Calculator(models.Model):
    num = models.TextField(verbose_name='number', null=True)
    oper = models.TextField(verbose_name='operator', null=True)
    res = models.TextField(verbose_name='result', null=True)


class RecommendResult(models.Model):
    image = models.TextField(verbose_name='image', null=False)
    item = models.TextField(verbose_name='item', null=False)
    result = models.TextField(verbose_name='result', null=False)
    time = models.TextField(verbose_name='result', null=False)


class ItemList(models.Model):
    item = models.TextField(verbose_name='item', null=False)
    itemName = models.TextField(verbose_name='product', null=False)
    price = models.TextField(verbose_name='price', null=False)
    stock = models.TextField(verbose_name='stock', null=False)
    store = models.TextField(verbose_name='store', null=False)
    storeName = models.TextField(verbose_name='store', null=False)
    phone = models.TextField(verbose_name='phone', null=False)


class JoinList(models.Model):
    item = models.TextField(verbose_name='product', null=False)
    itemName = models.TextField(verbose_name='product', null=False)
    price = models.TextField(verbose_name='price', null=False)
    stock = models.TextField(verbose_name='stock', null=False)
    store = models.TextField(verbose_name='store', null=False)
    storeName = models.TextField(verbose_name='store', null=False)
    phone = models.TextField(verbose_name='phone', null=False)
    result = models.TextField(verbose_name='result', null=False)
    time = models.TextField(verbose_name='result', null=False)
