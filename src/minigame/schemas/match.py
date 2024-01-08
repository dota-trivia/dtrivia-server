from typing import List

from ninja import ModelSchema, Schema

from minigame.models import MinigameType, MatchDifficulty, Match


class MatchStartSchemaIn(Schema):
    minigame: MinigameType
    difficulty: MatchDifficulty

class MatchSchemaOut(ModelSchema):
    class Meta:
        model = Match
        fields = "__all__"

class MatchAttemptSchemaIn(Schema):
    hero: int
