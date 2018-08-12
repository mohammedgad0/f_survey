from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from survey.forms import *
from survey.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q
# Create your views here.


def int_or_str(value):
    try:
        return int(value)
    except:
        return value

def dropListOptions(rp_id,lookup_id,l_list_active):
    options_list = GenLookupListView.objects.filter(rp_id=rp_id, lookup_id=lookup_id, l_list_active=1).order_by('seq_no')
    OPTIONS = []
    for y in options_list:
        OPTIONS.append((y.lookup_list_id, y.code + ' - ' + y.list_name))

    return OPTIONS

def add_family_member(request):
    form = FamilyMemberFormStep1()
    context = {'form_step1':form}
    CHOICES = dropListOptions(9,27,1)
    form.fields['place_birth'].widget = forms.Select(choices = CHOICES)
    form.fields['place_stay_previous'].widget = forms.Select(choices = CHOICES)
    #form.fields['member_status'].initial = 1
    sample_id = request.session['sample_id']
    if request.method == 'POST':
        form = FamilyMemberFormStep1(request.POST)
        #print(type(request.POST['difficulty_1_degree']))
        if form.is_valid():
            obj = form.save(commit=False)
            member_no = FcpFamilyMemberTab.objects.filter(sample_id=sample_id)
            if not member_no:
                memberNumber = str(1).zfill(2)
                obj.member_no = memberNumber
            else:
                # count and incrementing by 1 as member number
                member_num = member_no.count()+1
                memberNumber = str(member_num).zfill(2)
                obj.member_no = memberNumber

            obj.sample_id = sample_id
            # will get from session later on, random unique number for now.
            family_member_Id = (sample_id * 1000) + int(memberNumber);
            obj.f_m_id = family_member_Id
            obj.member_status = 1
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

            message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
            if "error" in type:
                return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fid': obj.f_m_id}))
            if "warning" in type:
                return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fid': obj.f_m_id}))

        return HttpResponseRedirect(reverse('survey:home'))
    return render(request, 'family-member-form-step1.html', context)

def edit_family_member(request, fid):
    sample_id = request.session.get('sample_id')
    instance=FcpFamilyMemberTab.objects.get(f_m_id=fid)
    form = FamilyMemberFormStep1(instance = instance)
    age = instance.age
    context = {'form_step1':form}
    if instance.difficulty_7_txt:
        form.fields['difficulty_other'].initial = 1

    if instance.place_birth:
        if instance.place_birth >= 2700001 and instance.place_birth <= 2700013:
            CHOICES = dropListOptions(9,27,1)
            form.fields['in_or_out_birth'].initial = 1
        else:
            CHOICES = dropListOptions(9,18,1)
            form.fields['in_or_out_birth'].initial = 2
    else:
        CHOICES = dropListOptions(9,27,1)

    form.fields['place_birth'].widget = forms.Select(choices = CHOICES)
    form.fields['place_birth'].initial = instance.place_birth

    if instance.place_stay_previous:
        if instance.place_stay_previous >= 2700001 and instance.place_stay_previous <= 2700013:
            CHOICES = dropListOptions(9,27,1)
            form.fields['in_or_out_prev_stay'].initial = 1
        else:
            CHOICES = dropListOptions(9,18,1)
            form.fields['in_or_out_prev_stay'].initial = 2
    else:
        CHOICES = dropListOptions(9,27,1)

    form.fields['place_stay_previous'].widget = forms.Select(choices = CHOICES)
    form.fields['place_stay_previous'].initial = instance.place_stay_previous

    context = {'form_step1':form, 'mem_obj': instance}
    if request.method == 'POST':
        old_record=FcpFamilyMemberTab.objects.get(f_m_id=fid)
        form = FamilyMemberFormStep1(request.POST, instance = instance)

        if form.is_valid():
            # post if he dismiss warning
            if request.POST.get('post') == "post-after-warning":
                print('after warning post')
                obj = form.save(commit=False)
                message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
                if "error" in type:
                    return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fid': obj.f_m_id}))
                else:
                    storage = get_messages(request)
                    for item in storage:
                        if item.tags == "warning":
                            del item
                    messages.success(request, _('Saved !'))
                    return HttpResponseRedirect(reverse('survey:home'))
            obj = form.save(commit = False)
            if old_record.age != obj.age:
                obj.member_status = 1
                if obj.age >= 3 and obj.age < 10:
                    obj.study_status = None
                    obj.education_status = None
                    obj.study_field = None
                    obj.marital_status = None
                    obj.males_count = None
                    obj.females_count = None
                    obj.labor_status = None
                    obj.labor_status_txt = None
                    obj.main_job = None
                    obj.economic_activity_parent = None
                    obj.economic_activity = None
                    obj.work_sector_type = None
                    obj.work_sector_type_txt = None
                    obj.member_status = 1
                elif obj.age >= 10 and obj.age < 15:
                    obj.education_status = None
                    obj.study_field = None
                    obj.marital_status = None
                    obj.males_count = None
                    obj.females_count = None
                    obj.labor_status = None
                    obj.labor_status_txt = None
                    obj.main_job = None
                    obj.economic_activity_parent = None
                    obj.economic_activity = None
                    obj.work_sector_type = None
                    obj.work_sector_type_txt = None
                    obj.member_status = 1
            obj.gender = int(request.POST['gender'])
            obj.nationality = int(request.POST['nationality'])
            obj.nationality_txt = GenLookupListView.objects.get(rp_id=1,lookup_id=18,l_list_active=1,lookup_list_id=int(request.POST['nationality'])).list_name
            obj.member_no = instance.member_no
            obj.f_m_id = instance.f_m_id
            obj.sample_id = instance.sample_id
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

            obj.save()
            message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
            if "error" in type:
                return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fid': obj.f_m_id}))
            if "warning" in type:
                return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fid': obj.f_m_id}))
        return HttpResponseRedirect(reverse('survey:home'))
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
    sample_id = request.session.get('sample_id')
    instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id)
    form = FamilyMemberFormStep2(instance = instance)
    #form.fields['member_status'].initial = 2
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
    show_female_fields = False
    if instance.gender == 1600002:
        show_female_fields = True
    else:
        show_female_fields = False;

    # show fields per age limits.
    three_years_age_flag = False
    ten_years_age_flag = False
    greater_age_flag = False

    if instance.age >= 3 and instance.age <= 10:

        three_years_age_flag = True
    elif instance.age >= 10 and instance.age <= 15:
        three_years_age_flag = True
        ten_years_age_flag = True
    else:
        three_years_age_flag = True
        ten_years_age_flag = True
        greater_age_flag = True

    if request.method == 'POST':
        form = FamilyMemberFormStep2(request.POST,instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id))
        if form.is_valid():
            # post if he dismiss warning
            if request.POST.get('post') == "post-after-warning":
                print('after warning post')
                obj = form.save(commit=False)
                message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
                if "error" in type:
                    return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fid': obj.f_m_id}))
                else:
                    storage = get_messages(request)
                    for item in storage:
                        if item.tags == "warning":
                            del item
                    messages.success(request, _('Saved !'))
                    return HttpResponseRedirect(reverse('survey:home'))
            obj = form.save(commit = False)
            obj.member_status = 2
            obj.save()
            message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
            if "error" in type:
                return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fid': obj.f_m_id}))
            if "warning" in type:
                return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fid': obj.f_m_id}))
            return HttpResponseRedirect(reverse('survey:home'))

    context = {'form_step2': form, 'female_fields': show_female_fields,'three_years_age':three_years_age_flag, 'ten_years_age':ten_years_age_flag, 'greater_age':greater_age_flag}
    return render(request, 'family-member-form-step2.html', context)

def ajax_render_list_options(request):
    lookup_list_id = request.GET.get('lookup_list_id')
    lookup_id = request.GET.get('lookup_id')
    if lookup_list_id:
        options_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=lookup_id,l_list_active=1, ref_work_type_pk=lookup_list_id).order_by('seq_no')
    else:
        options_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=lookup_id,l_list_active=1).order_by('seq_no')

    context = {'options': options_list}
    return render(request, 'options-list.html', context)


def home(request):
    sample_id = request.session.get('sample_id')
    sample_obj= GenSampleTab.objects.get(sample_id= sample_id)
    family_obj = FcpFamilyTab.objects.get(sample_id=sample_id)
    members = FcpFamilyMemberTab.objects.filter(sample_id=sample_id).order_by('member_no')
    members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=1))
    members_enter_count = members.count()
    members_complete_count = FcpFamilyMemberTab.objects.filter(sample_id=sample_id, member_status= 2).count()
    member_status = False
    if members_complete_count == sample_obj.no_of_member:
        member_status = True
    else:
        member_status = False

    death_list = FcpFamilyDeathTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=1))
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
            request.session['family_id'] = user_info.sample_id
            # UserLog.objects.create(user_id=user_info.id_number, input_id = member_id, success=True)
            return HttpResponseRedirect(reverse('survey:home'))
        else:
            # UserLog.objects.create(user_id=user_info.id_number, input_id=member_id, success=False)
            messages.error(request, _('invalid id or password'))
    context = {}
    return render(request, 'login.html', context)


def add_house(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        instance = FcpFamilyTab.objects.get(sample=sample_id)
        form = AddHouse(instance=instance)
        if request.method == 'POST':
            form = AddHouse(request.POST, instance=instance)
            if form.is_valid():
                print("form valid")
                # check if he ignore warninig
                if request.POST.get('post') == "post-after-warning":
                    print('after warning post')
                    obj = form.save(commit=False)
                    obj.save()
                    message, type = check_errors(request, 3, sample_id, None)
                    if "error" in type:
                        return HttpResponseRedirect(reverse('survey:add-house'))
                    else:
                        storage = get_messages(request)
                        for item in storage:
                            if item.tags == "warning":
                                del item
                        messages.success(request, _('Saved !'))
                        return HttpResponseRedirect(reverse('survey:home'))

                obj = form.save(commit=False)
                obj.insert_by = request.session.get('user_id')
                obj.save()
                message, type = check_errors(request, 3, sample_id, None)
                if "error" in type:
                    return HttpResponseRedirect(reverse('survey:add-house'))
                if "warning" in type:
                    return HttpResponseRedirect(reverse('survey:add-house'))
                # return HttpResponseRedirect(reverse('survey:add-house'))

                return HttpResponseRedirect(reverse('survey:add-house'))
    else:
        raise Http404
    context = {'form': form,}
    return render(request, 'add_house.html', context)


def death_form(request):
    sample_id = request.session.get('sample_id')
    member_no = FcpFamilyDeathTab.objects.filter(sample_id=sample_id)
    if not member_no:
        member_no = 1
    else:
        # count and incrementing by 1 as family member number
        member_num = member_no.count() + 1
        print(member_num)
        member_no = member_num
    form = DeathForm()
    if request.method == 'POST':
        form = DeathForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.f_m_id = int(sample_id) * 1000 + int(member_no)
            obj.sample_id = sample_id
            obj.member_no = member_no
            obj.member_status = 1
            print(obj.f_m_id)
            form.save()
            messages.success(request, _('Saved !'))
            return HttpResponseRedirect(reverse('survey:home'))
    context = {'form': form}
    return render(request, 'death_form.html', context)


def death_form_edit(request, member_id):
    instance = FcpFamilyDeathTab.objects.get(f_m_id = member_id)
    form = DeathForm(instance=instance)
    if request.method == 'POST':
        form = DeathForm(request.POST, instance=instance)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.member_status = 1
            print(obj.f_m_id)
            form.save()
            messages.success(request, _('Saved !'))
            return HttpResponseRedirect(reverse('survey:home'))
    context = {'form': form}
    return render(request, 'death_form.html', context)


def check_errors(request, part_id, sample_id, member_id):
    from django.db import connection
    cursor = connection.cursor()
    errors_list = GenErrorTab.objects.filter(rp_id=9, part_web=part_id, on_off_desktop=1).order_by('error_sort')
    query_list = []
    error_type = []
    for error in errors_list:
        where = error.desktop_condition
        where = where.replace('P_SAMPLE_ID', str(sample_id))
        if member_id:
            where = where.replace('P_F_M_ID', member_id)
        if where:
            query = "SELECT * FROM " + error.table_name + " WHERE " + where
            query_list.append(query)
        cursor.execute(query)
        row = cursor.fetchone()
        if row:
            if error.error_type == 1:
                error_type.append('error')
                messages.error(request, error.error_code + " " + error.message)
                break
            elif error.error_type == 2:
                error_type.append("warning")
                messages.warning(request, error.error_code + " " + error.message)
    return messages, set(error_type)


def check_error(request):
    sample_id = request.session.get('sample_id')
    member_id = "6"
    message, error_type = check_errors(request, sample_id, member_id)
    print(error_type)
    context = {}
    return render(request, 'check_error.html', context)


def delete_member(request):
    member_id = request.GET.get('member_id', None)
    data_type = request.GET.get('data_type', None)
    if data_type == "member":
        member = FcpFamilyMemberTab.objects.get(f_m_id= member_id)
        member.member_delete_status = 1
        member.save()
        messages.success(request, _("Member is deleted"))
    elif data_type == "Death":
        member = FcpFamilyDeathTab.objects.get(f_m_id= member_id)
        member.member_delete_status = 1
        member.save()
        messages.success(request, _("Member is deleted"))
    data = {
        'is_deleted': "Member is deleted "
    }
    return JsonResponse(data)


def change_number(request):
    string = None
    data = {}
    sample_id = request.GET.get('sample_id', None)
    new_value = request.GET.get('new_value', None)
    sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
    members_number = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=1)).count()
    if int(members_number) > int(new_value):
        string = _('value less than members already exists')
        data = {
            'messages': string,
            'type': 0
        }
    else:
        sample_obj.no_of_member = new_value
        sample_obj.save()
        string = _('change done')
        data = {
            'messages': string,
            'type': 1
        }

    return JsonResponse(data)

