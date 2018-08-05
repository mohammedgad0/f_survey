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

    if instance.main_job:
        mainjob_parent = GenLookupListView.objects.get(rp_id=9,lookup_id=23,l_list_active=1, lookup_list_id=instance.main_job).ref_work_type_pk
        mainjob_child_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=23,l_list_active=1, ref_work_type_pk=mainjob_parent).order_by('seq_no')
    else:
        mainjob_child_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=23,l_list_active=1, ref_work_type_pk=1100001).order_by('seq_no')

    CHOICESMAINJOB = []
    for x in mainjob_child_list:
        CHOICESMAINJOB.append((x.lookup_list_id, x.code + ' - ' + x.list_name))

    if instance.economic_activity:
        economic_activity_parent = GenLookupListView.objects.get(rp_id=9,lookup_id=21,l_list_active=1, lookup_list_id=instance.economic_activity).ref_work_type_pk
        economic_activity_child = GenLookupListView.objects.filter(rp_id=9,lookup_id=21,l_list_active=1, ref_work_type_pk=economic_activity_parent).order_by('seq_no')
    else:
        economic_activity_child = GenLookupListView.objects.filter(rp_id=9,lookup_id=21,l_list_active=1, ref_work_type_pk=2000099).order_by('seq_no')


    CHOICESECOAct = []
    for y in economic_activity_child:
        CHOICESECOAct.append((y.lookup_list_id, y.code + ' - ' + y.list_name))

    try:
        if instance.f_m_id:
            form.fields['family_member_id'].initial = instance.f_m_id

        if instance.study_field:
            form.fields['study_field_parent'].initial = GenLookupListView.objects.get(rp_id=9,lookup_id=10,l_list_active=1, lookup_list_id=instance.study_field).ref_work_type_pk
            form.fields['study_field'].initial = instance.study_field

        form.fields['study_field'].choices = CHOICES


        if instance.main_job:
            form.fields['main_job_parent'].initial = GenLookupListView.objects.get(rp_id=9,lookup_id=23,l_list_active=1, lookup_list_id=instance.main_job).ref_work_type_pk
            form.fields['main_job'].choices = CHOICESMAINJOB

        if instance.economic_activity:
            form.fields['economic_activity_parent'].initial = GenLookupListView.objects.get(rp_id=9,lookup_id=21,l_list_active=1, lookup_list_id=instance.economic_activity).ref_work_type_pk
            form.fields['economic_activity'].choices = CHOICESECOAct
    except:
        pass

    if request.method == 'POST':
        form = FamilyMemberFormStep2(request.POST,instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id))
        if form.is_valid():
            form.save()

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
    context = {}
    return render(request, 'home.html', context)


def login(request, token):
    user_info = AuthUserTab.objects.get(token_key= token)
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member_pass = request.POST.get('member_pass')
        print(member_id , member_pass)
        if member_id == user_info.id_number and member_pass == user_info.password:
            request.session['Is_auth'] = True
            request.session['user_id'] = user_info.id_number
            request.session['sample_id'] = user_info.sample.sample_id
            # return HttpResponseRedirect(reverse('projects:user-request-list'))
        else:
            messages.error(request, _('invalid id or password'))
    context = {}
    return render(request, 'login.html', context)


def add_house(request):
    form = AddHouse()
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
