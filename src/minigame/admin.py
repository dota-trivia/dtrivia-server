from django.contrib import admin
from django import forms

from minigame.models import MinigameConfig, EmojiHero, MatchAttempt, Match

# Register your models here.
admin.site.register(MinigameConfig)
admin.site.register(EmojiHero)
admin.site.register(Match)
admin.site.register(MatchAttempt)
