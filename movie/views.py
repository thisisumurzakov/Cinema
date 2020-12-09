from django.db.models import Q
from django.shortcuts import redirect

# Create your views here.
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, Actor, Genre
from .forms import ReviewForm

class GenreYear:
    def get_genre(self):
        return Genre.objects.all()
    def get_year(self):
        return Movie.objects.filter(draft=False).values('year').distinct()

class MovieView(GenreYear, ListView):
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    paginate_by = 1

    '''def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args,**kwargs)
        context['cotegories'] = Category.objects.all()
        return context'''

class MovieDetailView(GenreYear, DetailView):
    model = Movie
    slug_field = 'url'

class AddReview(View):
    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())

class ActorView(GenreYear, DetailView):
    model = Actor
    template_name = 'movie/actor.html'
    slug_field = 'name'

class FilterMoviesView(GenreYear, ListView):
    paginate_by = 1
    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist('year')) |
            Q(genre__in=self.request.GET.getlist('genre'))
        )
        return queryset
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['genre'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('genre')])
        context['year'] = ''.join([f'year={x}&' for x in self.request.GET.getlist('year')])
        return context

class Search(GenreYear, ListView):
    paginate_by = 2
    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('search'))
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search']= f"search={self.request.GET.get('search')}&"
        return context