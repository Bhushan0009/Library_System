from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book, Member, Transaction, StaffMember, StaffActivityLog
from .forms import BookForm, MemberForm, TransactionForm, StaffMemberForm
from django.utils.timezone import now
from django.db.models import Count
from datetime import date
from .functions import *

# --- Views ---


def home(request):
    return render(request, "home.html")


# Book Views
def book_list(request):
    books = Book.objects.all()
    return render(request, "book_list.html", {"books": books})


def book_create(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()
    return render(request, "book_form.html", {"form": form, "title": "Add New Book"})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)
    return render(request, "book_form.html", {"form": form, "title": "Edit Book Details"})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("book_list")
    return render(request, "book_delete.html", {"book": book})


# Member Views
def member_list(request):
    members = Member.objects.all()
    return render(request, "member_list.html", {"members": members})


def member_create(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save()
            send_welcome_email(member)
        return redirect("member_list")
    else:
        form = MemberForm()
    return render(request, "member_form.html", {"form": form, "title": "Add New Member"})


def member_update(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect("member_list")
    else:
        form = MemberForm(instance=member)
    return render(
        request,
        "member_form.html",
        {"form": form, "title": "Edit Member Details"},
    )


def member_delete(request, pk):
    member = get_object_or_404(Member, pk=pk)
    if request.method == "POST":
        member.delete()
        return redirect("member_list")
    return render(request, "member_confirm_delete.html", {"member": member})


def top_members_report(request, month):
    top_members = (
        Transaction.objects.filter(issue_date__month=month)
        .values("member__name")
        .annotate(total_books=Count("book"))
        .order_by("-total_books")[:10]
    )

    return render(
        request,
        "top_members_report.html",
        {"top_members": top_members, "month": month},
    )


# Transaction Views
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, "transaction_list.html", {"transactions": transactions})


def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save()
            if transaction.status == "Issued":
                transaction.book.available_copies -= 1
                transaction.book.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm()
    return render(
        request,
        "transaction_form.html",
        {"form": form, "title": "Add New Transaction"},
    )


def transaction_update(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=transaction)
    return render(
        request,
        "transaction_form.html",
        {"form": form, "title": "Edit Transaction Details"},
    )


def transaction_delete(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == "POST":
        transaction.delete()
        return redirect("transaction_list")
    return render(
        request,
        "transaction_confirm_delete.html",
        {"transaction": transaction},
    )


def overdue_books_report(request):
    today = date.today()
    overdue_transactions = Transaction.objects.filter(return_date___lt=today, status="Issued")

    context = {"overdue_transactions": overdue_transactions}
    return render(request, "overdue_report.html", context)


# Staff Views
def staff_list(request):
    staff_members = StaffMember.objects.all()
    return render(request, "staff_list.html", {"staff_members": staff_members})


def staff_create(request):
    if request.method == "POST":
        form = StaffMemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("staff_list")
    else:
        form = StaffMemberForm()
    return render(
        request,
        "staff_form.html",
        {"form": form, "title": "Add New Staff Member"},
    )


def staff_update(request, pk):
    staff_member = get_object_or_404(StaffMember, pk=pk)
    if request.method == "POST":
        form = StaffMemberForm(request.POST, instance=staff_member)
        if form.is_valid():
            form.save()
            return redirect("staff_list")
    else:
        form = StaffMemberForm(instance=staff_member)
    return render(
        request,
        "staff_form.html",
        {"form": form, "title": "Edit Staff Member Details"},
    )


def staff_delete(request, pk):
    staff_member = get_object_or_404(StaffMember, pk=pk)
    if request.method == "POST":
        staff_member.delete()
        return redirect("staff_list")
    return render(request, "staff_confirm_delete.html", {"staff_member": staff_member})


def staff_activity_log(request):
    logs = StaffActivityLog.objects.order_by("-timestamp")
    return render(request, "staff_activity_log.html", {"logs": logs})


def genre_popularity_chart(request):
    genre_data = (
        Transaction.objects.values("book__genre__name")
        .annotate(total_borrowed=Count("book"))
        .order_by("-total_borrowed")
    )

    return render(request, "genre_popularity_chart.html", {"genre_data": genre_data})
