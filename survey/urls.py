from django.conf import settings
from django.urls import path, re_path
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
    # Page to add house form
    path('add-house/', add_house, name='add-house'),
    # Death form
    path('death-form/', death_form, name='death-form'),

]
