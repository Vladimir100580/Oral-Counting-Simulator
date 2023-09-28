from django.urls import path
from . import views     #'.' - из этой же папки импортируем метод views

from django.contrib.auth.views import LoginView, LogoutView


urlpatterns = [
    path('', views.hello, name='home'),  # , name = 'home'
    path('12', views.hello, name='home1'),
    path('13', views.brend, name='brend'),
    path('begin', views.begin, name='begin'),
    path('changefik', views.changefik, name='changefik'),
    path('dayend', views.dayend, name='dayend'),
    path('instr', views.instr, name='instr'),
    path('itog', views.itog, name='itog'),
    path('itoglv', views.itoglv, name='itoglv'),
    path('passLv', views.passLv, name='passLv'),
    path('progress', views.progress, name='progress'),
    path('regist', views.regist, name='regist'),
    path('reset', views.reset, name='reset'),
    path('topday', views.topday, name='topday'),
    path('topdays', views.topdays, name='topdays'),
    path('toptab', views.toptab, name='toptab'),
    path('toplvl', views.toplvl, name='toplvl'),
    path('topglob', views.topglob, name='topglob'),
    path('unification', views.unification, name='unification'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
]
