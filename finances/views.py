"""
Defines all the user views for financial control
"""
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView, View
from .models import Transaction
from .forms import CustomUserForm

# Create your views here.


class HomeView(TemplateView):
    """
    The main view of the system
    """
    template_name = "home.html"


@method_decorator(login_required, name="dispatch")
class ExpensesView(ListView):
    """
    List of expenses of the user
    """
    model = Transaction
    template_name = "expenses.html"


@method_decorator(login_required, name="dispatch")
class IncomesView(ListView):
    """
    List of incomes of the user
    """
    model = Transaction
    template_name = "incomes.html"


@method_decorator(login_required, name="dispatch")
class ReportView(ListView):
    """
    General report of expenses and incomes
    """
    model = Transaction
    template_name = "report.html"


# user views
class RegisterUserView(FormView):
    """
    Manage the register of a new user in the system
    """
    template_name = "register.html"
    form_class = CustomUserForm
    success_url = "/report/"

    def form_valid(self, form):
        """
        Verify if the user information to register is correct to save
        """
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)

    def form_invalid(self, form):
        """
        Something with the user information is wrong
        """
        error = "Something is wrong"
        return self.render_to_response(
            self.get_context_data(form=form, error=error)
        )


class LoginUserView(FormView):
    """
    Manage the login of a user in the system
    """
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = "/report/"

    def form_valid(self, form):
        """
        Authenticate if there is a user with the username and password
        """
        username = self.request.POST['username']
        password = self.request.POST['password']
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)
            return redirect(self.success_url)
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """
        The user or the password are wrong
        """
        error = "Invalid user or password"
        return self.render_to_response(
            self.get_context_data(form=form, error=error)
        )


@method_decorator(login_required, name="dispatch")
class LogoutUserView(View):
    """
    Logout the user from the system
    """
    redirect_url = "/login/"

    def get(self, request):
        """
        Logout the system
        """
        logout(request)
        return redirect(self.redirect_url)
