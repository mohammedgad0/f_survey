from django import forms
from django.forms import ModelForm, Textarea, TextInput, DateField, ModelChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from survey.models import *
#from django.forms.models import modelformset_factor

class dropList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.code + '- ' + obj.list_name


class FamilyMemberFormStep1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FamilyMemberFormStep1, self).__init__(*args, **kwargs)
        self.fields['difficulty_1_degree'].empty_label = None
        self.fields['difficulty_2_degree'].empty_label = None
        self.fields['difficulty_3_degree'].empty_label = None
        self.fields['difficulty_4_degree'].empty_label = None
        self.fields['difficulty_5_degree'].empty_label = None
        self.fields['difficulty_6_degree'].empty_label = None
        self.fields['difficulty_7_degree'].empty_label = None
        #self.fields['difficulty_8'].initial = 1
        self.fields['family_relation'].empty_label = None
        self.fields['place_birth'].empty_label = None
        self.fields['place_stay_previous'].empty_label = None
        self.fields['place_stay'].empty_label = None
        self.fields['gender'].empty_label = None

    member_name_first = forms.CharField(max_length=254, required=True,widget=forms.TextInput({'class': 'form-control'}))
    member_name_second = forms.CharField(max_length=254, required=True,widget=forms.TextInput({'class': 'form-control'}))
    member_name_third = forms.CharField(max_length=254, required=True,widget=forms.TextInput({'class': 'form-control'}))
    id_number_member = forms.CharField(max_length=254, required=True,widget=forms.TextInput({'class': 'form-control'}))
    age = forms.CharField(max_length=254, required=True,widget=forms.TextInput({'class': 'form-control'}))
    #birth_month = forms.CharField(max_length=254,widget=forms.TextInput({'class': 'form-control'}))
    birth_year = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    family_relation = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=17,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    gender = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=16,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    nationality = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=18,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    difficulty_1 = forms.BooleanField(label='النظر', required=False,  widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    difficulty_1_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة', widget=forms.RadioSelect())
    difficulty_2 = forms.BooleanField(label='السمع', required=False,  widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    difficulty_2_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة', widget=forms.RadioSelect())
    difficulty_3 = forms.BooleanField(label='الحركة', required=False,  widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    difficulty_3_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة',widget=forms.RadioSelect())
    difficulty_4 = forms.BooleanField(label='التزكر', required=False,  widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    difficulty_4_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة', widget=forms.RadioSelect())
    difficulty_5 = forms.BooleanField(label='العناية الشخصية', required=False,  widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    difficulty_5_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة', widget=forms.RadioSelect())
    difficulty_6 = forms.BooleanField(label='التخاطب والتواصل', required=False,  widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    difficulty_6_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة', widget=forms.RadioSelect())
    difficulty_other = forms.BooleanField(required=False)
    difficulty_7_txt = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control require-one'}))
    difficulty_7_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=False, label='درجةالصعوبة', widget=forms.RadioSelect())
    difficulty_8 = forms.BooleanField(label='لايوجد', required=False, widget=forms.CheckboxInput(attrs={'class':'require-one'}))
    place_birth = dropList(queryset=GenLookupListView.objects.filter(rp_id=2,lookup_id=27,l_list_active=1),to_field_name="lookup_list_id",required=False, label='مكان الميلاد', widget=forms.Select(attrs={'class': 'chosen form-control'}))
    place_stay_previous = dropList(queryset=GenLookupListView.objects.filter(rp_id=2,lookup_id=27,l_list_active=1),to_field_name="lookup_list_id",required=False, label='مكان الاقامة السابق', widget=forms.Select(attrs={'class': 'chosen form-control'}))
    place_stay = dropList(queryset=GenLookupListView.objects.filter(rp_id=2,lookup_id=27,l_list_active=1),to_field_name="lookup_list_id",required=False, label='مكان الاقامة المعتاد', widget=forms.Select(attrs={'class': 'chosen form-control'}))

    class Meta:
        model = FcpFamilyMemberTab
        fields = [
            'member_name_first',
            'member_name_second',
            'member_name_third',
            'id_number_member',
            'family_relation',
            'gender',
            'age',
            #'birth_month',
            'birth_year',
            'nationality',
            'difficulty_1',
            'difficulty_1_degree',
            'difficulty_2',
            'difficulty_2_degree',
            'difficulty_3',
            'difficulty_3_degree',
            'difficulty_4',
            'difficulty_4_degree',
            'difficulty_5',
            'difficulty_5_degree',
            'difficulty_6',
            'difficulty_6_degree',
            'difficulty_other',
            'difficulty_7_txt',
            'difficulty_7_degree',
            'difficulty_8',
            'place_birth',
            'place_stay_previous',
            'place_stay',
            ]


internet_connection =(
    ('', _('Choice')),
    ('1', _('Connect')),
    ('2', _('Disconnect')),

)


class AddHouse(forms.ModelForm):

    internet_connection = forms.ChoiceField(choices=internet_connection, label=_('Internet connection'))

    class Meta:
        model = FcpFamilyTab
        fields = ('housing_type','housing_type_txt', 'building_material', 'building_material_txt', 'housing_space', 'housing_stay_type','housing_stay_type_txt',
                  'bed_room_count', 'other_room_count', 'kitchen_count', 'bath_room_count', 'holding_type', 'holding_type_txt', 'electric_sources', 'electric_sources_txt',
                  'water_sources', 'water_sources_txt', 'sewage', 'sewage_txt', 'mobile_count', 'telephone_count', 'internet_users_count', 'internet_connection',
                  'car_count', 'tv_count', 'income_avg', 'housing_act_economic', 'death_status')

        widgets = {
            'housing_type_txt': TextInput(attrs={'type': 'text'}),
            'building_material_txt': TextInput(attrs={'type': 'text'}),
            'holding_type_txt': TextInput(attrs={'type': 'text'}),
            'electric_sources_txt': TextInput(attrs={'type': 'text'}),
            'water_sources_txt': TextInput(attrs={'type': 'text'}),
            'sewage_txt': TextInput(attrs={'type': 'text'}),
            'housing_space': TextInput(attrs={'required': True, 'type': 'number', 'min': 0}),
            'bed_room_count': TextInput(attrs={'required': True, 'type': 'number','min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value=' ');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'other_room_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'kitchen_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'bath_room_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'mobile_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'telephone_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'internet_users_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'car_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
            'tv_count': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==2) return false;'}),
        }

        labels = {
            'building_material_txt': _('building material text'),
            'housing_type_txt': _('Housing Type text'),
            'holding_type_txt': _('holding type txt'),
            'electric_sources_txt': _('electric sources txt'),
            'water_sources_txt': _('water sources txt'),
            'sewage_txt': _('sewage txt'),
            'housing_space': _('Housing space'),
            'internet_connection': _('Internet connection'),
            'mobile_count': _('Mobile Count'),
            'telephone_count': _('Telephone Count'),
            'internet_users_count': _('Internet users count'),
            'car_count': _('Car count'),
            'tv_count': _('Tv count'),
            'bed_room_count': _('Bed count'),
            'other_room_count': _('other count'),
            'kitchen_count': _('kitchen count'),
            'bath_room_count': _('bath count'),
        }

        help_texts = {
            'housing_space': 'يتم تدوين إجمالي مساحة مسطحات البناء للمسكن(بالمتر المربع)'
        }

    def __init__(self, *args, **kwargs):
        empty = _('Choice')
        super(AddHouse, self).__init__(*args, **kwargs)
        self.fields['housing_type'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=104, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Housing type'), empty_label=empty)
        self.fields['building_material'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=9, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Building material'), empty_label=empty)
        self.fields['housing_stay_type'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=175, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Housing stay type'), empty_label=empty)
        self.fields['holding_type'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=13, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Holding type'), empty_label=empty)
        self.fields['electric_sources'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=100, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Electric source'), empty_label=empty)
        self.fields['water_sources'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=14, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Water source'), empty_label=empty)
        self.fields['sewage'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=102, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Sewage source'), empty_label=empty)
        self.fields['income_avg'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=176, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('Income avg'), empty_label=empty)
        self.fields['housing_act_economic'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=34, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label= _('Housing act economic'), empty_label=empty)


class DeathForm(forms.ModelForm):

    class Meta:
        model = FcpFamilyDeathTab
        fields = ('member_name', 'gender', 'nationality', 'death_age', 'reason_death', 'reason_death_txt')

        labels = {
            'member_name': _('Name'),
            'death_age': _('death age'),
            'reason_death_txt': _('reason death text')

        }
        widgets = {
            'member_name': TextInput(attrs={'type': 'text', 'required': True}),
            'death_age': TextInput(attrs={'required': True, 'type': 'number', 'min': 0, 'step': 1, 'pattern': "\d*", 'oninput': "validity.valid||(value='');", 'onKeyPress': 'if(this.value.length==3) return false;'}),
        }

    def __init__(self, *args, **kwargs):
        empty = _('Choice')
        super(DeathForm, self).__init__(*args, **kwargs)
        self.fields['gender'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=16, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('gender'), empty_label=empty)
        self.fields['nationality'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=159, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('nationality'), empty_label=empty)
        self.fields['reason_death'] = dropList(queryset=GenLookupListView.objects.filter(rp_id=9, lookup_id=107, l_list_active=1).order_by('seq_no'), to_field_name="lookup_list_id", label=_('reason death'), empty_label=empty)

