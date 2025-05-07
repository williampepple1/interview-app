from django.contrib import admin
from .models import Assessment, Question, UserAssessment, UserResponse

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at')
    inlines = [QuestionInline]

    def save_model(self, request, obj, form, change):
        if not change:  # If creating new assessment
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'assessment', 'correct_option')
    list_filter = ('assessment',)

@admin.register(UserAssessment)
class UserAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'assessment', 'started_at', 'completed_at', 'score')
    list_filter = ('assessment', 'user')

@admin.register(UserResponse)
class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('user_assessment', 'question', 'selected_option', 'is_correct', 'response_time')
    list_filter = ('user_assessment', 'is_correct')
