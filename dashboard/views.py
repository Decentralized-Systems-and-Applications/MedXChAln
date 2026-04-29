from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # This is your Overview page
    return render(request, 'dashboard/Overview.html')

@login_required
def diagnosis_view(request):
    return render(request, 'dashboard/diagnosis_support.html')

@login_required
def anamnesis_view(request):
    return render(request, 'dashboard/Anamnesis_Record.html')

@login_required
def model_mgmt_view(request):
    return render(request, 'dashboard/Model_Management.html')

@login_required
def hospital_mgmt_view(request):
    return render(request, 'dashboard/Hospital_Management.html')

@login_required
def security_traceability_view(request):
    return render(request, 'dashboard/Security_Traceability.html')