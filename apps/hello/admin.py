from django.contrib import admin

from models import AboutUser, HttpRequestLog

# Register your models here.


class AboutUserAdmin(admin.ModelAdmin):
    model = AboutUser
    list_display = ('username', 'first_name', 'last_name', 'birth_date', 'email')


class HttpRequestLogAdmin(admin.ModelAdmin):
    model = HttpRequestLog
    list_display = ('user', 'host', 'path', 'method', 'date_time')

admin.site.register(AboutUser, AboutUserAdmin)
admin.site.register(HttpRequestLog, HttpRequestLogAdmin)
