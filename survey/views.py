from django.shortcuts import render
from survey.forms import *
from survey.models import *

# Create your views here.
<<<<<<< HEAD
def FcpFamilyMemberTabFormStep1View(request):
    form = FcpFamilyMemberTabFormStep1
    queryset = GenLookupListView.objects.all()
    print(queryset)
    context = {'form_step1':form, 'queryset':queryset}
    return render(request, 'family-member-form-step1.html', context)
=======


def home(request):
    context = {}
    return render(request, 'home.html', context)
>>>>>>> 93e179f754681e6539346d1e260486800127cd81
