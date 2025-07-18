# My First Django Project Guided By Deepseek From Zero

### Step-by-Step Guide to Building a Django Project with Authentication and CRUD

Let's build a simple Task Manager app with authentication and CRUD operations. I'll guide you through every step from environment setup to deployment.

---

### **Step 1: Environment Setup**
1. Install Python (3.8+ recommended)
2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
3. Install Django:
```bash
pip install django
```

---

### **Step 2: Create Project and App**
1. Create project:
```bash
django-admin startproject taskmanager
cd taskmanager
```
2. Create core app:
```bash
python manage.py startapp core
```
3. Register app in `taskmanager/settings.py`:
```python
INSTALLED_APPS = [
    ...,
    'core',
    'crispy_forms',  # For better form rendering
]
```
4. Install crispy forms:
```bash
pip install django-crispy-forms
```
Add to `settings.py`:
```python
CRISPY_TEMPLATE_PACK = 'bootstrap4'
```

---

### **Step 3: Setup Authentication**
1. Create templates directory:
```bash
mkdir core/templates
```
2. Create `core/templates/registration` directory for auth templates

3. Create base template `core/templates/base.html`:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container">
        <nav class="navbar navbar-expand-lg navbar-light bg-light">
            <a class="navbar-brand" href="{% url 'home' %}">Task Manager</a>
            <div class="collapse navbar-collapse">
                {% if user.is_authenticated %}
                <a href="{% url 'task_list' %}" class="btn btn-outline-primary me-2">Tasks</a>
                <a href="{% url 'logout' %}" class="btn btn-outline-danger">Logout</a>
                {% else %}
                <a href="{% url 'login' %}" class="btn btn-outline-primary me-2">Login</a>
                <a href="{% url 'signup' %}" class="btn btn-outline-success">Sign Up</a>
                {% endif %}
            </div>
        </nav>
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

4. Create auth templates:
- `core/templates/registration/login.html`:
```html
{% extends 'base.html' %}

{% block content %}
<h2>Login</h2>
<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary mt-3">Login</button>
</form>
{% endblock %}
```

- `core/templates/signup.html`:
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<h2>Sign Up</h2>
<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-success mt-3">Sign Up</button>
</form>
{% endblock %}
```

---

### **Step 4: Create Models**
Update `core/models.py`:
```python
from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
```

Create migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

### **Step 5: Create Forms**
Create `core/forms.py`:
```python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Task

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'completed']
```

---

### **Step 6: Create Views**
Update `core/views.py`:
```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, TaskForm
from .models import Task

def home(request):
    return render(request, 'home.html')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('task_list')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'task_list.html', {'tasks': tasks})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'task_form.html', {'form': form})

@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'task_confirm_delete.html', {'task': task})
```

---

### **Step 7: Create Templates**
1. `core/templates/home.html`:
```html
{% extends 'base.html' %}

{% block content %}
<h1 class="mt-5">Welcome to Task Manager</h1>
<p class="lead">Manage your tasks efficiently</p>
{% if not user.is_authenticated %}
<a href="{% url 'login' %}" class="btn btn-primary btn-lg">Login to Start</a>
{% endif %}
{% endblock %}
```

2. `core/templates/task_list.html`:
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<div class="d-flex justify-content-between align-items-center mb-4">
    <h1>Task List</h1>
    <a href="{% url 'task_create' %}" class="btn btn-success">+ New Task</a>
</div>

<ul class="list-group">
    {% for task in tasks %}
    <li class="list-group-item d-flex justify-content-between align-items-center">
        <div>
            <h5>{{ task.title }}</h5>
            <p>{{ task.description }}</p>
            <small class="text-muted">{{ task.created_at|date:"M d, Y" }}</small>
            {% if task.completed %}
            <span class="badge bg-success ms-2">Completed</span>
            {% else %}
            <span class="badge bg-warning ms-2">Pending</span>
            {% endif %}
        </div>
        <div>
            <a href="{% url 'task_update' task.pk %}" class="btn btn-sm btn-outline-primary">Edit</a>
            <a href="{% url 'task_delete' task.pk %}" class="btn btn-sm btn-outline-danger">Delete</a>
        </div>
    </li>
    {% empty %}
    <li class="list-group-item">No tasks yet</li>
    {% endfor %}
</ul>
{% endblock %}
```

3. `core/templates/task_form.html`:
```html
{% extends 'base.html' %}
{% load crispy_forms_tags %}

{% block content %}
<h1>{% if object %}Edit{% else %}Create{% endif %} Task</h1>
<form method="post">
    {% csrf_token %}
    {{ form|crispy }}
    <button type="submit" class="btn btn-primary">Save</button>
    <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

4. `core/templates/task_confirm_delete.html`:
```html
{% extends 'base.html' %}

{% block content %}
<h1>Delete Task</h1>
<p>Are you sure you want to delete "{{ task.title }}"?</p>
<form method="post">
    {% csrf_token %}
    <button type="submit" class="btn btn-danger">Confirm Delete</button>
    <a href="{% url 'task_list' %}" class="btn btn-secondary">Cancel</a>
</form>
{% endblock %}
```

---

### **Step 8: Configure URLs**
1. Create `core/urls.py`:
```python
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Task URLs
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/update/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),
]
```

2. Update `taskmanager/urls.py`:
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]
```

---

### **Step 9: Add Admin Interface**
1. Create superuser:
```bash
python manage.py createsuperuser
```
2. Register model in `core/admin.py`:
```python
from django.contrib import admin
from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'completed', 'created_at')
```

---

### **Step 10: Run and Test**
1. Run development server:
```bash
python manage.py runserver
```
2. Access at http://localhost:8000
3. Test features:
   - Sign up new user
   - Login/logout
   - Create/read/update/delete tasks
   - Visit admin at http://localhost:8000/admin

---

### **Final Project Structure**
```
taskmanager/
├── core/
│   ├── migrations/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── registration/
│   │   │   ├── login.html
│   │   ├── signup.html
│   │   ├── task_list.html
│   │   ├── task_form.html
│   │   └── task_confirm_delete.html
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── taskmanager/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── venv/
├── db.sqlite3
└── manage.py
```

### **Key Concepts Covered**
1. Django MVT (Model-View-Template) architecture
2. User authentication system
3. CRUD operations (Create, Read, Update, Delete)
4. Form handling and validation
5. Database migrations
6. Template inheritance
7. Class-based vs function-based views
8. Admin interface customization

This project gives you a solid foundation. You can extend it by adding:
- User profiles
- Task categories
- Due dates and reminders
- Search functionality
- API endpoints

Would you like me to explain any part in more detail or add any specific feature to this project?