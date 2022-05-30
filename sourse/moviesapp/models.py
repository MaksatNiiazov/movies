from django.db import models

# Create your models here.
from datetime import date, datetime
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Категория"""
    name = models.CharField(verbose_name='Категория', max_length=150)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    """Актеры и режисеры"""
    name = models.CharField(verbose_name='Имя', max_length=100)
    age = models.DateField(verbose_name='Возраст', null=True)
    date_of_death = models.DateField(verbose_name='Дата смерти', null=True, blank=True)
    description = models.TextField(verbose_name='Описание')
    position = models.ManyToManyField('Position', verbose_name='Должность')
    photo = models.ImageField(verbose_name='Фотография', upload_to='actors/')
    url = models.SlugField(max_length=160, unique=True, null=True)


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={"slug": self.url})

    def get_age(self):
        return date.today().year - self.age.year

    class Meta:
        verbose_name = 'Актеры и режисеры'
        verbose_name_plural = 'Актеры и режисеры'


class Genre(models.Model):
    """Жанры"""
    name = models.CharField(verbose_name='Жанр', max_length=100)
    description = models.TextField(verbose_name='Описание')
    url = models.SlugField(max_length=160, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Movie(models.Model):
    """Фильм"""
    title = models.CharField(verbose_name='Название', max_length=100)
    tagline = models.CharField(verbose_name='Слоган', max_length=200, default='')
    description = models.TextField(verbose_name='Описание')
    poster = models.ImageField(verbose_name='Постер', upload_to='movies/')
    year = models.PositiveSmallIntegerField(verbose_name='Дата выхода', default=0)
    country = models.CharField(verbose_name='Страна', max_length=50)
    directors = models.ManyToManyField('Actor', verbose_name='Режисер', related_name='film_director')
    actors = models.ManyToManyField('Actor', verbose_name='Актеры', related_name='film_actor')
    genres = models.ManyToManyField('Genre', verbose_name='Жанры')
    category = models.ForeignKey('Category', verbose_name='Категория', on_delete=models.SET_NULL, null=True)
    world_premiere = models.DateField(verbose_name='Премьера в мире', default=date.today)
    budget = models.PositiveIntegerField(verbose_name='Бюджет', default=0, help_text='Суммму указывать в долларах')
    fees_in_usa = models.PositiveIntegerField(
        verbose_name='Сборы в США', default=0, help_text='Суммму указывать в долларах'
    )
    fees_in_world = models.PositiveIntegerField(
        verbose_name='Сборы в мире', default=0, help_text='Суммму указывать в долларах'
    )
    url = models.SlugField(max_length=160, unique=True)
    draft = models.BooleanField(verbose_name='Черновик', default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    def get_review(self):
        return self.reviews_set.filter(parent__isnull=True)

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'


class MovieShots(models.Model):
    title = models.CharField(verbose_name='Кадры', max_length=100)
    description = models.TextField(verbose_name='Описание')
    shot = models.ImageField(verbose_name='Кадр', upload_to='movies_shots/')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name='Фильм')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кадр'
        verbose_name_plural = 'Кадры'


class RatingStar(models.Model):
    """Звезды рейтинга"""
    value = models.SmallIntegerField(default=0, verbose_name='Звезда рейтинга')

    def __str__(self):
        return f'{self.value}'

    class Meta:
        verbose_name = 'Звезда рейтинга'
        verbose_name_plural = 'Звезды рейтинга'
        ordering = ["-value"]


class Rating(models.Model):
    """Отценка пользователя"""
    ip = models.CharField(verbose_name='Айпи адрес', max_length=50)
    star = models.ForeignKey('RatingStar', on_delete=models.CASCADE, verbose_name='Звезда')
    movie = models.ForeignKey('Movie', on_delete=models.CASCADE, verbose_name='Фильм')

    def get_avg(self, mov):
        a = Rating.objects.filter(movie=mov).values("star")


        print(a[0:])


    def __str__(self):
        return f"{self.movie}: {self.star}"


    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'

class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True
    )
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.movie}"

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"


class Position(models.Model):
    """Должность"""
    position = models.CharField(max_length=200, verbose_name='Должность')

    def __str__(self):
        return f"{self.position}"

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
