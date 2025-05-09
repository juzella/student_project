from django import forms
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'age', 'address', 'interest', 'course', 'gender']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter address'}),
            'interest': forms.Textarea(attrs={'rows': 2, 'class': 'form-control', 'placeholder': 'Enter your interests'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
        }
