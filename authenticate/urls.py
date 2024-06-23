from django.urls import path
from django.contrib.auth.views import LogoutView

from authenticate import views


urlpatterns = [
    path('/signin',views.signin, name='signin'),
    path('/signup',views.signup, name='signup'),
    path('/logout', LogoutView.as_view(next_page='signin'), name='logout'),
]
