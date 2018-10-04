from django.contrib.messages import get_messages
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
import requests
import json
from survey.forms import *
from survey.models import *
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.urls import reverse
from django.http import JsonResponse
from django.db.models import Q

def dropListOptions(rp_id,lookup_id,l_list_active):
    options_list = GenLookupListView.objects.filter(rp_id=rp_id, lookup_id=lookup_id, l_list_active=1).order_by('seq_no')
    OPTIONS = []
    OPTIONS.append(('', _('Choice')))
    for y in options_list:
        OPTIONS.append((y.lookup_list_id, y.code + ' - ' + y.list_name))

    return OPTIONS


def add_family_member(request):
    if request.session.get('Is_auth'):
        # check members limit before allowing user add new member
        sample_id = request.session['sample_id']
        sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
        no_of_members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0)).count()
        if no_of_members == sample_obj.no_of_member:
            messages.warning(request, _('You have reached out your members limit, Please increase number of members before adding new.'))
            return HttpResponseRedirect(reverse('survey:home'))

        form = FamilyMemberFormStep1()
        #request.session['member_order_count'] = 1
        context = {'form_step1':form, 'fm_id': sample_id, 'action' : 'add'}
        CHOICES = dropListOptions(9,27,1)
        form.fields['place_birth'].widget = forms.Select(choices = CHOICES)
        form.fields['place_stay_previous'].widget = forms.Select(choices = CHOICES)

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
                family_member_Id = (sample_id * 1000) + int(memberNumber);
                obj.f_m_id = family_member_Id
                request.session['fm_id'] = family_member_Id
                obj.member_status = 1
                obj.member_delete_status = 1
                obj.insert_by = request.session.get('user_id')
                if obj.age < 3:
                    obj.member_status = 2

                obj.save()
                message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
                if "error" in type:
                    return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fm_id': obj.f_m_id}))
                if "warning" in type:
                    return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fm_id': obj.f_m_id}))
                messages.success(request, _('Saved'))

                # recount family members
                total_members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0)).count()
                if total_members:
                    request.session['member_order_count'] += 1

                return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fm_id': obj.f_m_id, 'action' : 'add'}))
    else:
        raise Http404
    if request.session.get('member_order_count') is None:
        request.session['member_order_count'] = 1
    #print(request.session.get('member_order_count'))
    return render(request, 'family-member-form-step1.html', context)

def edit_family_member(request, fm_id):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id)

        if sample_id == instance.sample_id:
            form = FamilyMemberFormStep1(instance = instance)
            age = instance.age
            #context = {'form_step1':form, 'serial_num' : instance.member_no }
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

            context = {'form_step1':form, 'mem_obj': instance, 'action': 'edit'}

            if request.method == 'POST':
                old_record=FcpFamilyMemberTab.objects.get(f_m_id=fm_id)
                form = FamilyMemberFormStep1(request.POST, instance = instance)

                if form.is_valid():
                    # post if he dismiss warning

                    if request.POST.get('post') == "post-after-warning":
                        print('after warning post')
                        obj = form.save(commit=False)
                        obj.save()
                        message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
                        if "error" in type:
                            return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fm_id': obj.f_m_id}))
                        else:
                            storage = get_messages(request)
                            for item in storage:
                                if item.tags == "warning":
                                    del item
                            obj.member_status = 1
                            if obj.age < 3:
                                obj.member_status = 2
                            obj.save()
                            messages.success(request, _('Saved !'))
                            return HttpResponseRedirect(reverse('survey:home'))
                    obj = form.save(commit = False)

                    if old_record.gender != obj.gender:
                        obj.member_status = 1
                        if obj.gender == '1600001' or obj.marital_status == '10600001' :
                            obj.males_count = None
                            obj.females_count = None

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

                    obj.nationality_txt = GenLookupListView.objects.get(rp_id=1,lookup_id=18,l_list_active=1,lookup_list_id=obj.nationality).list_name
                    obj.member_no = instance.member_no
                    obj.f_m_id = instance.f_m_id
                    obj.sample_id = instance.sample_id

                    if obj.nationality != '1800001':
                        obj.place_birth = None
                        obj.place_stay_previous = None
                        obj.place_stay = None

                    if obj.age < 3:
                        obj.member_status = 2
                    obj.save()
                    message, type = check_errors(request, 1, sample_id, str(obj.f_m_id))
                    if "error" in type:
                        return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fm_id': obj.f_m_id}))
                    if "warning" in type:
                        return HttpResponseRedirect(reverse('survey:edit-family-member', kwargs={'fm_id': obj.f_m_id}))
                    messages.success(request, _('Saved'))

                    return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fm_id': obj.f_m_id, 'action':'edit'}))
        else:
            raise Http404
    else:
        raise Http404
    return render(request, 'family-member-form-step1.html', context)


# def familyMembersList(request, fm_id):
#     members_list = FcpFamilyMemberTab.objects.filter(sample_id=fm_id).order_by('member_no')
#     paginator = Paginator(members_list, 25)
#     page = request.GET.get('page')
#     if page and members_list != "":
#         members_list = paginator.get_page(pag)
#     context = {'members_list': members_list}
#     return render(request, 'family-members-list.html', context)


def add_member_info(request, fm_id, action):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        instance=FcpFamilyMemberTab.objects.get(f_m_id=fm_id)
        #context = {'fm_id': fm_id}
        #print('sdfds', instance.main_job)
        if sample_id == instance.sample_id:
            if instance.age < 3:
                messages.info(request, _('Your Form is Complete'))
                return HttpResponseRedirect(reverse('survey:home'))
            form = FamilyMemberFormStep2(instance = instance)

            if 'study_field' in form.fields:
                if instance.study_field:
                    edu_parent = GenLookupListView.objects.get(rp_id=9,lookup_id=10,l_list_active=1, lookup_list_id=instance.study_field).ref_work_type_pk
                    edu_child_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=10,l_list_active=1, ref_work_type_pk=edu_parent).order_by('seq_no')
                    CHOICES = []
                    CHOICES.append(('', _('Choice')))
                    for x in edu_child_list:
                        CHOICES.append((x.lookup_list_id, x.code + ' - ' + x.list_name))
                    form.fields['study_field_parent'].initial = edu_parent
                    form.fields['study_field'].initial = instance.study_field
                    if CHOICES:
                        form.fields['study_field'].choices = CHOICES
                else:
                    form.fields['study_field'].choices = ""

            if instance.age >= 15:
                if 'main_job' in form.fields:
                    if instance.main_job:
                        mainjob_parent = GenLookupListView.objects.get(rp_id=9,lookup_id=23,l_list_active=1, lookup_list_id=instance.main_job).ref_work_type_pk
                        mainjob_child_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=23,l_list_active=1, ref_work_type_pk=mainjob_parent).order_by('seq_no')
                        CHOICESMAINJOB = []
                        CHOICESMAINJOB.append(('', _('Choice')))
                        for x in mainjob_child_list:
                            CHOICESMAINJOB.append((x.lookup_list_id, x.code + ' - ' + x.list_name))

                        form.fields['main_job_parent'].initial = mainjob_parent
                        form.fields['main_job'].initial = instance.main_job
                        if CHOICESMAINJOB:
                            form.fields['main_job'].choices = CHOICESMAINJOB
                    else:
                        form.fields['main_job'].choices = ""

                if 'economic_activity' in form.fields:
                    if instance.economic_activity:

                        economic_activity_parent = GenLookupListView.objects.get(rp_id=9,lookup_id=21,l_list_active=1, lookup_list_id=instance.economic_activity).ref_work_type_pk
                        economic_activity_child = GenLookupListView.objects.filter(rp_id=9,lookup_id=21,l_list_active=1, ref_work_type_pk=economic_activity_parent).order_by('seq_no')
                        CHOICESECOACT = []
                        CHOICESECOACT.append(('', _('Choice')))
                        for y in economic_activity_child:
                            CHOICESECOACT.append((y.lookup_list_id, y.code + ' - ' + y.list_name))

                        form.fields['economic_activity_parent'].initial = economic_activity_parent
                        form.fields['economic_activity'].initial = instance.economic_activity

                        if CHOICESECOACT:
                            form.fields['economic_activity'].choices = CHOICESECOACT
                    else:
                        form.fields['economic_activity'].choices = ""

            show_female_fields = False
            if instance.gender == 1600002:
                show_female_fields = True
            else:
                show_female_fields = False;

            # show fields per age limits.
            three_years_age_flag = False
            ten_years_age_flag = False
            greater_age_flag = False

            if instance.age >= 3 and instance.age < 10:
                three_years_age_flag = True
            elif instance.age >= 10 and instance.age < 15:
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
                        #print('after warning post')
                        obj = form.save(commit=False)
                        message, type = check_errors(request, 2, sample_id, str(obj.f_m_id))
                        if "error" in type:
                            return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fm_id': obj.f_m_id, 'action': 'edit'}))
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
                    message, type = check_errors(request, 2, sample_id, str(obj.f_m_id))
                    if "error" in type:
                        return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fm_id': obj.f_m_id, 'action': 'edit'}))
                    if "warning" in type:
                        return HttpResponseRedirect(reverse('survey:add-member-info', kwargs={'fm_id': obj.f_m_id, 'action': 'edit'}))
                    messages.success(request, _('Saved'))

                    # check members limit before allowing user add new member
                    sample_id = request.session['sample_id']
                    sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
                    no_of_members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0)).count()

                    if action == 'edit':
                        return HttpResponseRedirect(reverse('survey:home'))

                    elif no_of_members < sample_obj.no_of_member and action == 'add':
                        return HttpResponseRedirect(reverse('survey:add-family'))
                    else:
                        messages.success(request, _('All members added, Please add housing details.'))
                        return HttpResponseRedirect(reverse('survey:add-house'))

            context = {'fm_id': fm_id, 'form_step2': form, 'female_fields': show_female_fields,'three_years_age':three_years_age_flag, 'ten_years_age':ten_years_age_flag, 'greater_age':greater_age_flag}

        else:
            raise Http404

        return render(request, 'family-member-form-step2.html', context)
    else:
        raise Http404

def ajax_load_member_data(request):

    if request.session.get('Is_auth'):

        fid = request.GET.get('fid')
        dob = request.GET.get('dob')
        opid = request.GET.get('opid')
        response = requests.get('http://192.168.0.21:81/NIC_PROD/Service1.svc/GetHeadFamilyData?FatherID='+fid+'&DOB='+dob+'&OperatorID='+opid+'')
        data = response.json()
        for key, value in data.items():
            ddata = json.loads(value)
            nationality_code = NicNaionalityTab.objects.get(nic_code = ddata["Nationality"])
            ddata["Nationality"] = nationality_code.nat_lookup_list_id
            ddata['nationality_txt'] = nationality_code.nic_nationality_name
            if ddata['MaritalStatus'] == 2500001:
                ddata['MaritalStatus'] = 10600001
                ddata['MartialStatustext'] = 'لم يتزوج'

            elif ddata['MaritalStatus'] == 2500002:
                ddata['MaritalStatus'] = 10600002
                ddata['MartialStatustext'] = 'متزوج'

            elif ddata['MaritalStatus'] == 2500003:
                ddata['MaritalStatus'] = 10600003
                ddata['MartialStatustext'] = 'مطلق'

            elif ddata['MaritalStatus'] == 2500004:
                ddata['MaritalStatus'] = 10600004
                ddata['MartialStatustext'] = 'مطلق'

            elif ddata['MaritalStatus'] < 1:
                ddata['MaritalStatus'] = ''
                ddata['MartialStatustext'] = '---'
        data = ddata

    else:
        raise Http404
    return JsonResponse(data)

def ajax_load_members_data(request):

    if request.session.get('Is_auth'):

        fid = request.GET.get('fid')
        dob = request.GET.get('dob')
        opid = request.GET.get('opid')
        mid = request.GET.get('mid')
        response = requests.get('http://192.168.0.21:81/NIC_PROD/Service1.svc/GetCitizenDepData?FatherID='+fid+'&DOB='+dob+'&MotherID='+mid+'&OperatorID='+opid+'')
        data = response.json()

        for key, value in data.items():
            ddata = json.loads(value)
            for i, val in enumerate(ddata['Persons']):
                nationality_code = NicNaionalityTab.objects.get(nic_code = val["Nationality"])
                val["Nationality"] = nationality_code.nat_lookup_list_id

                if val['MaritalStatus'] == 2500001:
                    val['MaritalStatus'] = 10600001
                    val['MartialStatustext'] = 'لم يتزوج'

                elif val['MaritalStatus'] == 2500002:
                    val['MaritalStatus'] = 10600002
                    val['MartialStatustext'] = 'متزوج'

                elif val['MaritalStatus'] == 2500003:
                    val['MaritalStatus'] = 10600003
                    val['MartialStatustext'] = 'مطلق'

                elif val['MaritalStatus'] == 2500004:
                    val['MaritalStatus'] = 10600004
                    val['MartialStatustext'] = 'مطلق'

                elif val['MaritalStatus'] < 1:
                    val['MaritalStatus'] = ''
                    val['MartialStatustext'] = '---'

                ddata["Persons"][i] = val
                ddata["Persons"][i]['nationality_txt'] = nationality_code.nic_nationality_name
            data = ddata
        #print(data)
    else:
        raise Http404
    return JsonResponse(data)

def ajax_save_members_data(request):

    sample_id = request.session['sample_id']
    sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
    no_of_members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0)).count()
    if no_of_members == sample_obj.no_of_member:
        messages.warning(request, _('You have reached out your members limit, Please increase number of members before adding new.'))
        return HttpResponseRedirect(reverse('survey:home'))

    member_no = FcpFamilyMemberTab.objects.filter(sample_id=sample_id)
    if not member_no:
        memberNumber = str(1).zfill(2)
        member_sno = memberNumber
    else:
        # count and incrementing by 1 as member number
        member_num = member_no.count()+1
        memberNumber = str(member_num).zfill(2)
        member_sno = memberNumber

    family_member_Id = (sample_id * 1000) + int(memberNumber);
    nationality_code = request.GET.get('nationality_code')
    nationality_txt = request.GET.get('nationality_txt')
    fname = request.GET.get('fname')
    age = request.GET.get('age')
    year = request.GET.get('year')
    relationshiptype =  request.GET.get('relationshiptype')
    gender = request.GET.get('gender')
    maritalstatus = request.GET.get('maritalstatus')

    family_member = FcpFamilyMemberTab.objects.create(
        f_m_id = family_member_Id,
        member_no = member_sno,
        sample_id=sample_id,
        member_name_first=fname,
        age=age,
        birth_year=year,
        family_relation = relationshiptype,
        gender= gender,
        nationality=nationality_code,
        nationality_txt=nationality_txt
    )

    if family_member:
        data = {
            'success': _("Member is added "),
            'f_m_id': family_member_Id,
            'link_text': _('Review newly added members')
        }
    else:
        data = {
            'error': _("Member is could not be added, Something went wrong! ")
        }
    return JsonResponse(data)

def ajax_render_list_options(request):
    if request.session.get('Is_auth'):
        lookup_list_id = request.GET.get('lookup_list_id')
        lookup_id = request.GET.get('lookup_id')
        if lookup_list_id:
            options_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=lookup_id,l_list_active=1, ref_work_type_pk=lookup_list_id).order_by('seq_no')
        else:
            options_list = GenLookupListView.objects.filter(rp_id=9,lookup_id=lookup_id,l_list_active=1).order_by('seq_no')

        context = {'options': options_list}
    else:
        raise Http404
    return render(request, 'options-list.html', context)


def home(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        sample_obj= GenSampleTab.objects.get(sample_id= sample_id)
        family_obj = FcpFamilyTab.objects.get(sample_id=sample_id)
        members = FcpFamilyMemberTab.objects.filter(sample_id=sample_id).order_by('member_no')
        members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0)).order_by('member_no')
        members_enter_count = members.count()
        members_complete_count = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & Q(member_status=2) & ~Q(member_delete_status=0)).count()
        member_status = False
        if members_complete_count == sample_obj.no_of_member:
            member_status = True
        else:
            member_status = False

        death_list = FcpFamilyDeathTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0))
        family_status = True
        if sample_obj.family_status != 2:
            family_status = False
        context = {'members_count':sample_obj.no_of_member, 'members_enter_count':members_enter_count, 'member_status': member_status,
                   'family_status': family_status, 'sample_obj': sample_obj, 'family_obj': family_obj, 'members': members, 'death_list': death_list}
    else:
        raise Http404
    return render(request, 'home.html', context)


def login(request, token):
    from django.contrib.auth.models import User
    user_info = AuthUserTab.objects.filter(token_key= token)
    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member_pass = request.POST.get('member_pass')
        #print(member_id, member_pass)
        try:
            user_info = AuthUserTab.objects.get(token_key=token, id_number = member_id)
        except AuthUserTab.DoesNotExist:
            messages.error(request, _('invalid id or password'))
            return HttpResponseRedirect(reverse('survey:login', kwargs={'token': token}))
        if int(member_id) == int(user_info.id_number) and member_pass == user_info.password:
            request.session['Is_auth'] = True
            request.session['user_id'] = user_info.id_number
            request.session['sample_id'] = user_info.sample_id
            request.session['family_id'] = user_info.sample_id
            # get nationality
            family_sample = FcpFamilyTab.objects.get(sample_id = user_info.sample_id)
            request.session['nationality'] = family_sample.nationality
            # token in session
            request.session['token_key'] = token

            total_members = FcpFamilyMemberTab.objects.filter(Q(sample_id=user_info.sample_id) & ~Q(member_delete_status=0)).count()
            if total_members:
                request.session['member_order_count']  = total_members + 1
            else:
                request.session['member_order_count']  = 1
            # UserLog.objects.create(user_id=user_info.id_number, input_id = member_id, success=True)
            return HttpResponseRedirect(reverse('survey:welcome'))
        else:
            # UserLog.objects.create(user_id=user_info.id_number, input_id=member_id, success=False)
            messages.error(request, _('invalid id or password'))
    context = {}
    return render(request, 'login.html', context)

def logout_view(request, token):
    from django.contrib.auth import logout
    logout(request)
    return HttpResponseRedirect(reverse('survey:login', kwargs={'token': token}))

def welcome_page(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        sample_obj= GenSampleTab.objects.get(sample_id= sample_id)
        context = {'members_count': sample_obj.no_of_member, 'sample_id': sample_id}
        return render(request, 'welcome.html', context)
    else:
        raise Http404
def start_step(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        sample_obj= GenSampleTab.objects.get(sample_id= sample_id)
        context = {'members_count': sample_obj.no_of_member, 'sample_id': sample_id}
        return render(request, 'start-step.html', context)
    else:
        raise Http404

def add_house(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        instance = FcpFamilyTab.objects.get(sample=sample_id)
        sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
        if sample_obj.family_status == 2:
            messages.info(request, _('Your Form is Complete'))
            return HttpResponseRedirect(reverse('survey:home'))
        members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id)& Q(member_status= 2) & ~Q(member_delete_status=0)).count()
        # All members status is complete
        if members == sample_obj.no_of_member:
            form = AddHouse(instance=instance)
            if request.method == 'POST':
                form = AddHouse(request.POST, instance=instance)
                if form.is_valid():
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
                    messages.success(request, _('House added'))
                    sample_id = request.session.get('sample_id')
                    sample_obj = FcpFamilyTab.objects.get(sample_id=sample_id)
                    if sample_obj.death_status == 3400001:
                        return HttpResponseRedirect(reverse('survey:death-form'))
                    else:
                        return HttpResponseRedirect(reverse('survey:submit-form'))
        else:
            messages.warning(request, _('Cannot add house before complete members'))
            return HttpResponseRedirect(reverse('survey:home'))

    else:
        raise Http404
    context = {'form': form,}
    return render(request, 'add_house.html', context)


def death_form(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
        family_obj = FcpFamilyTab.objects.get(sample_id=sample_id)
        if family_obj.death_status == 3400001:
            if sample_obj.family_status == 2:
                messages.info(request, _('Your Form is Complete'))
                return HttpResponseRedirect(reverse('survey:home'))
            member_no = FcpFamilyDeathTab.objects.filter(sample_id=sample_id)
            if not member_no:
                member_no = 1
            else:
                # count and incrementing by 1 as family member number
                member_num = member_no.count() + 1
                #print(member_num)
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
                    obj.member_delete_status = 1
                    obj.insert_by = request.session.get('user_id')
                    obj.save()
                    message, type = check_errors(request, 4, sample_id, str(obj.f_m_id))
                    if "error" in type:
                        return HttpResponseRedirect(reverse('survey:death-form-edit', kwargs={'member_id': obj.f_m_id}))
                    if "warning" in type:
                        return HttpResponseRedirect(reverse('survey:death-form-edit', kwargs={'member_id': obj.f_m_id}))
                    obj.member_status = 2
                    obj.save()
                    messages.success(request, _('Saved !'))
                    return HttpResponseRedirect(reverse('survey:submit-form'))
            context = {'form': form}
        else:
            messages.info(request, _('No death status available for this family'))
            return HttpResponseRedirect(reverse('survey:home'))
    else:
        raise Http404
    return render(request, 'death_form.html', context)


def death_form_edit(request, member_id):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        sample_obj = GenSampleTab.objects.get(sample_id=sample_id)
        if sample_obj.family_status == 2:
            messages.info(request, _('Your Form is Complete'))
            return HttpResponseRedirect(reverse('survey:home'))
        instance = FcpFamilyDeathTab.objects.get(f_m_id = member_id)
        if instance.sample_id == sample_id:
            form = DeathForm(instance=instance)
            if request.method == 'POST':
                form = DeathForm(request.POST, instance=instance)
                if form.is_valid():
                    # check if he ignore warninig
                    if request.POST.get('post') == "post-after-warning":
                        print('after warning post')
                        obj = form.save(commit=False)
                        obj.save()
                        message, type = check_errors(request, 3, sample_id, None)
                        if "error" in type:
                            return HttpResponseRedirect(reverse('survey:death-form-edit', kwargs={'member_id': obj.f_m_id}))
                        else:
                            storage = get_messages(request)
                            for item in storage:
                                if item.tags == "warning":
                                    del item
                            obj.member_status = 2
                            obj.save()
                            messages.success(request, _('Saved !'))
                            return HttpResponseRedirect(reverse('survey:home'))
                    obj = form.save(commit=False)
                    obj.member_status = 1

                    form.save()
                    message, type = check_errors(request, 4, sample_id, str(obj.f_m_id))
                    if "error" in type:
                        return HttpResponseRedirect(reverse('survey:death-form-edit', kwargs={'member_id': obj.f_m_id}))
                    if "warning" in type:
                        return HttpResponseRedirect(reverse('survey:death-form-edit', kwargs={'member_id': obj.f_m_id}))
                    obj.member_status = 2
                    obj.save()
                    messages.success(request, _('Saved !'))
                    return HttpResponseRedirect(reverse('survey:home'))
        else:
            raise Http404
        context = {'form': form, 'member_obj': instance}
    else:
        raise Http404

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
            print(query)
            query_list.append(query)
        row = []
        try:
            cursor.execute(query)
            row = cursor.fetchone()
        except Exception:
            messages.error(request, _('Error database') + " " + error.error_code )
            break
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
    member_id = '59080002'
    message, error_type = check_errors(request, 1 , sample_id, member_id)

    context = {}
    return render(request, 'check_error.html', context)


def delete_member(request):
    member_id = request.GET.get('member_id', None)
    data_type = request.GET.get('data_type', None)
    if data_type == "member":
        member = FcpFamilyMemberTab.objects.get(f_m_id= member_id)
        member.member_delete_status = 0
        member.save()
        request.session['member_order_count']  -= 1
        messages.success(request, _("Member is deleted"))
    elif data_type == "Death":
        member = FcpFamilyDeathTab.objects.get(f_m_id= member_id)
        member.member_delete_status = 0
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
    members_number = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_delete_status=0)).count()
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

def submit_form(request):
    if request.session.get('Is_auth'):
        sample_id = request.session.get('sample_id')
        sample_obj = GenSampleTab.objects.get(sample_id= sample_id)
        family_obj = FcpFamilyTab.objects.get(sample_id=sample_id)
        members = FcpFamilyMemberTab.objects.filter(Q(sample_id=sample_id) & Q(member_status=2) & ~Q(member_delete_status=0))
        death = FcpFamilyDeathTab.objects.filter(Q(sample_id=sample_id) & ~Q(member_status=2) & ~Q(member_delete_status=0))
        members_enter_count = members.count()

        member_status = False
        if members_enter_count == sample_obj.no_of_member:
            member_status = True

        death_status = True
        if death:
            death_status = False

        family_status = True
        message, error_type = check_errors(request, 3, sample_id, None)
        if error_type:
            family_status = False

        form_complete = False
        if member_status and death_status and family_status:
            form_complete = True
        if request.method == 'POST':
            name = request.POST.get('s_name', None)
            email = request.POST.get('s_email', None)
            mobile = request.POST.get('s_mobile', None)
            if name is None:
                messages.error(request, 'برجاء إدخال الأسم')
                return HttpResponseRedirect(reverse('survey:submit-form'))
            if name is None:
                messages.error(request, 'برجاء إدخال رقم الجوال')
                return HttpResponseRedirect(reverse('survey:submit-form'))
            sample_obj.family_status = 2
            sample_obj.data_giver_name = name
            sample_obj.data_giver_phone = mobile
            if email:
                sample_obj.data_giver_email = email
            sample_obj.save()
            messages.success(request, 'تم الاعتماد')
            return HttpResponseRedirect(reverse('survey:home'))
            print(name, mobile, email)
        context = {'member_status': member_status, 'death_status': death_status, 'family_status': family_status, 'form_complete': form_complete}
    else:
        raise Http404
    return render(request, 'submit_form.html', context)
