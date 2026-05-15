from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('diagnosis-support/', views.diagnosis_view, name='diagnosis_support'),
    path('diagnosis/predict/', views.predict_view, name='predict'),    
    path('anamnesis-record/', views.anamnesis_view, name='anamnesis_record'),
    path('model-management/', views.model_mgmt_view, name='model_management'),
    path('hospital-management/', views.hospital_mgmt_view, name='hospital_management'),
    path('security-traceability/', views.security_traceability_view, name='security_traceability'),
    path('accounts/signup/', views.signup_view, name='register'),
]