from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages  # For notifications
from .models import Student
from .forms import StudentForm
from django.core.paginator import Paginator
from django.db.models import Q  # For flexible search filters
from django.http import JsonResponse
import json
from .ml_model import CoursePredictor
from django.views.decorators.csrf import csrf_exempt

def student_list(request):
    query = request.GET.get('q', '')
    students = Student.objects.all()

    if query:
        terms = query.strip().split()
        if len(terms) == 1:
            students = students.filter(
                Q(first_name__icontains=terms[0]) |
                Q(last_name__icontains=terms[0]) |
                Q(email__icontains=terms[0])
            )
        else:
            # Try to match first name and last name together
            students = students.filter(
                Q(first_name__icontains=terms[0], last_name__icontains=terms[-1]) |
                Q(email__icontains=query)
            )

    paginator = Paginator(students, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query
    }

    return render(request, 'student_app/student_list.html', context)


def student_create(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Student has been added successfully!")  # Success notification
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'student_app/student_form.html', {'form': form})


def student_update(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Student details have been updated successfully!")  # Success notification
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'student_app/student_form.html', {'form': form})


def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.delete()
        messages.success(request, "Student has been deleted successfully!")  # Success notification
        return redirect('student_list')
    return render(request, 'student_app/student_confirm_delete.html', {'student': student})


def train_model(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
        
    predictor = CoursePredictor()
    students = Student.objects.all()
    
    if len(students) < 10:  # Ensure we have enough data to train
        return JsonResponse({'error': 'Not enough student data for training. Need at least 10 students.'}, status=400)
    
    try:
        ages = [student.age for student in students]
        genders = [student.get_gender_display() for student in students]
        interests = [student.interest for student in students]
        courses = [student.course for student in students]
        
        result = predictor.train(ages, genders, interests, courses)
        
        if result['success']:
            metrics = result['metrics']
            return JsonResponse({
                'message': 'Model trained successfully',
                'accuracy': f"{metrics['training_accuracy']:.2f}",
                'cv_score': f"{metrics['cv_mean']:.2f} (+/- {metrics['cv_std']:.2f})"
            })
        else:
            return JsonResponse({'error': result['error']}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt  # Add this decorator
def predict_course(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            age = int(data.get('age'))
            gender = data.get('gender')
            interest = data.get('interest')
            
            predictor = CoursePredictor()
            if not predictor.load_model():
                return JsonResponse({'error': 'Model needs to be trained first. Please add at least 10 students and train the model.'}, status=400)
            
            # Validate input data
            if not all([age, gender, interest]):
                return JsonResponse({'error': 'All fields are required'}, status=400)
            
            result = predictor.predict(age, gender, interest)
            if result['success']:
                return JsonResponse({
                    'predicted_course': result['predicted_course'],
                    'confidence': result['confidence']
                })
            else:
                return JsonResponse({'error': result['error']}, status=400)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)


def get_model_status(request):
    predictor = CoursePredictor()
    predictor.load_model()
    info = predictor.get_model_info()
    return JsonResponse(info)


def register_student(request):
    if request.method == 'POST':
        # Get the form data
        student_data = {
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'email': request.POST.get('email'),
            'age': request.POST.get('age'),
            'gender': request.POST.get('gender'),
            'address': request.POST.get('address'),
            'interest': request.POST.get('interest'),
            'course': request.POST.get('course')  # Add the predicted course
        }
        
        form = StudentForm(student_data)
        
        if form.is_valid():
            student = form.save()
            messages.success(request, "Registration successful!")
            return redirect('student_list')
        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'student_app/registration.html', {'form_errors': form.errors})
    
    return render(request, 'student_app/registration.html')


def test_prediction(request=None):
    """Test function to directly test the course prediction system"""
    predictor = CoursePredictor()
    
    try:
        # Load existing model if available
        if not predictor.load_model():
            # If no model exists, train with current data
            students = Student.objects.all()
            if len(students) < 10:
                return {'error': 'Need at least 10 students to train the model'}
                
            ages = [student.age for student in students]
            genders = [student.get_gender_display() for student in students]
            interests = [student.interest for student in students]
            courses = [student.course for student in students]
            
            result = predictor.train(ages, genders, interests, courses)
            if not result['success']:
                return {'error': result['error']}
        
        # Test predictions with different interest combinations
        test_cases = [
            {'age': 18, 'gender': 'Male', 'interest': 'Technology'},
            {'age': 19, 'gender': 'Female', 'interest': 'Science'},
            {'age': 20, 'gender': 'Other', 'interest': 'Arts'},
            {'age': 18, 'gender': 'Male', 'interest': 'Coding'},
            {'age': 19, 'gender': 'Female', 'interest': 'Web Development'}
        ]
        
        predictions = []
        for case in test_cases:
            result = predictor.predict(**case)
            if result['success']:
                predictions.append({
                    'input': case,
                    'predicted_course': result['predicted_course'],
                    'confidence': result['confidence']
                })
            else:
                predictions.append({
                    'input': case,
                    'error': result['error']
                })
        
        return {'success': True, 'predictions': predictions}
        
    except Exception as e:
        return {'error': str(e)}
