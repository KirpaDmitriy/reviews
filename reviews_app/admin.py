from django.contrib import admin

from .models import Review, User


class ReviewAdmin(admin.ModelAdmin):
    fields = ['author', 'rate', 'text', 'pub_date', 'is_published']
    list_display = ['author', 'rate', 'text', 'pub_date', 'is_published']
    readonly_fields = ('is_published', )


admin.site.register(Review, ReviewAdmin)

admin.site.register(User)
