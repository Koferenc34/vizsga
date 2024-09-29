from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('login', views.Login_page.as_view(), name='login_page'),
    path('logout', views.Logout_page.as_view(), name="logout"),
    path('register', views.Register_page.as_view(), name='register_page'),
    path('download/<str:fileName>', views.Download.as_view(), name="download")
]
