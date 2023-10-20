from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.views.generic import TemplateView, CreateView
from .forms import ProfileEditForm
from .models import Profile


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"

class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = "myauth/register.html"
    success_url = reverse_lazy("myauth:about-me")

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request,
                            username=username,
                            password=password)
        login(request=self.request, user=user)
        return response

# def login_view(request:HttpRequest) -> HttpResponse:
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#         return render(request, 'myauth/login.html')
#
#     username = request.POST["username"]
#     password = request.POST["password"]
#
#     user = authenticate(request, username=username, password=password)
#     if user:
#         login(request, user)
#         return redirect("/admin/")
#
#     return render(request, "myauth/login.html", {"error": "Invalid login credentials"})
#
# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse("myauth:login"))

class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("Cookie set!")
    response.set_cookie("key", "some cookie value", max_age=3600)
    return response


def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("key", "default cookie value")
    return HttpResponse(f'Cookie: {value!r}')

@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["key"] = "some session value"
    return HttpResponse("Session set!")

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("key", "default session value")
    return HttpResponse(f"Session value: {value}")

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo":"bar", "spam":"eggs"})


class ProfileDetailsView(DetailView):
    template_name = 'myauth/profile_detail.html'
    queryset = Profile.objects.all()
    context_object_name = "profile"


class ProfilesListView(ListView):
    template_name = 'myauth/profiles_list.html'
    queryset = Profile.objects.all()
    context_object_name = "profiles"

class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    # model = Profile
    template_name = "myauth/profile_update_form.html"
    queryset = Profile.objects.all()
    context_object_name = "profile"
    form_class = ProfileEditForm

    def test_func(self):
        if self.request.user.id == self.get_object().user.profile.user_id or self.request.user.is_staff:
            return True
        return False

    def get_success_url(self):
        return reverse(
            "myauth:profiles_list"
        )