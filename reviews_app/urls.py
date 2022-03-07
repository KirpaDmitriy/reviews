from django.urls import path
from . import views

urlpatterns = [
    path('all', views.AllReviews.as_view(), name='index'),
    path('create/', views.add_review, name='create'),
]
