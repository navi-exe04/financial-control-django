"""
Defines all the user views for financial control
"""
from django.shortcuts import redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, FormView, View
from .models import Transaction, Category
from .forms import CustomUserForm, TransactionForm, CategoryForm
from decimal import Decimal

REPORT_TEMPLATE_URL = "/report/"
ERROR_MESSAGE_RESPONSE = "Something is wrong"

# Create your views here.
class HomeView(TemplateView):
    """
    The main view of the system
    """
    template_name = "home.html"


@method_decorator(login_required, name="dispatch")
class CreateTransactionView(FormView):
    """
    Create a new transaction in system
    """
    model = Transaction
    template_name = "create_transaction.html"
    form_class = TransactionForm
    success_url = ""

    def form_valid(self, form):
        # Define the transaction information
        transaction = form.save(commit=False)
        transaction.user = self.request.user
        transaction.save()
        # Save the transaction amount
        amount = Decimal(self.request.POST['amount'])
        # Check if there is a expense or income
        if self.request.POST['transaction_type'] == "EX":
            self.request.user.total_amount -= amount
            self.success_url = "/expenses/"
        else:
            self.request.user.total_amount += amount
            self.success_url = "/incomes/"
        # update the user information
        self.request.user.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form, error=ERROR_MESSAGE_RESPONSE)
        )


@method_decorator(login_required, name="dispatch")
class CreateCategoryView(FormView):
    """
    Create a new category in system
    """
    model = Category
    template_name = "create_category.html"
    form_class = CategoryForm
    success_url = REPORT_TEMPLATE_URL

    def form_valid(self, form):
        category = form.save(commit=False)
        category.user = self.request.user
        category.save()
        return redirect(self.success_url)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form, error=ERROR_MESSAGE_RESPONSE)
        )


@method_decorator(login_required, name="dispatch")
class ExpensesView(ListView):
    """
    List of expenses of the user
    """
    model = Transaction
    template_name = "expenses.html"
    context_object_name = "expenses"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user, transaction_type="EX")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expense_count"] = self.get_queryset().count()
        return context


@method_decorator(login_required, name="dispatch")
class IncomesView(ListView):
    """
    List of incomes of the user
    """
    model = Transaction
    template_name = "incomes.html"
    context_object_name = "incomes"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user, transaction_type="IN")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["incomes_count"] = self.get_queryset().count()
        return context

@method_decorator(login_required, name="dispatch")
class ReportView(ListView):
    """
    General report of expenses and incomes
    """
    model = Transaction
    template_name = "report.html"
    context_object_name = "transactions"

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_amount"] = self.request.user.total_amount
        context["transactions_count"] = self.get_queryset().count()
        return context


# user views
class RegisterUserView(FormView):
    """
    Manage the register of a new user in the system
    """
    template_name = "register.html"
    form_class = CustomUserForm
    success_url = REPORT_TEMPLATE_URL

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
        return self.render_to_response(
            self.get_context_data(form=form, error=ERROR_MESSAGE_RESPONSE)
        )


class LoginUserView(FormView):
    """
    Manage the login of a user in the system
    """
    template_name = "login.html"
    form_class = AuthenticationForm
    success_url = REPORT_TEMPLATE_URL

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
