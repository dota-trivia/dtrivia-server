from django.contrib import admin
from django import forms
from emoji_picker.widgets import EmojiPickerTextInputAdmin

from minigame.models import MinigameConfig, EmojiHero

# Register your models here.
admin.site.register(MinigameConfig)
admin.site.register(EmojiHero)


class EmojiHeroForm(forms.ModelForm):
    emojis = forms.CharField(widget=EmojiPickerTextInputAdmin)
