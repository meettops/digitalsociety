from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('signup_page/',signup_page,name='signup_page'),
    path('profile_page/',profile_page,name='profile_page'),
    path('security_page/',security_page,name='security_page'),
    path('otp_page/',otp_page,name='otp_page'),
    path('verify_otp/', verify_otp, name='verify_otp'),
    path('payment_page/',payment_page,name='payment_page'),
    path('event_page/',event_page,name='event_page'),
    path('society_rules_page/',society_rules_page,name='society_rules_page'),
    path('complain_page/',complain_page,name='complain_page'),
    path('signup/',signup,name='signup'),
    path('signin/',signin,name='signin'),
    path('signout/',signout,name='signout'),
    path('update_profile/',update_profile,name='update_profile'),
    path('change_password/',change_password,name='change_password'),


    #<----user path------->
    
    path('user_profile_page/',user_profile_page,name='user_profile_page'),
    path('change_complain/',change_complain,name='change_complain'),
    path('change_soc_rules/',change_soc_rules,name='change_soc_rules'),
    path('change_event/',change_event,name='change_event'),

    path('pay/', initiate_payment, name='pay'),
    path('callback/', callback, name='callback'),
    
]
