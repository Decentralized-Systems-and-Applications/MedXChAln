from django.shortcuts import render

def index(request):
    return render(request, 'dashboard/Overview.html')

def diagnosis_view(request):
    return render(request, 'dashboard/diagnosis_support.html')

def anamnesis_view(request):
    return render(request, 'dashboard/Anamnesis_Record.html')

def model_mgmt_view(request):
    return render(request, 'dashboard/Model_Management.html')

def hospital_mgmt_view(request):
    return render(request, 'dashboard/Hospital_Management.html')

def security_traceability_view(request):
    return render(request, 'dashboard/Security_Traceability.html')