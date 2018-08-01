from django.shortcuts import render
from survey.forms import *
from survey.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
# Create your views here.
def int_or_str(value):
    try:
        return int(value)
    except:
        return value

def add_family_member(request):
    form = FamilyMemberFormStep1
    context = {'form_step1':form}
    if request.method == 'POST':
        form = FamilyMemberFormStep1(request.POST)
        #print(type(request.POST['difficulty_1_degree']))
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

            if obj.difficulty_1_degree:
                obj.difficulty_1_degree = int(request.POST['difficulty_1_degree'])
            if obj.difficulty_2_degree:
                obj.difficulty_2_degree = int(request.POST['difficulty_2_degree'])
            if obj.difficulty_3_degree:
                obj.difficulty_3_degree = int(request.POST['difficulty_3_degree'])
            if obj.difficulty_4_degree:
                obj.difficulty_4_degree = int(request.POST['difficulty_4_degree'])
            if obj.difficulty_5_degree:
                obj.difficulty_5_degree = int(request.POST['difficulty_5_degree'])
            if obj.difficulty_6_degree:
                obj.difficulty_6_degree = int(request.POST['difficulty_6_degree'])
            if obj.difficulty_7_degree:
                obj.difficulty_7_degree = int(request.POST['difficulty_7_degree'])
            if obj.place_birth:
                obj.place_birth = int(request.POST['place_birth'])
            if obj.place_stay_previous:
                obj.place_stay_previous = int(request.POST['place_stay_previous'])
            if obj.place_stay:
                obj.place_stay = int(request.POST['place_stay'])
            obj.save()
            messages.success(request, _('Member Added successfully.'))
        context = {'form_step1':form}

    return render(request, 'family-member-form-step1.html', context)

def familyMembersList(request, fid):
    members_list = FcpFamilyMemberTab.objects.filter(sample_id=fid).order_by('member_no')
    paginator = Paginator(members_list, 25)
    page = request.GET.get('page')
    if page and members_list != "":
        members_list = paginator.get_page(pag)
    context = {'members_list': members_list}
    return render(request, 'family-members-list.html', context)

def add_member_info(request, fm_id):
    form = FamilyMemberFormStep2(instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id))
    form.fields['family_member_id'].initial = FcpFamilyMemberTab.objects.get(f_m_id=fm_id).f_m_id
    if request.method == 'POST':
        form = FamilyMemberFormStep2(request.POST,instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id))

    context = {'form_step2': form}
    return render(request, 'family-member-form-step2.html', context)

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
