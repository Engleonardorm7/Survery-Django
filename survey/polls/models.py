import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    #id:             - se puede omitir ya que Django lo hace automaticamente
    question_text = models.CharField(max_length=200) #string
    pub_date = models.DateTimeField("Date published")

    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now()-datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)#on_delete=models.CASCADE "si se borra la pregunta, las respuestas tambien serán borradas"
    choice_text=models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text