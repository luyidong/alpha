from django.contrib import admin

from posts.models import Category,Post,Comment,TaggedItem

class PostAdmin(admin.ModelAdmin):
    list_display = ["title","content","status","image","slug","tags"]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name","slug","enabled"]


admin.site.register(TaggedItem)

admin.site.register(Category,CategoryAdmin)
admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
