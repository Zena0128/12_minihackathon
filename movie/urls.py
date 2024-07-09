from django.urls import  path
from .views import *

app_name = 'movie'

urlpatterns = [
    path('', MovieCrawlView.as_view()),
    path('list', MovieListView.as_view()),
    path('<int:movie_id>', MovieDetailView.as_view()),
    path('data', InitDB.as_view()),
]