from django.contrib import admin
from django.utils.html import mark_safe

from django import forms
from .models import *

# Register your models here.

from ckeditor_uploader.widgets import CKEditorUploadingWidget

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'year',)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'url',)

class ReviewsInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('name', 'email')

class MovieShotsInline(admin.StackedInline):
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="15%" height="auto" >')
    get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category',)
    search_fields = ('title', 'category__name',)
    inlines = [MovieShotsInline, ReviewsInline]
    save_on_top = True
    save_as = True
    list_editable = ('draft',)
    form = MovieAdminForm
    readonly_fields = ('get_image',)
    actions = ('unpublish', 'publish',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="15%" height="auto" >')
    get_image.short_description = 'Изображение'

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == '1':
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обнавлено'
        self.message_user(request, message_bit)

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == '1':
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обнавлено'
        self.message_user(request, message_bit)

@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="15%" height="auto" >')
    get_image.short_description = 'Изображение'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'ip')

admin.site.register(RatingStar)
admin.site.site_title = 'Admin'
admin.site.site_header = 'Admin'