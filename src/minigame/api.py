from typing import List

from django.shortcuts import render
import ninja

from minigame.models import EmojiHero
from minigame.schemas.emoji_hero import EmojiHeroSchemaOut

# Create your views here.

emoji_hero_router = ninja.Router(tags=['Emoji Hero'])


@emoji_hero_router.get('/', response=List[EmojiHeroSchemaOut])
def get_emoji_hero(request):
    return EmojiHero.objects.all()
