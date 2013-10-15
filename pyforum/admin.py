from django.contrib import admin

from pyforum.models import Forum, Thread, Post, User


class ForumAdmin(admin.ModelAdmin):
    """
    """
    pass

class ThreadAdmin(admin.ModelAdmin):
    """
    """
    pass

class PostAdmin(admin.ModelAdmin):
    """
    """
    pass

class UserAdmin(admin.ModelAdmin):
    """
    """
    pass

admin.site.register(Forum, ForumAdmin)
admin.site.register(Thread, ThreadAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(User, UserAdmin)
