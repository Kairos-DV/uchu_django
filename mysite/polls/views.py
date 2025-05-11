from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from .models import Choice, Question
from django.utils import timezone


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

"""
Vote not change
"""
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))

# @login_required()
def questions(request):
    profile = request.user.profile
    questions = Question.objects.all()
    custom_range, questions = paginateObjects(request, questions, 3)
    context = {'questions': questions, 'custom_range': custom_range, 'profile': profile}
    return render(request, 'polls/questions.html', context)

# @login_required()
def question(request, question_id):
    profile = request.user.profile
    question = Question.objects.get(pk=question_id)
    context = {'question': question,
    'profile': profile}
    return render(request,
        'polls/question.html', context)

# @login_required()
def results(request, question_id):
    profile = request.user.profile
    question = get_object_or_404(Question, pk=question_id)
    labels = []
    data = []
    votes = question.choice_set.select_related('question').all()
    for item in votes:
        labels.append(item.name)
        data.append(item.votes)
    context = {'question': question,
    'profile': profile,
    'labels': labels,
    'data': data}
    return render(request,
        'polls/results.html', context)

# @login_required()
def vote(request, question_id):
    profile = request.user.profile
    question = get_object_or_404(Question, pk=question_id)
    try:
        user_choice = question.choice_set.get(pk=request.POST['choice'])
        if not question.user_voted(request.user):
            messages.error(request,
                'Вы уже голосовали в этом опросе.')
            return render(request,
                'polls/question.html',
                {'question': question,'profile': profile})
        if user_choice:
            user_choice.votes += 1
            user_choice.save()
            vote = Vote(user=request.user, question=question, choice=user_choice)
            vote.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    except (KeyError, UnboundLocalError):
        messages.error(request, 'Вы не выбрали вариант ответа!')
        return render(request, 'polls/question.html', {'question': question})
    return render(request,
        'polls/results.html',
        {'question': question, 'profile': profile})