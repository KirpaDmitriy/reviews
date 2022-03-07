from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views import generic

from .models import User, Review

from .utils import *


class AllReviews(generic.ListView):
    template_name = 'reviews/index.html'
    context_object_name = 'all_reviews'

    def get_queryset(self):
        return list(map(lambda r: r.__str__(), Review.objects.all()))


def add_review(request):
    print(request.POST)
    if ('choice' not in request.POST) or ('user_login' not in request.POST):
        return render(request, 'reviews/new_review_form.html', {
            'possible_rates': list(range(RATE_LOWER_BOUND, RATE_UPPER_BOUND+1)),
            'error_message': "Чтобы добавить отзыв, мне необходимо знать ваш логин и оценку",
        })
    else:
        try:
            current_user = User.objects.get(login__exact=request.POST['user_login'])
        except Exception:
            return render(request, 'reviews/new_review_form.html', {
                'possible_rates': list(range(RATE_LOWER_BOUND, RATE_UPPER_BOUND+1)),
                'error_message': "Неверный логин",
            })
        else:
            new_review = Review(author=current_user, rate=request.POST['choice'], text=request.POST['text'])
            new_review.save()
            return HttpResponseRedirect(reverse('index'))
