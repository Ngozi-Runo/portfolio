from django.shortcuts import render

def home(request):
    """Home page view"""
    context = {
        'name': 'Moses Otiti',
        'title': 'Cloud Engineer',
        'about': 'I am a passionate Cloud Engineer with Experience in AWS Cloud computing, Linux Administration and Python Programming.',
        'skills': [
            'Python', 'Django', 'JavaScript', 'React', 'AWS', 'Docker', 'PostgreSQL', 'Git'
        ],
        'projects': [
            {
                'title': 'E-commerce Platform',
                'description': 'A full-featured e-commerce platform built with Django and React.',
                'technologies': ['Django', 'React', 'PostgreSQL', 'AWS'],
                'github_url': 'https://github.com/yourusername/ecommerce-platform',
                'live_url': 'https://your-ecommerce-site.com',
                'image': 'images/projects/ecommerce-platform.jpg'
            },
            {
                'title': 'Task Management App',
                'description': 'A collaborative task management application with real-time updates.',
                'technologies': ['Django', 'WebSockets', 'Redis', 'Bootstrap'],
                'github_url': 'https://github.com/yourusername/task-manager',
                'live_url': 'https://your-task-app.com',
                'image': 'images/projects/task-management.jpg'
            },
            {
                'title': 'Weather Dashboard',
                'description': 'A responsive weather dashboard with location-based forecasts.',
                'technologies': ['JavaScript', 'API Integration', 'Chart.js', 'CSS3'],
                'github_url': 'https://github.com/yourusername/weather-dashboard',
                'live_url': 'https://your-weather-app.com',
                'image': 'images/projects/weather-app.jpg'
            }
        ],
        'contact': {
            'email': 'otitimoses@gmail.com',
            'linkedin': 'https://www.linkedin.com/in/moses-otiti-b4a94978',
            'github': 'https://github.com/yourusername',
            'phone': '+2348032937786'
        }
    }
    return render(request, 'main/home.html', context)

def about(request):
    """About page view"""
    return render(request, 'main/about.html')

def projects(request):
    """Projects page view"""
    return render(request, 'main/projects.html')

def contact(request):
    """Contact page view"""
    return render(request, 'main/contact.html')
