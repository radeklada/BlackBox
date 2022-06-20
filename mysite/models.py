from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# modele w bazie danych dla kolejno aplikacji, testu, kroku dla konkretnego testu
class Application(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)

class Test(models.Model):
    app = models.ForeignKey(Application, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    result = models.CharField(max_length=500)
    date = models.DateField(auto_now_add=True)

class TestStep(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    description = models.CharField(max_length=500)
    requirements = models.CharField(max_length=500)