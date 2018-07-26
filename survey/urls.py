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
    path('add-family/', FcpFamilyMemberTabFormStep1View, name='add-family'),

]
