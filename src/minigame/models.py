from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth import get_user_model

from utils.models import UserStampedModel, TimeStampedModel


class MinigameType(models.TextChoices):
    EMOJI = 'emoji'


class MatchDifficulty(models.TextChoices):
    EASY = 'easy'
    MEDIUM = 'medium'
    HARD = 'hard'


class MatchStatus(models.TextChoices):
    STARTED = 'started'


class MinigameConfig(TimeStampedModel, UserStampedModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    type = models.CharField(choices=MinigameType.choices, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class EmojiHero(TimeStampedModel, UserStampedModel):
    emoji = ArrayField(models.CharField(max_length=255))
    config = models.ForeignKey('minigame.MinigameConfig', on_delete=models.CASCADE)
    hero = models.ForeignKey('hero.Hero', on_delete=models.CASCADE)
    difficulty = models.CharField(choices=MatchDifficulty.choices, default=MatchDifficulty.EASY)

    def __str__(self):
        return self.config.name + ' - ' + self.hero.name
