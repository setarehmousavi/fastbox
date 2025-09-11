from django.contrib.auth import authenticate, login, logout, get_user_model
from django.core.cache import cache
from django.urls import reverse_lazy
from django.views.generic import FormView, View
from django.shortcuts import render,  redirect
from user.forms import UserRegisterationForm
from user.models import UserProfile


User = get_user_model()


class RegisterView(FormView):
    template_name = 'accounts/signup.html'
    form_class = UserRegisterationForm
    success_url = reverse_lazy('user:index')

    def form_valid(self, form):
        user = form.save(commit = False)
        user.set_password(form.cleaned_data['password'])
        user.is_active = False
        user.save()
        user_object = User.objects.filter(id=user.id).first()
        UserProfile(user=user_object, role=0).save()

        send_activation_link.delay(user.id)
        return super().form_valid(form)
    




def index_view(request):
    return render(request,'parcel/index.html')


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("user:index") 
        else:
            return render(request, self.template_name, {"error": "Invalid username or password"})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('user:index')

