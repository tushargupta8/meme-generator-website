from django.urls import path
from . import views

urlpatterns = [
    path("",views.home,name='home'),
    path("register/",views.register,name="register"),
    path("login/",views.login,name="login"),
    path("meme/",views.getMeme,name="getMeme"),
    path('logout/',views.logout,name="logout"),
    path('meme_details/',views.meme_details,name='meme_details'),
    path('edit_memes/',views.edit,name="edit")
]
