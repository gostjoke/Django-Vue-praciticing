from django.contrib import admin
from article.models import Article, Category, Tag

@admin.register(Article)
class ArticleModelAdmin(admin.ModelAdmin):
    # Use __all__ to display all fields of the model in the list view
    model = Article
    list_display = ["author", "title","body", "created", "updated", "category", "display_tags"]
    filter_horizontal = ('tags',)

    # 自定义方法，用于显示文章的标签
    def display_tags(self, obj):
        return ", ".join(tag.text for tag in obj.tags.all())
    display_tags.short_description = "Tags"


@admin.register(Category)
class TagModelAdmin(admin.ModelAdmin):
    # Use __all__ to display all fields of the model in the list view
    list_display = ["title", "created"]

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    # Use __all__ to display all fields of the model in the list view
    list_display = ['text']

# admin.site.register(ArticleModelAdmin)
# admin.site.register(Category)
# admin.site.register(Tag)