from django.contrib import admin
from django.contrib import messages  # Import messages for notifications
from .models import Student

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'age', 'address', 'interest', 'course', 'gender')
    search_fields = ('first_name', 'last_name', 'email', 'address', 'interest', 'course', 'gender')

    # Override the save_model method to add success notification after saving a student
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change:
            # If it's an update (not a new object)
            messages.success(request, f"Student {obj.first_name} {obj.last_name} has been updated successfully!")
        else:
            # If it's a new student
            messages.success(request, f"Student {obj.first_name} {obj.last_name} has been added successfully!")

    # Override the delete_model method to add a success notification after deleting a student
    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        messages.success(request, f"Student {obj.first_name} {obj.last_name} has been deleted successfully!")
