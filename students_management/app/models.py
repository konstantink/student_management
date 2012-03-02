from django.db import models
from sorl.thumbnail import ImageField

# Create your models here.
class Student(models.Model):
    id = models.AutoField(primary_key=True)
    firstName = models.CharField(max_length=32, null=False)
    lastName = models.CharField(max_length=32, null=False)
    middleName = models.CharField(max_length=32, null=False)
    photo = ImageField(upload_to="/images")
    birthday = models.DateField(null=False)
    studentTicket = models.IntegerField(null=False)
    groupId = models.ForeignKey('app.Group', blank=True, null=True, on_delete=models.SET_NULL)


class Group(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=32, null=False)
    seniorId = models.ForeignKey(Student, default=None, blank=True, null=True, on_delete=models.SET_NULL)

