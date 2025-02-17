from django.db import models
from django.core.validators import RegexValidator
from django.utils.timezone import now

# --- Models ---


class Book(models.Model):
    GENRE_CHOICES = [
        ("Fiction", "Fiction"),
        ("Non-Fiction", "Non-Fiction"),
        ("Sci-Fi", "Sci-Fi"),
        ("Biography", "Biography"),
    ]

    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default="Fiction")
    publication_year = models.PositiveIntegerField()
    available_copies = models.PositiveIntegerField(default=1)
    isbn_number = models.CharField(max_length=13, unique=True)
    rating = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title


class Member(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Phone number must be exactly 10 digits.")],
    )
    membership_start_date = models.DateField(default=now)
    membership_type = models.CharField(max_length=50)
    max_books_allowed = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class StaffMember(models.Model):
    ROLE_CHOICES = [
        ("Librarian", "Librarian"),
        ("Assistant", "Assistant"),
    ]

    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(
        max_length=10,
        validators=[RegexValidator(r"^\d{10}$", "Phone number must be exactly 10 digits.")],
    )
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class StaffActivityLog(models.Model):
    staff_member = models.ForeignKey("StaffMember", on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("Issued", "Issued"),
        ("Returned", "Returned"),
        ("Overdue", "Overdue"),
    ]

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    issue_date = models.DateField(default=now)
    return_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="Issued")
    fine_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.book.title} ({self.member.name})"

    def is_overdue(self):
        return self.return_date is None and self.due_date < now().date()
