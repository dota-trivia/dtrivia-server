import requests
from django.core.management.base import BaseCommand, CommandError
from hero.models import Hero, HeroAttribute, HeroAttackType, HeroRole
from typing import Optional


class Command(BaseCommand):
    help = "Updates or creates heroes from the Dota 2 API"

    def add_arguments(self, parser):
        parser.add_argument(
            "--hero-id",
            type=int,
            help="The ID of a specific hero to update",
        )

    def upsert_hero(self, hero_id: Optional[int | None] = None, hero_data: Optional[dict | None] = None):
        if hero_id is None and hero_data is None:
            raise CommandError("You must provide either a hero ID or hero data")

        if hero_id:
            hero_data = requests.get(f"https://api.opendota.com/api/heroStats/{hero_id}").json()
            return self.upsert_hero(hero_data=hero_data)

        hero_attributes = {
            'agi': 'AGILITY',
            'int': 'INTELLIGENCE',
            'str': 'STRENGTH',
            'all': 'UNIVERSAL',
        }

        hero_data['primary_attr'] = HeroAttribute[hero_attributes[hero_data['primary_attr'].lower()]].value
        hero_data['attack_type'] = HeroAttackType[hero_data['attack_type'].upper()].value
        hero_data['roles'] = [HeroRole[role.upper()].value for role in hero_data['roles']]
        hero_data['img'] = hero_data['img'].replace('?', '')

        hero, _ = Hero.objects.update_or_create(
            dota_id=hero_data["id"],
            defaults={
                "name": hero_data["localized_name"],
                "dota_name": hero_data["name"],
                "primary_attr": hero_data["primary_attr"],
                "attack_type": hero_data["attack_type"],
                "roles": hero_data["roles"],
                "avatar_url": "https://api.opendota.com" + hero_data['img'],
            },
        )

        self.stdout.write(self.style.SUCCESS(f'Successfully upserted hero {hero_data["localized_name"]}'))

    def handle(self, *args, **options):
        hero_id = options["hero_id"]

        if hero_id:
            self.upsert_hero(hero_id=hero_id)
            return None

        heroes = requests.get("https://api.opendota.com/api/heroStats").json()

        for hero in heroes:
            self.upsert_hero(hero_data=hero)
