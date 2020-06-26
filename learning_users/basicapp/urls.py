from django.urls import path, include
from basicapp import views

# Template tagging
app_name = 'basicapp'

urlpatterns = [
    path('registration/', views.registration, name="registration"),
    path('login/', views.user_login, name="user_login"),
    path('other/', views.other, name="other"),
]
