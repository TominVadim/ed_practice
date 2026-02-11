from django.shortcuts import render, redirect
from .forms import ServiceForm, PetForm
from .models import Service, Pet

def pet_list(request):
    return render(request, 
                  'pets.html',
                  {'pets': Pet.objects.all()})

def create_service(request):
    if request == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('pet_list')
    else:
        form = ServiceForm()
    
    return render(request, 'service.html', {"form": form})