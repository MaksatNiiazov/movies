from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import *
from .forms import ReviewForm, RatingForm

class GenreYear:

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYear,ListView):
    """Список Фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1
    template_name = 'movies/movie_list.html'


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = "url"
    template_name = 'movies/movie_detail.html'
    queryset = Movie.objects.filter(draft=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()

        return context

    def get_user_stars(self, ip, movie_id):
        if Rating.objects.filter(ip=ip, movie_id=movie_id).exists():
            stars = Rating.objects.get(ip=ip, movie_id=movie_id).star
        else:
            stars = None
        return stars


class ActorView(DetailView):
    model = Actor
    slug_field = "url"
    template_name = 'movies/actor_detail.html'


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())



class FilterMovieView(GenreYear,ListView):
    template_name = 'movies/movie_list.html'
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))).distinct()

        return queryset
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        context['genre'] = ''.join([f'genre={x}&' for x in self.request.GET.getlist('genre')])
        return context



class AddStarRating(View):

    def get_client_ip(self, request):
        Rating.get_avg(self, int(request.POST.get("movie")))
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


    def post(self, request):

        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(ststus=201)
        else:
            return HttpResponse(ststus=400)


class Search(ListView):
    template_name = 'movies/movie_list.html'
    paginate_by = 1

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        print(context)
        return context