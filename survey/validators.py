import os
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.core.validators import *
from django.contrib.auth.views import login
from survey.models import *

def validate_family_relation(value):
    member_no = FcpFamilyMemberTab.objects.filter(sample_id=2)
    if not member_no and value.lookup_list_id != 1700001:
        #family_relation = GenLookupListView.objects.get(rp_id=1,lookup_id=17,l_list_active=1,lookup_list_id=1700001)
        raise ValidationError(
            _('First family member must be Family head'),
            params={'value': value},
        )

    elif member_no and value.lookup_list_id == 1700001:
        raise ValidationError(
            _('Family head already added, Please select correct relationship with this member'),
            params={'value': value},
        )
