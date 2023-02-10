from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from django_extensions.db.fields import AutoSlugField

from utils.db import DateBaseModel


class Team(DateBaseModel):
    name = models.CharField(max_length=63)
    slug = AutoSlugField(populate_from='name', max_length=127, editable=True, unique=True)
    owner = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Player(DateBaseModel):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', max_length=255, editable=True, unique=True)
    profile_image = models.ImageField(max_length=255, blank=True, null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, null=True, blank=True)
    player_of_the_match = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name}"


class Umpire(DateBaseModel):
    name = models.CharField(max_length=127)
    slug = AutoSlugField(populate_from='name', max_length=255, editable=True, unique=True)

    def __str__(self):
        return f"{self.name}"


class Season(DateBaseModel):
    name = models.CharField(max_length=63)
    champion = models.ForeignKey(Team, null=True, blank=True, on_delete=models.RESTRICT, related_name='champion')
    runner_up = models.ForeignKey(Team, null=True, blank=True, on_delete=models.RESTRICT, related_name='runner_up')

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Venue(models.Model):
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Match(DateBaseModel):
    NORMAL = 'n'
    TIE = 't'
    NO_RESULT = 'nr'
    BAT = 'b'
    FIELD = 'f'
    TOSS_DECISIONS = (
        (BAT, 'Bat'),
        (FIELD, 'Field'),
    )
    RESULT_TYPES = (
        (NORMAL, "Normal"),
        (TIE, "Tie"),
        (NO_RESULT, "No Result")
    )
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    match_date = models.DateField()
    match_id = models.IntegerField(unique=True)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team1')
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team2')
    toss_winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='toss_winner')
    toss_decision = models.CharField(choices=TOSS_DECISIONS, max_length=1)
    result = models.CharField(choices=RESULT_TYPES, max_length=2)
    dl_applied = models.BooleanField(default=False)
    match_winner = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_winner', null=True, blank=True)
    win_by_runs = models.IntegerField(default=0)
    win_by_wickets = models.IntegerField(default=0)
    player_of_the_match = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='get_match', null=True, blank=True)
    umpire1 = models.ForeignKey(Umpire, on_delete=models.CASCADE, related_name='umpire1')
    umpire2 = models.ForeignKey(Umpire, on_delete=models.CASCADE, related_name='umpire2')

    def __str__(self):
        return f"{self.team1.name} x {self.team2.name} >> {self.season.name}"


class Delivery(DateBaseModel):
    FIRST = '1'
    SECOND = '2'
    INNINGS_TYPES = (
        (FIRST, '1'),
        (SECOND, '2')
    )
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    innings = models.CharField(choices=INNINGS_TYPES, max_length=1)
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_team')
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_team')
    over = models.IntegerField(validators=[MaxValueValidator(20), MinValueValidator(1)])
    ball = models.IntegerField(validators=[MinValueValidator(1)])
    batsman = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='batsman')
    non_striker = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='non_striker')
    bowler = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bowler')
    is_super_over = models.BooleanField(default=False)
    wide_runs = models.IntegerField(default=0)
    bye_runs = models.IntegerField(default=0)
    leg_bye_runs = models.IntegerField(default=0)
    no_ball_runs = models.IntegerField(default=0)
    penalty_runs = models.IntegerField(default=0)
    batsman_runs = models.IntegerField(default=0)
    extra_runs = models.IntegerField(default=0)
    total_runs = models.IntegerField(default=0)
    player_dismissed = models.ForeignKey(Player, related_name='player_dismissed', on_delete=models.CASCADE, null=True, blank=True)
    dismissal_kind = models.CharField(max_length=127, null=True, blank=True)
    fielder = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fielder', null=True, blank=True)

    def __str__(self):
        return f"{self.match} > {self.innings} > {self.over}.{self.ball}"
