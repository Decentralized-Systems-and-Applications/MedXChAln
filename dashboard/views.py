from django.shortcuts import render

def index(request):
    # Django automatically looks in the 'templates' folder, 
    # so we just give it the path AFTER that.
    return render(request, 'dashboard/index.html')

