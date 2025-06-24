from django.urls import path
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('create_order/', views.create_order, name='create_order'),
    path('api/verify-payment/', views.verify_payment , name="verify_payment"),
    path('api/update-plan/', views.update_plan, name='update_plan'),
    
] 
