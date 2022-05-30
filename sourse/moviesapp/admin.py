from django.contrib import admin

# Register your models here.
from django.utils.safestring import mark_safe
from django import forms

from .models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url", )
    list_display_links = ("name",)

class RevieInLines(admin.TabularInline):
    model = Reviews
    extra = 1

class MovieShotsInLine(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)
    fields = ("title", "shot","get_image" )
    def get_image(self, obj):
        return mark_safe(f'<img src = {obj.shot.url} with = "50" height = "60"')

    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category","url","draft" )
    list_display_links = ("title",)
    list_filter = ("category", "year")
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInLine,RevieInLines, ]
    save_on_top = True
    save_as = True
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    form = MovieAdminForm
    readonly_fields = ("get_image",)

    fieldsets = (
        ("Options", {
            "fields": ("url",)
        }),
        ("О фильме", {
            "fields": ("title", "tagline", "description","get_image","poster", "country", "category","genres"),

        }),
        ("Принимавние участие", {
            "fields": (("actors", "directors"),)
        }),
        ("Даты", {
            "fields": (("year", "world_premiere"),)
        }),
        ("Финансы", {
            "fields": (("budget","fees_in_usa","fees_in_world"),),

        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src = {obj.poster.url} with = "60"')

    get_image.short_description = "Изображение"


    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f"{row_update} записей обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f"{row_update} записей обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ("change",)
    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ("change",)

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id","name","movie")
    list_display_links = ("name",)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("id","name","url")
    list_display_links = ("name",)

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ("id","name","age","get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src = {obj.photo.url} with = "50" height = "60"')

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("id","ip","star", "movie")
    list_display_links = ("ip",)

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ("id","title","movie","get_image")
    list_display_links = ("title",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src = {obj.shot.url} with = "50" height = "60"')

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("id","value")
    list_display_links = ("value",)

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id","position")
    list_display_links = ("position",)


admin.site.site_title = "Movies"
admin.site.site_header = "Movies"