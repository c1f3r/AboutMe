from django.contrib import admin
from apps.hello.models import AboutUser
# Register your models here.


class AboutUserAdmin(admin.ModelAdmin):
    model = AboutUser
    list_display = ('username', 'first_name', 'last_name', 'birth_date', 'email')


admin.site.register(AboutUser, AboutUserAdmin)