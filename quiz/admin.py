from django.contrib import admin
from .models import Subject, Question, StudentProfile, QuizScore

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1   # how many blank slots to show

class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [QuestionInline]

admin.site.register(Subject, SubjectAdmin)
admin.site.register(Question)
admin.site.register(StudentProfile)
admin.site.register(QuizScore)



