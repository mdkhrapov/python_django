from django.urls import path
from django.contrib.auth.views import LoginView
from .views import (
    # login_view,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    MyLogoutView,
    RegisterView,
    AboutMeView,
    FooBarView,
    ProfilesListView,
    ProfileDetailsView,
    ProfileUpdateView,
    HelloView,
)

app_name ='myauth'

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(
            template_name="myauth/login.html",
            redirect_authenticated_user = True,
        ), name="login"),
    path("hello/", HelloView.as_view(), name="hello"),
    path("logout/", MyLogoutView.as_view(), name="logout"),
    path("register", RegisterView.as_view(), name="register"),
    path("about-me/", AboutMeView.as_view(), name="about-me"),
    path("cookie/get", get_cookie_view, name="cookie-get"),
    path("cookie/set", set_cookie_view, name="cookie-set"),
    path("session/get", get_session_view, name="session-get"),
    path("session/set", set_session_view, name="session-set"),
    path("foo-bar/", FooBarView.as_view(), name="foo-bar"),
    path("profiles/", ProfilesListView.as_view(), name="profiles_list"),
    path("profiles/<int:pk>/", ProfileDetailsView.as_view(), name="profile_details"),
    path("profile/<int:pk>/update", ProfileUpdateView.as_view(), name="profile_update"),
]