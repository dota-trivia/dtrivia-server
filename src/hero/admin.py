from django.contrib import admin

from hero.models import Hero


@admin.register(Hero)
class HeroAdmin(admin.ModelAdmin):
    list_display = ('name', 'primary_attr', 'attack_type', 'roles')
