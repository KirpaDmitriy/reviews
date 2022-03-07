from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


RATE_LOWER_BOUND, RATE_UPPER_BOUND = 1, 5


class User(models.Model):
    login = models.TextField(max_length=100, unique=True)

    def __str__(self):
        return self.login


class Review(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # если удалим пользователя, удалятся и его отзывы
    rate = models.IntegerField(validators=[
        MinValueValidator(1), MaxValueValidator(5)
    ])
    text = models.TextField(default='', blank=True)
    pub_date = models.DateTimeField(default=timezone.now())
    is_published = models.BooleanField(default=False)

    def __str__(self):
        return 'id: {}; ' \
               'author_id: {}; ' \
               'rate: {}; ' \
               'text: {}; ' \
               'date: {}; ' \
               'is_published: {}'.format(self.id, self.author.id, self.rate, self.text, self.pub_date, self.is_published)


