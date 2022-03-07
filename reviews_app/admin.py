from django.contrib import admin
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters, register
import requests

from .models import Review, User

from .utils import *


@register.inclusion_tag('reviews/submit_line.html', takes_context=True)
def custom_submit_row(context):
    """
    Displays the row of buttons for delete and save.
    """
    opts = context['opts']
    change = context['change']
    is_popup = context['is_popup']
    save_as = context['save_as']
    ctx = {
        'opts': opts,
        'show_delete_link': (
            not is_popup and context['has_delete_permission'] and
            change and context.get('show_delete', True)
        ),
        'show_save_as_new': not is_popup and change and save_as,
        'show_save_and_add_another': (
            context['has_add_permission'] and not is_popup and
            (not save_as or context['add'])
        ),
        'show_save_and_continue': not is_popup and context['has_change_permission'],
        'is_popup': is_popup,
        'show_save': True,
        'preserved_filters': context.get('preserved_filters'),
    }
    if context.get('original') is not None:
        ctx['original'] = context['original']
    return ctx


class ReviewAdmin(admin.ModelAdmin):
    change_form_template = 'reviews/admin_edit_review.html'

    def publish(self, obj):
        obj.is_published = True
        obj.save()
        r = requests.post(PUBLISH_ADDRESS, {
            "author": obj.author.id,
            "rating": obj.rate,
            "review": obj.text
        })

    def response_change(self, request, obj):
        opts = self.model._meta
        pk_value = obj._get_pk_val()
        preserved_filters = self.get_preserved_filters(request)

        if "_customaction" in request.POST:
            self.publish(obj)
            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({'preserved_filters': preserved_filters, 'opts': opts}, redirect_url)
            return HttpResponseRedirect(redirect_url)

        else:
            return super(ReviewAdmin, self).response_change(request, obj)

    fields = ['author', 'rate', 'text', 'pub_date', 'is_published']
    list_display = ['author', 'rate', 'text', 'pub_date', 'is_published']
    readonly_fields = ('is_published', )


admin.site.register(Review, ReviewAdmin)

admin.site.register(User)
