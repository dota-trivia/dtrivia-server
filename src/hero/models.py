import requests
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db import models

from utils.fields import ChoiceArrayField


class HeroAttribute(models.TextChoices):
    STRENGTH = 'strength'
    AGILITY = 'agility'
    INTELLIGENCE = 'intelligence'
    UNIVERSAL = 'universal'


class HeroAttackType(models.TextChoices):
    MELEE = 'melee'
    RANGED = 'ranged'


class HeroRole(models.TextChoices):
    CARRY = 'carry'
    DISABLER = 'disabler'
    DURABLE = 'durable'
    ESCAPE = 'escape'
    INITIATOR = 'initiator'
    JUNGLER = 'jungler'
    NUKER = 'nuker'
    PUSHER = 'pusher'
    SUPPORT = 'support'


class Hero(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    hype = models.TextField(null=True, blank=True)

    primary_attr = models.CharField(choices=HeroAttribute.choices)
    attack_type = models.CharField(choices=HeroAttackType.choices)
    roles = ChoiceArrayField(models.CharField(choices=HeroRole.choices))
    avatar = models.ImageField(
        upload_to='media/heroes/avatars/',
        null=True,
        blank=True,
    )
    avatar_url = models.URLField(null=True, blank=True)

    dota_name = models.CharField(max_length=255)
    dota_id = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Heroes"
        verbose_name = "Hero"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        super().save(force_insert, force_update, using, update_fields)

        if (force_insert and self.avatar_url) or (update_fields and "avatar_url" in update_fields):
            img_temp = NamedTemporaryFile()
            img_temp.write(requests.get(self.avatar_url).content)
            img_temp.flush()

            self.avatar.save(f"{self.dota_name}.png", File(img_temp))
