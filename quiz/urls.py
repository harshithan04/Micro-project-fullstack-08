from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Home Page (redirects to login if not logged in)
    path('', views.home, name='home'),

    # Student authentication
    path('login/', views.student_login, name='student_login'),
    path('register/', views.student_register, name='student_register'),
    path('logout/', views.student_logout, name='logout'),

    # Dashboard & Quiz
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/<int:subject_id>/', views.take_quiz, name='take_quiz'),
    path('result/<int:subject_id>/', views.quiz_result, name='quiz_result'),
    path('results/', views.view_results, name='results'),

    # Teacher routes
    path('teacher/', views.teacher_dashboard, name='teacher_dashboard'),
    path('teacher/add_subject/', views.add_subject, name='add_subject'),
    path('teacher/add_question/<int:subject_id>/', views.add_question, name='add_question'),

    # Password reset routes
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]


