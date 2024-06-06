from django.contrib import admin
from . models import Blog,Comment,Profile


class BlogAdmin(admin.ModelAdmin):
    list_display=('id','title','content','image','type')
    list_filter=['type']


class CommentAdmin(admin.ModelAdmin):
    list_display=('id','fk_blog','fk_user','comment' )
    list_filter=['fk_blog']


admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment,CommentAdmin)
admin.site.register(Profile)
