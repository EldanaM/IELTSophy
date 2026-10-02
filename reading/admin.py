from django.contrib import admin
from .models import Text, Question, UserProfile, Achievement, PreparingVideo, VocabularyWord, TestSession, Mistake

@admin.register(Text)
class TextAdmin(admin.ModelAdmin):
    list_display =('title', 'level', 'topic')
    list_filter =('level', 'topic')
    search_fields =('title',)

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display =('question_text', 'text', 'question_type', 'correct_option')
    list_filter =('text', 'question_type')

@admin.register(PreparingVideo)
class PreparingVideoAdmin(admin.ModelAdmin):
    list_display =('title', 'tag', 'type', 'date')
    list_filter =('tag', 'type')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display =('user', 'level', 'streak', 'total_tests')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display =('user', 'title', 'unlocked_at')

@admin.register(VocabularyWord)
class VocabularyWordAdmin(admin.ModelAdmin):
    list_display =('user', 'word', 'added_at')

@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display =('user', 'text', 'percent', 'time_spent', 'started_at')

@admin.register(Mistake)
class MistakeAdmin(admin.ModelAdmin):
    list_display =('user', 'question_type', 'count')