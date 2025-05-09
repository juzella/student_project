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

    # Define choices for courses
    COURSE_CHOICES = [
        ('BSCS', 'Bachelor of Science in Computer Science'),
        ('BSIT', 'Bachelor of Science in Information Technology'),
        ('BFA', 'Bachelor of Fine Arts'),
        ('BA-LIT', 'Bachelor of Arts in Literature'),
        ('BSEE', 'Bachelor of Science in Electrical Engineering'),
        ('BSME', 'Bachelor of Science in Mechanical Engineering'),
        ('BSMath', 'Bachelor of Science in Mathematics'),
        ('BSPhysics', 'Bachelor of Science in Physics'),
        ('BMus', 'Bachelor of Music'),
        ('BSPE', 'Bachelor of Science in Physical Education'),
        ('BSIS', 'Bachelor of Science in Information Systems'),
        ('BSData', 'Bachelor of Science in Data Science'),
        ('BDes', 'Bachelor of Design'),
        ('BBA', 'Bachelor of Business Administration'),
        ('BSPsych', 'Bachelor of Science in Psychology'),
        ('BSMed', 'Bachelor of Science in Medical Sciences'),
        ('BA-Lang', 'Bachelor of Arts in Foreign Languages'),
        ('BBA-DM', 'Bachelor of Business Administration in Digital Marketing'),
        ('BA-Anim', 'Bachelor of Arts in Animation'),
        ('BA-Photo', 'Bachelor of Arts in Photography'),
        ('BSRobo', 'Bachelor of Science in Robotics Engineering'),
        ('BSAI', 'Bachelor of Science in Artificial Intelligence'),
        ('BSGame', 'Bachelor of Science in Game Development'),
        ('BArch', 'Bachelor of Architecture'),
        ('BSFash', 'Bachelor of Science in Fashion Technology'),
        ('BSEnv', 'Bachelor of Science in Environmental Science'),
        ('BA-Comm', 'Bachelor of Arts in Mass Communication'),
        ('BA-Film', 'Bachelor of Arts in Film Production'),
        ('BS-Cul', 'Bachelor of Science in Culinary Arts Management')
    ]

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.TextField(default='Not Provided')
    email = models.EmailField()
    gender = models.IntegerField(choices=GENDER_CHOICES, default=OTHER)
    age = models.IntegerField()
    interest = models.TextField()
    course = models.CharField(max_length=100, choices=COURSE_CHOICES, default='BSCS')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"