from django.http import HttpResponseRedirect
from django.shortcuts import render
from survey.forms import *
from survey.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.http import JsonResponse
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
            #obj.family_relation = int(request.POST['family_relation'])
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
    instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id)
    form = FamilyMemberFormStep2(instance = instance)
    # temp field
    #print(instance.study_field)
    if instance.study_field:
        edu_parent = GenLookupListView.objects.get(rp_id=9,lookup_id=10,l_list_active=1, lookup_list_id=instance.study_field).ref_work_type_pk
        edu_child_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=10,l_list_active=1, ref_work_type_pk=edu_parent).order_by('seq_no')
    else:
        edu_child_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=10,l_list_active=1, ref_work_type_pk=1100001).order_by('seq_no')

    CHOICES = []
    for x in edu_child_list:
        CHOICES.append((x.lookup_list_id, x.code + ' - ' + x.list_name))
    try:
        if instance.f_m_id:
            form.fields['family_member_id'].initial = instance.f_m_id
        if instance.study_field:
            form.fields['study_field_parent'].initial = GenLookupListView.objects.get(rp_id=9,lookup_id=10,l_list_active=1, lookup_list_id=instance.study_field).ref_work_type_pk
            form.fields['study_field'].initial = instance.study_field
        form.fields['study_field'].choices = CHOICES
        print(instance.marital_status)
        #form.feilds['marital_status'].initial = GenLookupListView.objects.get(rp_id=9,lookup_id=10,l_list_active=1, lookup_list_id=instance.marital_status).lookup_list_id
    except:
        pass

    if request.method == 'POST':
        form = FamilyMemberFormStep2(request.POST,instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id))
        if form.is_valid():
            obj = form.save(commit=False)
            print(int(obj.marital_status))
            obj.save()

    show_female_fields = False
    if instance.gender == 1600002:
        show_female_fields = True
    else:
        show_female_fields = False;

    context = {'form_step2': form, 'female_fields': show_female_fields}
    return render(request, 'family-member-form-step2.html', context)

def ajax_render_list_options(request):
    lookup_list_id = request.GET.get('lookup_list_id')
    lookup_id = request.GET.get('lookup_id')
    options_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=lookup_id,l_list_active=1, ref_work_type_pk=lookup_list_id).order_by('seq_no')
    context = {'options': options_list}
    return render(request, 'options-list.html', context)


def home(request):
    sample_id = request.session.get('sample_id')
    sample_obj= GenSampleTab.objects.get(sample_id= sample_id)
    family_obj = FcpFamilyTab.objects.get(sample_id=sample_id)
    members = FcpFamilyMemberTab.objects.filter(sample_id=sample_id)
    members_enter_count = members.count()
    members_complete_count = FcpFamilyMemberTab.objects.filter(sample_id=sample_id, member_status= 2).count()
    member_status = False
    if members_complete_count == sample_obj.no_of_member:
        member_status = True
    else:
        member_status = False
    death_list = FcpFamilyDeathTab.objects.filter(sample_id=sample_id)

    context = {'members_count':sample_obj.no_of_member, 'members_enter_count':members_enter_count, 'member_status': member_status,
               'family_status': sample_obj.family_status, 'sample_obj': sample_obj, 'family_obj': family_obj, 'members': members, 'death_list': death_list}
    return render(request, 'home.html', context)


def login(request, token):
    user_info = AuthUserTab.objects.filter(token_key= token)

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member_pass = request.POST.get('member_pass')
        print(member_id, member_pass)
        user_info = AuthUserTab.objects.get(token_key=token, id_number = member_id)
        if int(member_id) == int(user_info.id_number) and member_pass == user_info.password:
            request.session['Is_auth'] = True
            request.session['user_id'] = user_info.id_number
            request.session['sample_id'] = user_info.sample_id
            UserLog.objects.create(user_id=user_info.id_number, input_id = member_id, success=True)
            return HttpResponseRedirect(reverse('survey:home'))
        else:
            UserLog.objects.create(user_id=user_info.id_number, input_id=member_id, success=False)
            messages.error(request, _('invalid id or password'))
    context = {}
    return render(request, 'login.html', context)


def add_house(request):
    instance = FcpFamilyTab.objects.get(sample=request.session.get('sample_id'))
    form = AddHouse(instance=instance)
    if request.method == 'POST':
        form = AddHouse(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.sample_id = request.session.get('sample_id')
            obj.insert_by = request.session.get('user_id')
            obj.save()
            messages.success(request, _('House Added successfully.'))
            return HttpResponseRedirect(reverse('survey:home'))

    context = {'form': form}
    return render(request, 'add_house.html', context)


def death_form(request):
    form = DeathForm()
    if request.method == 'POST':
        form = DeathForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.f_m_id = 2
            form.save()
    context = {'form': form}
    return render(request, 'death_form.html', context)
