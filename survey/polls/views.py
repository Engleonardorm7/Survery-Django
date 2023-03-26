from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice
from django.views import generic

from django.contrib.auth.views import LoginView
from django.db.models import Count

from django.utils import timezone

class CustomLoginView(LoginView):
    template_name = 'login.html'  # Especifique la plantilla de inicio de sesión a utilizar


# Create your views here.

# def index(request):
#     """
#     Vista que muestra una lista de todas las preguntas disponibles en la base de datos de preguntas.
    
#     Argumentos:
#     - request: objeto HttpRequest que representa la solicitud HTTP que se está procesando.
    
#     Retorna:
#     - HttpResponse que representa la respuesta HTTP que se enviará al cliente que realizó la solicitud.
    
#     """
#     question_list = Question.objects.all()
#     return render(request,"polls/index.html",{
#         "question_list":question_list
#     })


def holi(request):
     return HttpResponse("Holi world")


# def detail(request, question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request, "polls/detail.html",{
#         "question":question,
#     })
#     #question=Question.objects.get(pk=question_id)

# def results(request, question_id):
#     question=get_object_or_404(Question,pk=question_id)
#     return render(request, "polls/results.html",{
#         "question":question,
#     })

class IndexView(generic.ListView):
    template_name="polls/index.html"
    context_object_name= "question_list"

    # def get_queryset(self):
    #    """Return the last five published questions that have at least 2 questions""" 
    #    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]
    
    def get_queryset(self):
        """Return the last five published questions that have at least 2 questions"""
        question=Question.objects.filter(pub_date__lte=timezone.now()).annotate(num_choices=Count('choice'))
        question=question.filter(num_choices__gte=2).order_by('-pub_date')[:5]
        return question

class DetailView(generic.DetailView):
    model=Question
    template_name="polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that are not published yet
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultView(generic.DetailView):
    model=Question
    template_name="polls/results.html"

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

def vote(request, question_id):
    question=get_object_or_404(Question,pk=question_id)
    try:
        selected_choice=question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html",{
            "question":question,
            "error_message":"No elegiste ninguna respuesta"
        })
    else:
        selected_choice.votes +=1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results",args=(question_id,)))
