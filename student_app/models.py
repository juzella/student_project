from django.db import models

class Student(models.Model):
    # Define integer constants for gender choices
    MALE = 1
    FEMALE = 2
    OTHER = 3
    
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField(default='Not Provided')
    email = models.EmailField()
    gender = models.IntegerField(choices=GENDER_CHOICES, default=OTHER)
    age = models.IntegerField()
    interest = models.TextField()
    course = models.CharField(max_length=100, default='BSCS')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"