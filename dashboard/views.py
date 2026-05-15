from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import json
import os

# === Model tanımı ===
class MedCPTClassifier(nn.Module):
    def __init__(self, encoder, num_labels):
        super().__init__()
        self.encoder = encoder
        self.classifier = nn.Sequential(
            nn.Linear(768, 512),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(512, num_labels)
        )

    def forward(self, input_ids, attention_mask):
        outputs = self.encoder(input_ids=input_ids, attention_mask=attention_mask)
        cls_embedding = outputs.last_hidden_state[:, 0, :]
        return self.classifier(cls_embedding)

# === Modeli bir kez yükle (sunucu başlarken) ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ML_DIR   = os.path.join(BASE_DIR, "ml_models")

with open(os.path.join(ML_DIR, "label_mapping.json")) as f:
    label_mapping = json.load(f)  # {"0": "dengue fever", ...}

NUM_LABELS = len(label_mapping)
DEVICE     = torch.device("cpu")

tokenizer = AutoTokenizer.from_pretrained("ncbi/MedCPT-Query-Encoder")
encoder   = AutoModel.from_pretrained("ncbi/MedCPT-Query-Encoder")
model     = MedCPTClassifier(encoder, NUM_LABELS)
model.load_state_dict(torch.load(
    os.path.join(ML_DIR, "global_model_weights.pt"),
    map_location=DEVICE
))
model.eval()

# === Tahmin fonksiyonu ===
def predict_disease(symptom_text, top_k=5):
    encoded = tokenizer(
        symptom_text,
        max_length=128,
        padding="max_length",
        truncation=True,
        return_tensors="pt"
    )
    with torch.no_grad():
        outputs = model(encoded["input_ids"], encoded["attention_mask"])
        probs   = torch.softmax(outputs, dim=1)[0]

    top_probs, top_indices = torch.topk(probs, top_k)

    results = []
    for prob, idx in zip(top_probs.tolist(), top_indices.tolist()):
        disease_name = label_mapping.get(str(idx), f"Unknown ({idx})")
        results.append({
            "disease": disease_name.title(),
            "probability": round(prob * 100, 1)
        })
    return results

# === API endpoint ===
@csrf_exempt
@login_required
def predict_view(request):
    if request.method == "POST":
        data    = json.loads(request.body)
        symptom = data.get("symptoms", "").strip()
        if not symptom:
            return JsonResponse({"error": "Symptom text is required."}, status=400)
        results = predict_disease(symptom)
        return JsonResponse({"predictions": results})
    return JsonResponse({"error": "POST request required."}, status=405)

# === Mevcut view'lar ===
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

@login_required
def index(request):
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