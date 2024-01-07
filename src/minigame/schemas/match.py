from ninja import ModelSchema, Schema

from minigame.models import MinigameType


class MatchStartSchemaIn(ModelSchema):
    minigame = MinigameType
