from django.contrib import admin
from .models import Question, Choice


class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra=3

# Personaliza como se ven los modelos en el administrador
class QuestionAdmin(admin.ModelAdmin):
    fields=["pub_date","question_text"]
    inlines=[ChoiceInLine] #incluir las respuestas cuando se crea la pregunta
    list_display=["question_text","pub_date","was_published_recently"]
    list_filter=["pub_date","question_text"]
    search_fields=["question_text"]

admin.site.register(Question,QuestionAdmin)
admin.site.register(Choice)
