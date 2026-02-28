from django.urls import path
from . import views

app_name = 'notebooks'

urlpatterns = [
    path('', views.notebook_list, name='notebook_list'),
    path('<slug:slug>/', views.notebook_detail, name='notebook_detail'),
    path('<slug:slug>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:pk>/delete/', views.delete_comment, name='delete_comment'),
]
