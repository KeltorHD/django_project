from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User
import uuid

class SchoolClass(models.Model):
    school_class = models.CharField(max_length=10, help_text = 'Класс')
    def __str__(self):
        return self.school_class
        # Возвращает id 0_о
    def get_absolute_url(self):
        return reverse('class-detail', args=[str(self.id)])
    class Meta:
    	ordering = ['school_class']

class People(models.Model):
    first_name = models.CharField(max_length=100, help_text = 'Имя учащегося')
    last_name = models.CharField(max_length=100, help_text = 'Фамилия учащегося')
    school_class = models.ForeignKey(SchoolClass, help_text = 'Класс ученика', on_delete = models.SET_NULL, null=True)
    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class State(models.Model):
    date = models.DateField(help_text = '- в формате дд.мм.гггг')
    status = models.CharField(max_length=1)
    people = models.ManyToManyField(People, 
        help_text = '-выберите только тех, кто пришел!',
        related_name="peoples",
        blank = 'true')
    school_class = models.CharField(max_length=10)
    school_class_id = models.CharField(max_length=10)
    author = models.CharField(max_length=100)
    availability = models.CharField(max_length=2)

    def __str__(self):
        return '{} {}'.format(self.date, self.people.__str__())

    def get_absolute_url(self):
        return reverse('date-detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date']