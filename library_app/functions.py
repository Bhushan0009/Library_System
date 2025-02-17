from datetime import date
from django.core.mail import send_mail
from .models import Transaction


# --- Utility Functions ---
def send_welcome_email(member):
    subject = "Welcome to the Library!"
    message = f"Hello {member.name},\n\nWelcome to our Library System. Enjoy your reading!\n\nRegards,\nLibrary Team"
    send_mail(subject, message, "bhushansonar009@gmail.com", [member.email])


def send_overdue_notification(transaction):
    if transaction.status == "Overdue":
        subject = "Overdue Book Alert"
        message = (
            f"Dear {transaction.member.name},\n\nYour borrowed book '{transaction.book.title}' "
            f"is overdue. The current fine is ₹{transaction.fine_amount}. Please return it as soon as possible.\n\nRegards,\nLibrary Team"
        )
        send_mail(
            subject,
            message,
            "bhushansonar009@gmail.com",
            [transaction.member.email],
        )
