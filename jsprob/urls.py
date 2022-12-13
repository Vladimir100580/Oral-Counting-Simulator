from django.urls import path
from . import views     #'.' - из этой же папки импортируем метод views

from datetime import datetime

from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import forms


urlpatterns = [
    path('', views.hello, name='home'),  # , name = 'home'
    path('list1', views.list1, name='list1'),
    path('list2', views.list2, name='list2'),
    path('list3', views.list3, name='list3'),
    path('list4', views.list4, name='list4'),
    path('list5', views.list5, name='list5'),
    path('level1', views.level1, name='level1'),
    path('level2', views.level2, name='level2'),
    path('level3', views.level3, name='level3'),
    path('level4', views.level4, name='level4'),
    path('level5', views.level5, name='level5'),
    path('regist', views.regist, name='regist'),
    path('itog', views.itog, name='itog'),
    path('toptab', views.toptab, name='toptab'),
    path('instr', views.instr, name='instr'),
    path('reset', views.reset, name='reset'),
    path('toplvl', views.toplvl, name='toplvl'),

    path('login/',
         LoginView.as_view
             (
             template_name='jsprob/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Log in',
                 'year': datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
