from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('class/', views.class_list, name = 'class'),
    path('class/<int:pk>', views.class_detail_view, name='detail'),
    path('write/', views.writeindex, name = 'writeindex'),
    path('write/<int:pk>', views.newwrite, name = 'newwrite'),
    path('write/edit/<int:pk>/<int:kl>', views.edit, name = 'state_edit'),
    path('write/edit/', views.list, name = 'list'),
    path('faq/', views.faq, name = 'faq'),
    path('privacypolicy', views.confidencial, name = 'confidencial'),
    path('delete/<int:pk>', views.delete, name = 'delete'),

    path('login/', views.login, name = 'login'),
    path('logout/', views.logout_view, name = 'logout'),
    path('register/', views.register, name = 'register'),
    path('account/', views.account, name = 'account'),
    path('pasrec/', views.pasrec, name = 'pasrec')
]