from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

# Define forms
# We can define forms that 
#   - manage(get, hold, verify/clean and etc.) form field data
#   - control how to be rendered by HTML

class SignUpForm(UserCreationForm):
    # Custom user registration form
    #
    # Inherits from:
    #   UserCreationForm: username, password1 and password2 fields
    #
    # Additional fields:
    #   email

    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",         # Add help text
        widget=forms.EmailInput(attrs={'class': 'form-contrl'})     # Add widget, that contorols how the form filed is rendered as HTML
        )

    class Meta:
        # Defines the model and fields

        model = User    # Uses Django's built-in User model
        fields = ('username', 'email', 'password1', 'password2')

        # Customize widgets for styling
        widgets = {
            'username': forms.TextInput(attrs={'class': 'from-control'})
        }

    def clean_email(self):
        # Custom validation to ensure email is unique

        email = self.cleaned_data.get('email')
        if User.object.filter(email=email).exists():
            raise forms.ValidationError('This email address is alreay in use.')
        return email
        
    def __init__(self, *args, **kwargs):
        # Initialize th form and CSS classes to password fields for styling

        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class TaskForm(forms.ModelForm):
    # Form for creating and updating a task

    # This is a ModelForm that automatically:
    #   - Generates form fields based on the Task Model
    #   - Handles form validation based on the model field definition
    #   - Saves data to the model directly

    class Meta:
        # Defines the model and fields

        model = Task
        fields = ('title', 'description', 'completed')

        # Custom widgets
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter task title',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter task description',
            }),
            'completed': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            })
        }
    
    def __init__(self, *args, **kwargs):
        # Initialize the form and set custom labels and help text

        super(TaskForm, self).__init__(*args, **kwargs)

        # Customize form labels
        self.fields['title'].label = 'Task Title'
        self.fields['description'].label = 'Description'
        self.fields['completed'].label = 'Mark as completed'

        # Add help text
        self.fields['title'].help_text = 'Enter a short descriptive title'
        self.fields['description'].help_text = 'Add details about your task'

    def clean_title(self):
        # Custom validation for the title field
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise forms.ValidationError('Title must be at least 3 characters long.')
        return title
    