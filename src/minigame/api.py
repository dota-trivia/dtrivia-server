from typing import List

from django.shortcuts import render
import ninja

from minigame.models import EmojiHero
from minigame.schemas.emoji_hero import EmojiHeroSchemaOut

router = ninja.Router(tags=['Match'])


@router.post('/', response=List[EmojiHeroSchemaOut])
def get_emoji_hero(request):
    return EmojiHero.objects.all()
