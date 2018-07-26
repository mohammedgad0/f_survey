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

    member_name_first = forms.CharField(max_length=254,widget=forms.TextInput({'class': 'form-control'}))    
    family_relation = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=17,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    gender = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=16,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    nationality = dropList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=18,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    difficulty_1 = forms.BooleanField(label='النظر')
    difficulty_1_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة', widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_2 = forms.BooleanField(label='السمع')
    difficulty_2_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة', widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_3 = forms.BooleanField(label='الحركة')
    difficulty_3_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة',widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_4 = forms.BooleanField(label='التزكر')
    difficulty_4_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة', widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_5 = forms.BooleanField(label='العناية الشخصية')
    difficulty_5_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة', widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_6 = forms.BooleanField(label='التخاطب والتواصل')
    difficulty_6_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة', widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_7_txt = forms.TextInput(attrs={'label':'اخرى(توصيح)'})
    difficulty_7_degree = dropList(queryset=GenLookupListView.objects.filter(rp_id=9,lookup_id=173,l_list_active=1),to_field_name="lookup_list_id",required=True, label='درجةالصعوبة', widget=forms.RadioSelect(attrs={'class': 'form-control'}))
    difficulty_8 = forms.BooleanField(label='لايوجد')
    place_birth = dropList(queryset=GenLookupListView.objects.filter(rp_id=2,lookup_id=27,l_list_active=1),to_field_name="lookup_list_id",required=True, label='مكان الميلاد', widget=forms.Select(attrs={'class': 'chosen form-control'}))
    place_stay_previous = dropList(queryset=GenLookupListView.objects.filter(rp_id=2,lookup_id=27,l_list_active=1),to_field_name="lookup_list_id",required=True, label='مكان الاقامة السابق', widget=forms.Select(attrs={'class': 'chosen form-control'}))
    place_stay = dropList(queryset=GenLookupListView.objects.filter(rp_id=2,lookup_id=27,l_list_active=1),to_field_name="lookup_list_id",required=True, label='مكان الاقامة المعتاد', widget=forms.Select(attrs={'class': 'chosen form-control'}))

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
            'birth_month',
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
            'difficulty_7_txt',
            'difficulty_7_degree',
            'difficulty_8',
            'place_birth',
            'place_stay_previous',
            'place_stay',
            ]
