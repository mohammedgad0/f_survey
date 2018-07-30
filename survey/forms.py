from django import forms
from django.forms import ModelForm, Textarea, TextInput, DateField, ModelChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from survey.models import *
#from django.forms.models import modelformset_factor
class dropList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.list_name

class FcpFamilyMemberTabFormStep1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FcpFamilyMemberTabFormStep1, self).__init__(*args, **kwargs)
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

    member_name_first = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    member_name_second = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    member_name_third = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    id_number_member = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    age = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    #birth_month = forms.CharField(max_length=254,widget=forms.TextInput({'class': 'form-control'}))
    birth_year = forms.CharField(max_length=254, required=False,widget=forms.TextInput({'class': 'form-control'}))
    family_relation = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=17,l_list_active=1),to_field_name="lookup_list_id",required=False,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    gender = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=16,l_list_active=1),to_field_name="lookup_list_id",required=False,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    nationality = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=18,l_list_active=1),to_field_name="lookup_list_id",required=False,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
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
