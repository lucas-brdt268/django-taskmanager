from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, TaskForm
from .models import Task

# Create your views here.

def home(request):
    # Home page view
    # Renders the main landing page that users see when they first visit the site.
    return render(request, 'home.html')

def signup_view(request):
    # User registration view
    # Handles both GET(display form) and POST(process form submission) requests

    # For POST request
    if request.method == 'POST':
        # Create form instance that holds form data
        form = SignUpForm(request.POST)

        # Validate form data
        if form.is_valid():
            # Save new user into DB and get the created user
            user = form.save()
            # Login the user after registration, i.e., create a session for the new user
            login(request, user)
            # Redirect to the task list page
            return redirect('task_list')
    # For GET request
    else:
        # Create a blank form
        form = SignUpForm()

    # Render the signup template with 
    # the blank form data when handling GET request,
    # old form data when the form POST request is not valid
    return render(request, 'auth/signup.html', {'form': form})

@login_required
def task_list(request):
    # Show task list
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    # Create a task
    # Handles both GET(display form) and POST(process form submission) requests

    # For POST request
    if request.method == 'POST':
        # Create form instance
        form = TaskForm(request.POST)

        # Validate form data
        if form.is_valid():
            # Create  task instance from from
            # Because Commit is False, so form data don't save to DB yet
            task = form.save(commit=False)

            # Assign the current user to the user field of the task
            task.user = request.user

            # Now save the task to DB
            task.save()

            # Redirect to the task list view
            return redirect('task_list')
    
    # For GET request
    else:
        # Create an empty task form instance
        form = TaskForm()

    # Render the form template when
    #   - form POST request is not valid
    #   - GET request is handled
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    # Update an existing task
    #
    # Parameters:
    #   pk - Primary key of the task to update
    
    # Retrieve the task and if not exist, return 404
    task = get_object_or_404(Task, pk=pk, user=request.user)

    # For POST
    if request.method == 'POST':
        # Bind form with the submitted data and the existing instance
        form = TaskForm(request.POST, instance=task)

        # Validate form data
        if(form.is_valid):
            # Save updated task
            form.save()
            # Redirect to the task list view
            return redirect('task_list')
        
    # For GET
    else:
        # Pre-fill form with existing task data
        form = TaskForm(instance=task)

    # Render the form template when
    #   - form POST request is not valid
    #   - GET request is handled
    return render(request, 'task_form.html', {'form': form, 'object': task})

@login_required
def task_delete(request, pk):
    print('k1')
    # Delete an task
    #
    # Parameters:
    #   pk - Primary key of the task to delete

    # Retrieve the task with given pk
    task = get_object_or_404(Task, pk=pk, user=request.user)

    # For POST
    if request.method == 'POST':
        # Only delete on POST (confirmation)
        task.delete()
        return redirect('task_list')
    print('k2')
    # For GET
    return render(request, 'task_confirm_delete.html', {'task': task})

