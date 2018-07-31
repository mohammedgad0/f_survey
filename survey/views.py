from django.shortcuts import render
from survey.forms import *
from survey.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
# Create your views here.
def add_family_member(request):
    form = FamilyMemberFormStep1
    context = {'form_step1':form}
    if request.method == 'POST':
        form = FamilyMemberFormStep1(request.POST)
        print("dfgdfg",type(request.POST['difficulty_1_degree']))
        if form.is_valid():
            obj = form.save(commit = False)

            # sample_id will get from session later on, static used now.
            member_no = FcpFamilyMemberTab.objects.filter(sample_id=2)

            if not member_no:
                obj.member_no = 1
            else:
                # count and incrementing by 1 as family member number
                member_num = member_no.count()+1
                obj.member_no = member_num

            # will get from session later on, static used now.
            obj.sample_id = 2

            # will get from session later on, random unique number for now.
            obj.f_m_id = member_no.count()+100
            obj.family_relation = int(request.POST['family_relation'])
            obj.gender = int(request.POST['gender'])
            obj.nationality = int(request.POST['nationality'])
            obj.nationality_txt = GenLookupListView.objects.get(rp_id=1,lookup_id=18,l_list_active=1,lookup_list_id=int(request.POST['nationality'])).list_name
            obj.save()
            messages.success(request, _('Member Added successfully.'))
        context = {'form_step1':form}

    return render(request, 'family-member-form-step1.html', context)


def home(request):
    context = {}
    return render(request, 'home.html', context)


def login(request):
    if request.method == 'POST':
        id = request.method.POST.get('memper_id')
        print(id)
    context = {}
    return render(request, 'login.html', context)


def add_house(request):
    form = AddHouse()
    context = {'form': form}
    return render(request, 'add_house.html', context)


def death_form(request):
    form = DeathForm()
    context = {'form': form}
    return render(request, 'death_form.html', context)
