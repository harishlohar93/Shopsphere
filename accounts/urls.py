
from django.urls import path
from accounts.views import login_page
from accounts.views import register_page , activate_email

from . import views




urlpatterns = [
    path('login/' ,login_page , name="login"),
    path('register/' ,register_page , name="register"),
    path('activate/<email_token>/' ,activate_email , name="activate_email"),
    


    
    
] 