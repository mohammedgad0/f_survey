from django import forms
from django.forms import ModelForm, Textarea, TextInput, DateField, ModelChoiceField
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from survey.models import *
#from django.forms.models import modelformset_factor
class familyRelationsList(ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.type
class FcpFamilyMemberTabFormStep1(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FcpFamilyMemberTabFormStep1, self).__init__(*args, **kwargs)


    CHOICES = (('1', _('Employee'),), ('2', _('Department'),))
    # family_relation = familyRelationsList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=17,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    # family_relation = familyRelationsList(queryset=GenLookupListView.objects.filter(rp_id=1,lookup_id=17,l_list_active=1),to_field_name="lookup_list_id",required=True,widget=forms.Select(attrs={'class': 'chosen-select form-control'}))
    family_relation = forms.ChoiceField(label=_('Assignto'),required=False,widget=forms.RadioSelect(attrs={'class':'form-check-input-task'}), choices=CHOICES)
    class Meta:
        model = FcpFamilyMemberTab
        fields = ['member_name_first',
            'member_name_second',
            'member_name_third',
            'id_number_member',
            'family_relation',
            'gender',
            'age',
            'birth_month',
            'birth_year',
            'nationality',
            ]
