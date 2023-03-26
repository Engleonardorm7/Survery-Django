from django.urls import path
from . import views
from .views import CustomLoginView

app_name="polls"
urlpatterns=[
    #/polls/
    path("",views.IndexView.as_view(),name='index'),
    #/polls/holi/
    path("holi/", views.holi,name='holi'),
    path("<int:pk>/", views.DetailView.as_view(), name='detail'),
    path("<int:pk>/results", views.ResultView.as_view(), name='results'),
    path("<int:question_id>/vote", views.vote, name='vote'),
    path("login/", CustomLoginView.as_view(), name='login'),
]