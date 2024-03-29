from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import ListView
from .models import Question
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question
from django.views.decorators.csrf import csrf_exempt
from app_cms.utils import get_user_profile

# Create your views here.
@csrf_exempt
class IndexView(ListView):
    template_name = "app_polls/polls.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "app_polls/detail.html"
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "app_polls/results.html"


def polls(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    user_id = request.session.get('user_id')
    profile = get_user_profile(user_id)
    context = {"latest_question_list": latest_question_list,
               'is_authenticated': request.user.is_authenticated, 
               "profile": profile}
    return render(request, "app_polls/polls.html", context)


def new_poll(request):
    if request.method == 'POST':
        question_text = request.POST.get('question_text')
        # Set pub_date to the current date and time
        question = Question.objects.create(question_text=question_text, pub_date=timezone.now())
        
        for key, value in request.POST.items():
            if key.startswith("choice_"):
                Choice.objects.create(question=question, choice_text=value)
        
        return redirect('app_polls:polls')

    return render(request, 'app_polls/new_poll.html')


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "app_polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "app_polls/results.html", {"question": question})


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "app_polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("app_polls:results", args=(question.id,)))