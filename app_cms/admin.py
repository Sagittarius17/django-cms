from django.contrib import admin
from .models import Article
# Register your models here.

# @admin.register(Article)
# class ArticleAdmin(admin.ModelAdmin):
#     list_display = ('title', 'published_date', 'updated_date')

admin.site.register(Article)