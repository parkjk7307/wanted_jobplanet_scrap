from django.contrib import admin
from .models import *


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):

    fieldsets = [
        ('Question', {'fields': ['question_text']}),
        ('Create_Date', {'fields': ['pub_date'], 'classes': ['collapse']}),        
    ]
    readonly_fields = ['pub_date'] # model.py에 적혀있는 에러 해결법 auto_now_add=True
    inlines = [ChoiceInline]
    list_display = ('question_text','pub_date','was_published_recently')
    search_fields = ['question_text', 'choice__choice_text']
    list_filter = ['pub_date']

admin.site.register(Question, QuestionAdmin)