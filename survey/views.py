from django.shortcuts import render
from survey.forms import *
from survey.models import *
from django.contrib import messages
# Create your views here.
def add_family_member(request):
    form = FamilyMemberFormStep1
    if request.method == 'POST':
        form = FamilyMemberFormStep1(request.POST)

        if form.is_valid():
            print(request.POST)
            form.save()
            messages.success(request, _('Member Added successfully.'))
            context = {'form': form}

    context = {'form_step1':form}
    return render(request, 'family-member-form-step1.html', context)


def home(request):
    context = {}
    return render(request, 'home.html', context)


def add_house(request):
    form = AddHouse()
    context = {'form':form}
    return render(request, 'add_house.html', context)


def death_form(request):
    form = DeathForm()
    context = {'form': form}
    return render(request, 'death_form.html', context)