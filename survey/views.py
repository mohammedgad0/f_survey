from django.shortcuts import render
from survey.forms import *
from survey.models import *

# Create your views here.
def FcpFamilyMemberTabFormStep1View(request):
    form = FcpFamilyMemberTabFormStep1
    context = {'form_step1':form}
    return render(request, 'family-member-form-step1.html', context)

def home(request):
    context = {}
    return render(request, 'home.html', context)
