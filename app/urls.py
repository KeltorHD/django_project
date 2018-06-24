from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('class/', views.ClassListView.as_view(), name = 'class'),
    path('class/<int:pk>', views.class_detail_view, name='detail'),
    path('write/', views.writeindex, name = 'writeindex'),
    path('write/<int:pk>', views.newwrite, name = 'newwrite'),
    path('write/edit/<int:pk>/<int:kl>', views.edit, name = 'state_edit'),
    path('write/edit/', views.list, name = 'list'),
    path('faq/', views.faq, name = 'faq'),

    path('login/', views.login, name = 'login'),
    path('logout/', views.logout_view, name = 'logout')
]