from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.CharField(max_length=100)


class MotivationalPhrase(models.Model):
    phrase = models.CharField(max_length=128,
                              verbose_name="Frase")

    class Meta:
        verbose_name = "Frase"
        verbose_name_plural = "Frasi"

    def __str__(self):
        return self.phrase
