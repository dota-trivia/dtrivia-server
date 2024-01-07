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


class MatchAttempt(TimeStampedModel, UserStampedModel):
    hero = models.ForeignKey('hero.Hero', on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='%(class)s_created')


class Match(TimeStampedModel, UserStampedModel):
    status = models.CharField(choices=MatchStatus.choices, default=MatchStatus.STARTED)
    difficulty = models.CharField(choices=MatchDifficulty.choices, default=MatchDifficulty.EASY)
    type = models.CharField(choices=MinigameType.choices)
    minigame_id = models.IntegerField()
    score = models.IntegerField(default=0)
    attempts = models.ManyToManyField(MatchAttempt)
    attempt_count = models.IntegerField(default=5, help_text='Maximum number of attempts allowed per match')
    attempt_time = models.IntegerField(default=180, help_text='Maximum time allowed per match')
    attempt_score = models.IntegerField(default=100, help_text='Match max score')


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
    emojis = ArrayField(models.CharField(max_length=255))
    config = models.ForeignKey('minigame.MinigameConfig', on_delete=models.CASCADE)
    hero = models.ForeignKey('hero.Hero', on_delete=models.CASCADE)

    def __str__(self):
        return self.config.name + ' - ' + self.hero.name
