from django.contrib import admin
from unity.models import Subscriber
from django.template.response import TemplateResponse
from django.urls import path


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email', 'view_timestamp', 'status']
    ordering = ['-timestamp']
    @admin.display(empty_value='???')
    def view_timestamp(self, obj):
        return obj.timestamp_string

admin.site.register(Subscriber, SubscriberAdmin)