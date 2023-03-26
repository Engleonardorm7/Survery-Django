import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

# Create your tests here..
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """This test returns false for questions whose pub_date is in the future"""
        time= timezone.now() + datetime.timedelta(days=30)
        furure_quiestion=Question(question_text="Cual es la mejor proteina?",pub_date=time)
        self.assertIs(furure_quiestion.was_published_recently(),False)

    def test_was_published_recently_with_past_questions(self):
        """was_published_recently() must return Flase for questions whose pub_date is more than 1 day in the past"""
        time = timezone.now() - datetime.timedelta(days=30)
        past_question = Question(question_text="Cual es la mejor proteina?",pub_date=time)
        self.assertIs(past_question.was_published_recently(),False)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently() must return True for questions whose pub_date is actual"""
        time = timezone.now()
        present_question = Question(question_text="Cual es la mejor proteina?",pub_date=time)
        self.assertIs(present_question.was_published_recently(),True)


def create_question(question_text,days):
    """
    Create a question with the given "question_text"
    and published the given number of days offset 
    to now(negative for questions in the past and 
    positive for questions in the future)
    """
    time=timezone.now()+datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

def create_choice(pk,choice_text,votes=0):
    """
    Create a choice with the given "choice_text",
    pk and votes
    """
    question=Question.objects.get(pk=pk)
    return question.choice_set.create(choice_text=choice_text,votes=votes)

class QuestionIndexViewTest(TestCase):


    def test_no_questions(self):
        """if no question exist, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, "Polls are not available.")
        self.assertQuerysetEqual(response.context["question_list"],[])
    

    def test_future_questions_are_not_displayed(self):
        """Future questions are not displayed until pub_date equals to the present time"""
        response = self.client.get(reverse("polls:index"))
        time= timezone.now() + datetime.timedelta(days=30)
        furure_question=Question(question_text="Cual es la mejor proteina?",pub_date=time)
        self.assertNotIn(furure_question,response.context["question_list"])


    def test_past_questions(self):
        """Past questions are displayed in the index page"""
        question=create_question("Past question",days=-10)
        choice1 = create_choice(pk=question.id, choice_text="Best protein", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Bipro", votes=0)
        response=self.client.get(reverse("polls:index"))
        #self.assertIn(question,response.context["question_list"])
        self.assertQuerysetEqual(response.context["question_list"],[question])

    def test_future_and_past_questions(self):
        """Even if both, past and future question exist, only past questions are displayed"""
        past_question = create_question(question_text="Past question",days=-30)
        choice1 = create_choice(pk=past_question.id, choice_text="Best protein", votes=0)
        choice2 = create_choice(pk=past_question.id, choice_text="Bipro", votes=0)
        future_question = create_question(question_text="Future question",days=30)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["question_list"],
            [past_question]
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions"""
        past_question1 = create_question(question_text="Past question 1",days=-30)
        choice1 = create_choice(pk=past_question1.id, choice_text="Best protein", votes=0)
        choice2 = create_choice(pk=past_question1.id, choice_text="Bipro", votes=0)
        past_question2 = create_question(question_text="Past question 2",days=-40)
        choice1 = create_choice(pk=past_question2.id, choice_text="Best protein", votes=0)
        choice2 = create_choice(pk=past_question2.id, choice_text="Bipro", votes=0)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["question_list"],
            [past_question1,past_question2]
        )
    
    def test_two_future_questions(self):
        """The questions index page may display multiple questions"""
        future_question1 = create_question(question_text="Future question 1",days=30)
        future_question2 = create_question(question_text="Future question 2",days=40)
        response=self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["question_list"],
            []
        )

class Question_Detail_View_Tests(TestCase):

    def test_future_question(self):
        """The detail view of a future question returns
        a 404 error not found"""
        future_question=create_question("Future_question",days=30)
        url=reverse("polls:detail",args=(future_question.id,))
        response=self.client.get(url)
        self.assertEqual(response.status_code,404)

    def test_past_question(self):
        """The detail view of a past question displays
        the question text"""
        past_question=create_question("Past_question",days=-30)
        url=reverse("polls:detail",args=(past_question.id,))
        response=self.client.get(url)
        self.assertContains(response,past_question.question_text)

    def test_question_without_choices(self):
        """
        Questions that have no choices aren't displayed in the index view
        """
        question = create_question("Cual es tu proteina favorita?", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["question_list"], [])

    def test_question_with_choices(self):
        """
        Question with choices are displayed in the index view
        """
        question = create_question("Cual es tu proteina favorita", days=-10)
        choice1 = create_choice(pk=question.id, choice_text="Best protein", votes=0)
        choice2 = create_choice(pk=question.id, choice_text="Bipro", votes=0)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["question_list"], [question])



class ResultViewTest(TestCase):

    def test_with_past_question(self):
        """
        The result view with a pub date in the past display the 
        question's text
        """
        past_question = create_question("past question", days=-15)
        url = reverse("polls:results", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)

    def test_with_future_question(self):
        """
        Questions with a future date aren't displayed and this return a 404 error(not found) 
        until the date is the specified date
        """
        future_question = create_question("this is a future question", days=30)
        url = reverse("polls:results", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    
   