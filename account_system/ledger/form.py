from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]


class TransactionForm(forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    category = forms.ChoiceField(
        choices=[
            ("food", "Food"),
            ("rent", "Rent"),
            ("utilities", "Utilities"),
            ("movies", "Movies"),
            ("travel", "Travel"),
            ("petrol", "Petrol"),
            ("salary", "Salary"),
            ("emi", "EMI"),
        ]
    )
    description = forms.ChoiceField(
        choices=[
            ("groceries", "Groceries"),
            ("dinner", "Dinner"),
            ("electricity", "Electricity"),
            ("internet", "Internet"),
            ("flight", "Flight"),
        ]
    )
    transaction_type = forms.ChoiceField(
        choices=[("debit", "Debit"), ("credit", "Credit")]
    )
    amount = forms.IntegerField(
        widget=forms.NumberInput(attrs={"step": "1", "min": "1"})
    )
    payment_mode = forms.ChoiceField(
        choices=[("cash", "Cash"), ("card", "Card"), ("upi", "UPI")]
    )
