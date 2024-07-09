from django.shortcuts import render
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from rest_framework import status

from .models import Movie, CustomUser
from .serializers import MovieSerializer, ActorSerializer, MovieListSerializer, MovieDetailSerializer, \
    CommentSerializer, MovieCrawlSerializer


# Create your views here.
class InitDB(APIView):
    def get(self, request):
        image_base_url = "https://image.tmdb.org/t/p/original"

        movies = []
        for i in range(1, 26):
            url = f"https://api.themoviedb.org/3/discover/movie?include_adult=false&include_video=false&language=en-US&page={i}&sort_by=popularity.desc"

            headers = {
                "accept": "application/json",
                "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJmN2YyOWQ3MWMxMDVhMjM3Y2ExYjJmYjY4NmI4NWFiZiIsIm5iZiI6MTcyMDQzMzEwNC4xMzYxMTgsInN1YiI6IjY2ODdlM2E2ZmNhNGUwNzI0ZjllYjg5MyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.53BFdaP-qxhicUASIOuQmjFMCioGM379jw6MRwkXl7U"
            }

            response = requests.get(url, headers=headers)
            jsonData = response.json()['results']
            for result in jsonData:
                movies.append(result['id'])

        print("got all movie ids")

        i = 0
        for movie_id in movies:
            url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=ko"

            actor_response = requests.get(url, headers=headers)
            jsonData = actor_response.json()
            genres = ', '.join([genres['name'] for genres in jsonData['genres']])
            poster_url = image_base_url+jsonData['poster_path']


            credits_url = f"https://api.themoviedb.org/3/movie/{movie_id}/credits?language=ko"
            credits_response = requests.get(credits_url, headers=headers)
            credits_jsonData = credits_response.json()

            if len(credits_jsonData['crew']) == 0:
                continue
            else:
                director = credits_jsonData['crew'][0]
                director_image_url = None
                if director['profile_path']:
                    director_image_url = image_base_url+director['profile_path']

                movie_data = {
                    'title_kor': jsonData['title'],
                    'title_eng': jsonData['original_title'],
                    'poster_url': poster_url,
                    'genre': genres,
                    'showtime': jsonData['runtime'],
                    'release_date': jsonData['release_date'],
                    'plot': jsonData['overview'],
                    'rating': jsonData['vote_average'],
                    'director_name': director['name'] if director else None,
                    'director_image_url': director_image_url
                }
                serializer = MovieSerializer(data=movie_data)
                serializer.is_valid(raise_exception=True)
                movie = serializer.save()

                actors = credits_jsonData['cast'][:8]
                for actor in actors:
                    actor_image_url = None
                    if actor['profile_path']:
                        actor_image_url = image_base_url+actor['profile_path']

                    actor_data = {
                        'movie' : movie.id,
                        'name' : actor['name'],
                        'character' : actor['character'],
                        'image_url' : actor_image_url
                    }
                    serializer = ActorSerializer(data=actor_data)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
            i += 1
            print(i/len(movies)*100, "% DONE")

        return Response({"status": "Database initialized"}, status=status.HTTP_200_OK)

class MovieCrawlView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        response = MovieCrawlSerializer(movies, many=True).data
        return Response(response, status=status.HTTP_200_OK)

class MovieListView(APIView):
    def get(self, request):
        movies = Movie.objects.all()
        response = MovieListSerializer(movies, many=True).data
        return Response(response, status=status.HTTP_200_OK)

class MovieDetailView(APIView):
    def get(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        response = MovieDetailSerializer(movie).data
        return Response(response, status=status.HTTP_200_OK)
    def post(self, request, movie_id):
        movie = Movie.objects.get(pk=movie_id)
        user = CustomUser.objects.get(pk=1)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie, user=user)
        return Response({"msg": "댓글 생성 완료"}, status=status.HTTP_201_CREATED)

