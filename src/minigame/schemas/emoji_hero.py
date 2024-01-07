from ninja import ModelSchema

from minigame.models import EmojiHero


class EmojiHeroSchemaOut(ModelSchema):
    class Meta:
        model = EmojiHero
        fields = "__all__"
