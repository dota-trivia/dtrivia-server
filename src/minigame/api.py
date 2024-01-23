from typing import List

from django.shortcuts import render, get_object_or_404
import ninja

from hero.models import Hero
from minigame.models import EmojiHero, MatchDifficulty, MinigameType, Match, MatchAttempt
from minigame.schemas.emoji_hero import EmojiHeroSchemaOut
from minigame.schemas.match import MatchStartSchemaIn, MatchSchemaOut, MatchAttemptSchemaIn

router = ninja.Router(tags=['Minigame'])


def start_emoji_hero(request, difficulty: MatchDifficulty):
    emoji_hero = EmojiHero.objects.filter(difficulty=difficulty).order_by('?').first()

    attempts_config = {}

    match difficulty:
        case MatchDifficulty.EASY:
            attempts_config['attempt_count'] = 5
            attempts_config['attempt_time'] = 180
            attempts_config['attempt_score'] = 100
        case MatchDifficulty.MEDIUM:
            attempts_config['attempt_count'] = 4
            attempts_config['attempt_time'] = 120
            attempts_config['attempt_score'] = 150
        case MatchDifficulty.HARD:
            attempts_config['attempt_count'] = 3
            attempts_config['attempt_time'] = 60
            attempts_config['attempt_score'] = 200

    game_match = Match.objects.create(
        difficulty=difficulty,
        type=MinigameType.EMOJI,
        minigame=emoji_hero.id,
        created_by=request.user,
        updated_by=request.user,
        **attempts_config
    )

    return game_match


@router.post('/start', response=MatchSchemaOut)
def get_emoji_hero(request, payload: MatchStartSchemaIn):
    if payload.minigame == MinigameType.EMOJI:
        return start_emoji_hero(request, payload.difficulty)

@router.post('/{match_id}/attempt', response=MatchSchemaOut)
def attempt_emoji_hero(request, match_id: int, payload: MatchAttemptSchemaIn):
    match = get_object_or_404(Match, id=match_id)

    hero = get_object_or_404(Hero, id=payload.hero)

    MatchAttempt.objects.create(
        hero=hero,
        created_by=request.user,
    )

    minigame = None

    if match.type == MinigameType.EMOJI:
        minigame = get_object_or_404(EmojiHero, id=match.minigame)

    if hasattr(minigame, 'hero') and payload.hero == minigame.hero.id:
        score = (match.attempt_score / match.attempt_count) * max(match.attempt_count - match.attempts.count(), 0)
        match.score = score
    else:
        match.score = 0

    match.save()

    return match

