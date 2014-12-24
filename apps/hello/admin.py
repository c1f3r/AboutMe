from django.contrib import admin

from apps.hello.models import AboutUser, HttpRequestLog, Event

# Register your models here.


class AboutUserAdmin(admin.ModelAdmin):
    model = AboutUser
    list_display = (
        'username', 'first_name', 'last_name', 'birth_date', 'email'
    )


class HttpRequestLogAdmin(admin.ModelAdmin):
    model = HttpRequestLog
    list_display = ('priority', 'user', 'host', 'path', 'method', 'date_time')


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ['model', 'action', 'time']
    search_fields = ['model']

admin.site.register(AboutUser, AboutUserAdmin)
admin.site.register(HttpRequestLog, HttpRequestLogAdmin)
admin.site.register(Event, EventAdmin)
