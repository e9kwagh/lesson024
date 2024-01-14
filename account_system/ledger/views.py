from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.admin import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import SignUpForm, TransactionForm
from .models import Account
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    return render(request, "ledger/home.html")


def loginpage(request):
    page = "login"
    form = AuthenticationForm(request, request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("transaction")
        else:
            messages.error(request, "Invalid username or password.")

    context = {"page": page, "form": form}
    return render(request, "ledger/loginpage.html", context)


def logoutUser(request):
    logout(request)
    return redirect("home")


@login_required(login_url="login")
def report(request):
    transactions = Account.objects.filter(user=request.user).order_by("-assign_date")
    return render(request, "ledger/report.html", {"transactions": transactions})


def signuppage(request):
    page = "signup"
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful. You are now logged in.")
            return redirect("home")
        else:
            messages.error(
                request, "Registration failed. Please correct the errors below."
            )
    else:
        form = SignUpForm()

    context = {"page": page, "form": form}
    return render(request, "ledger/signuppage.html", context)


@login_required(login_url="login")
def transaction(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)

        if form.is_valid():
            user = request.user
            date = form.cleaned_data["date"]
            category = form.cleaned_data["category"]
            description = form.cleaned_data["description"]
            transaction_type = form.cleaned_data["transaction_type"]
            amount = form.cleaned_data["amount"]
            payment_mode = form.cleaned_data["payment_mode"]

            debit = amount if transaction_type == "debit" else 0
            credit = amount if transaction_type == "credit" else 0

            last_transaction = (
                Account.objects.filter(user=user).order_by("-assign_date").first()
            )
            balance = (
                last_transaction.balance + credit - debit
                if last_transaction
                else credit - debit
            )

            Account.objects.create(
                user=user,
                assign_date=date,
                balance=balance,
                category=category,
                description=description,
                debit=debit,
                credit=credit,
                m_of_pay=payment_mode,
            )

            return redirect("report")
    else:
        form = TransactionForm()

    return render(request, "ledger/transaction.html", {"form": form})
