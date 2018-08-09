from django.conf import settings
from django.urls import path, re_path, reverse
from survey.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url

app_name = 'survey'

urlpatterns = [
    # Home
    path('', home, name='home'),
    # Login page
    path(r'login/<str:token>/', login, name='login'),
    # Add family member
    path('add-family/', add_family_member, name='add-family'),
    # ajax path to populate dependend child select field with correct values
    path('ajax/options/', ajax_render_list_options, name='ajax-options'),
    # list family members by family id
    re_path(r'^family/(?P<fid>\w+)/$', familyMembersList, name='list-family'),
    # complete member info (step2)
    re_path(r'^add-member-info/(?P<fm_id>\w+)/$', add_member_info , name='add-member-info'),
    #edit member on step 1
    re_path(r'^edit-member/(?P<fid>\w+)/$', edit_family_member, name='edit-family-member'),
    # Page to add house form
    path('add-house/', add_house, name='add-house'),
    # Death form
    path('death-form/', death_form, name='death-form'),
    # Death form Edit
    path('death-form-edit/<int:member_id>/', death_form_edit, name='death-form-edit'),
    # test error
    path('check-error/', check_error, name='check-error'),
    # popup delete
    path(r'delete-member/', delete_member, name='delete-member'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
