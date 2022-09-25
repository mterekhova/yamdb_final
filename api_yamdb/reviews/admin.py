from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, TitleGenres


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category', 'description')
    list_display_links = ('name',)
    search_fields = ('name', 'year', 'category', 'genre')


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('name',)
    search_fields = ('name',)


class TitleGenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre')
    list_display_links = ('title',)
    search_fields = ('title',)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'title', 'author', 'score')
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('title', 'author', 'score',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'review', 'author', 'pub_date')
    list_display_links = ('text',)
    search_fields = ('text',)
    list_filter = ('review', 'author',)


admin.site.register(Title, TitleAdmin)
admin.site.register(TitleGenres, TitleGenreAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
