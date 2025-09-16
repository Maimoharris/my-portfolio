from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Skill, Service, Project, Profile, Contact
from .forms import ContactForm

def home(request):
    profile = Profile.objects.filter(is_active=True).first()
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    skills = Skill.objects.all()
    services = Service.objects.filter(is_active=True)[:3]
    
    context = {
        'profile': profile,
        'featured_projects': featured_projects,
        'skills': skills,
        'services': services,
    }
    return render(request, 'portfolio/home.html', context)

def about(request):
    profile = Profile.objects.filter(is_active=True).first()
    skills = Skill.objects.all()
    
    context = {
        'profile': profile,
        'skills': skills,
    }
    return render(request, 'portfolio/about.html', context)

def services(request):
    services = Service.objects.filter(is_active=True)
    
    context = {
        'services': services,
    }
    return render(request, 'portfolio/services.html', context)

def projects(request):
    category = request.GET.get('category', 'all')
    
    if category == 'all':
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(category=category)
    
    categories = Project.CATEGORY_CHOICES
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category,
    }
    return render(request, 'portfolio/projects.html', context)

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    related_projects = Project.objects.filter(category=project.category).exclude(pk=pk)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save()
            
            # Send email notification (optional)
            try:
                send_mail(
                    subject=f"New Contact Form Message: {contact.subject}",
                    message=f"From: {contact.name} ({contact.email})\n\n{contact.message}",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except:
                pass
            
            messages.success(request, 'Thank you for your message! I will get back to you soon.')
            return redirect('portfolio:contact')
    else:
        form = ContactForm()
    
    profile = Profile.objects.filter(is_active=True).first()
    
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'portfolio/contact.html', context)
