from django import forms
from .models import Book, Member, Transaction, StaffMember
import datetime
from django.utils.timezone import now
from datetime import timedelta, date


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title",
            "author",
            "genre",
            "publication_year",
            "available_copies",
            "isbn_number",
            "rating",
        ]

    # Custom validation for publication year
    def clean_publication_year(self):
        publication_year = self.cleaned_data.get("publication_year")
        current_year = datetime.datetime.now().year
        if publication_year < 1900 or publication_year > current_year:
            raise forms.ValidationError(
                f"Please enter a valid year between 1900 and {current_year}."
            )
        return publication_year

    # Custom validation for available copies
    def clean_available_copies(self):
        available_copies = self.cleaned_data.get("available_copies")
        if available_copies < 0:
            raise forms.ValidationError("Available copies cannot be less than 0.")
        return available_copies

    # Custom validation for rating
    def clean_rating(self):
        rating = self.cleaned_data.get("rating")
        if rating is not None and (rating < 1 or rating > 5):
            raise forms.ValidationError("Rating must be between 1 and 5.")
        return rating


class MemberForm(forms.ModelForm):
    MEMBERSHIP_TYPE_CHOICES = [
        ("Basic", "Basic"),
        ("Premium", "Premium"),
        ("Elite", "Elite"),
    ]

    membership_type = forms.ChoiceField(choices=MEMBERSHIP_TYPE_CHOICES)

    class Meta:
        model = Member
        fields = [
            "name",
            "email",
            "phone_number",
            "membership_start_date",
            "membership_type",
            "max_books_allowed",
        ]
        widgets = {
            "membership_start_date": forms.DateInput(attrs={"type": "date"}),
        }

    # Override the form's clean method to set `max_books_allowed`
    def clean(self):
        cleaned_data = super().clean()
        membership_type = cleaned_data.get("membership_type")

        if membership_type == "Basic":
            cleaned_data["max_books_allowed"] = 2
        elif membership_type == "Premium":
            cleaned_data["max_books_allowed"] = 5
        elif membership_type == "Elite":
            cleaned_data["max_books_allowed"] = 10

        return cleaned_data


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "member",
            "book",
            "issue_date",
            "return_date",
            "status",
            "fine_amount",
        ]
        widgets = {
            "issue_date": forms.DateInput(attrs={"type": "date"}),
            "return_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set initial issue date to today
        self.fields["issue_date"].initial = now().date()

    def clean_book(self):
        book = self.cleaned_data.get("book")
        # Prevent transactions if available copies are 0
        if book.available_copies <= 0:
            raise forms.ValidationError("The selected book is not available.")
        return book

    def clean_return_date(self):
        issue_date = self.cleaned_data.get("issue_date")
        return_date = self.cleaned_data.get("return_date")

        # Validate that return date is later than issue date
        if return_date and return_date <= issue_date:
            raise forms.ValidationError("Return date must be later than issue date.")
        return return_date

    def clean(self):
        cleaned_data = super().clean()
        return_date = cleaned_data.get("return_date")
        issue_date = cleaned_data.get("issue_date")

        # Calculate fine if overdue
        if return_date and return_date > issue_date:
            days_overdue = (
                return_date - issue_date - timedelta(days=14)
            ).days  # Assuming 14 days borrowing period
            cleaned_data["fine_amount"] = max(0, days_overdue * 2.00)  # $2 per day fine for overdue
        return cleaned_data


class StaffMemberForm(forms.ModelForm):
    class Meta:
        model = StaffMember
        fields = ["name", "email", "role", "phone_number"]
