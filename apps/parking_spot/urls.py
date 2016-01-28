from django.conf.urls import url, include
from django.contrib import admin
from . import views

from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.Index.as_view(), name = 'parking_index'),
    url(r'sign_up', views.SignUp.as_view(), name='parking_sign_up'),
    url(r'sign_in', views.SignIn.as_view(), name='parking_sign_in'),
    url(r'user/(?P<id>\d+)', login_required(views.User.as_view(), login_url = '/sign_in'), name='user_detail'),
    url(r'user', login_required(views.User.as_view(), login_url = '/sign_in'), name='user_detail_post'),
]
