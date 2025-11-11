from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

from .models import StudentProfile, Subject, Question, QuizScore


# ---------------- HOME ----------------
def home(request):
    return render(request, 'home.html')


# ---------------- AUTH ----------------
def student_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm_password']

        age = request.POST['age']

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return redirect('student_register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('student_register')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('student_register')

        user = User.objects.create_user(username=username, email=email, password=password)
        StudentProfile.objects.create(user=user, age=age)

        messages.success(request, "Registration successful! Please login.")
        return redirect('student_login')


    return render(request, 'register.html')


def student_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')

        messages.error(request, "Invalid username or password.")
        return redirect('student_login')

    return render(request, 'login.html')


def student_logout(request):
    logout(request)
    return redirect('home')


# ---------------- STUDENT DASHBOARD ----------------
@login_required
def dashboard(request):
    subjects = Subject.objects.all()
    return render(request, 'dashboard.html', {"subjects": subjects})


# ---------------- QUIZ ----------------
@login_required
def take_quiz(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    questions = Question.objects.filter(subject=subject)

    if request.method == "POST":
        score = 0

        for q in questions:
            selected = request.POST.get(str(q.id))
            if selected == q.correct_answer:
                score += 1

        QuizScore.objects.create(
            student=request.user.studentprofile,
            subject=subject,
            score=score
        )

        return redirect('quiz_result', subject_id=subject.id)

    return render(request, 'take_quiz.html', {
        'subject': subject,
        'questions': questions
    })


@login_required
def quiz_result(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)
    score = QuizScore.objects.filter(
        student=request.user.studentprofile,
        subject=subject
    ).last()

    return render(request, 'quiz_result.html', {
        'subject': subject,
        'score': score.score if score else 0
    })


# ---------------- TEACHER AREA ----------------
@login_required
def teacher_dashboard(request):
    subjects = Subject.objects.all()
    return render(request, "teacher_dashboard.html", {"subjects": subjects})


@login_required
def add_subject(request):
    if request.method == "POST":
        name = request.POST["name"]
        Subject.objects.create(name=name)
        return redirect("teacher_dashboard")

    return render(request, "add_subject.html")


@login_required
def add_question(request, subject_id):
    subject = get_object_or_404(Subject, id=subject_id)

    if request.method == "POST":
        Question.objects.create(
            subject=subject,
            text=request.POST["text"],
            option1=request.POST["option1"],
            option2=request.POST["option2"],
            option3=request.POST["option3"],
            option4=request.POST["option4"],
            correct_answer=request.POST["correct_answer"],
        )
        return redirect("teacher_dashboard")

    return render(request, "add_question.html", {"subject": subject})


# ---------------- VIEW RESULTS ----------------
@login_required
def view_results(request):
    scores = QuizScore.objects.filter(student=request.user.studentprofile)
    return render(request, "results.html", {"scores": scores})


