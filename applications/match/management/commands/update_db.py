from django.core.management.base import BaseCommand

import pandas as pd
import numpy as np

from applications.match import models


class Command(BaseCommand):
    help = 'Import data from Deliveries.xlsx and IPL Matches.xlsx files'

    def handle(self, *args, **kwargs):
        loc = "/mnt/c/Users/savad.kunhippurayil/projects/matches.xlsx"
        delivery_file_loc = "/mnt/c/Users/savad.kunhippurayil/projects/deliveries.xlsx"

        # dbframe = pd.read_excel(loc, sheet_name='matches')
        # for dbframe in dbframe.itertuples():
        #     # print(dbframe)
        #     season, created = models.Season.objects.get_or_create(name=dbframe.Season)
        #     city, created = models.City.objects.get_or_create(name=dbframe.City)
        #     venue, created = models.Venue.objects.get_or_create(name=dbframe.Venue, city=city)
        #     team1, created = models.Team.objects.get_or_create(name=dbframe.Team1)
        #     team2, created = models.Team.objects.get_or_create(name=dbframe.Team2)
        #     umpire1, created = models.Umpire.objects.get_or_create(name=dbframe.Umpire1)
        #     umpire2, created = models.Umpire.objects.get_or_create(name=dbframe.Umpire2)
        #
        #     # player, created = models.Player.objects.get_or_create(first_name=dbframe.Playerofthematch.split(" ")[:1], last_name=dbframe.Playerofthematch.split(" ")[1:])
        #
        #     if dbframe.TossDecision == 'field':
        #         toss = models.Match.FIELD
        #     else:
        #         toss = models.Match.BAT
        #     if dbframe.Result == 'normal':
        #         result = models.Match.NORMAL
        #     elif dbframe.Result == 'tie':
        #         result = models.Match.TIE
        #     else:
        #         result = models.Match.NO_RESULT
        #     if not result == models.Match.NO_RESULT:
        #         winner = models.Team.objects.get(name=dbframe.Winner)
        #     else:
        #         winner = None
        #     if dbframe.DLApplied:
        #         dl_applied = True
        #     else:
        #         dl_applied = False
        #     try:
        #         match, created = models.Match.objects.get_or_create(season=season,
        #                                                             venue=venue,
        #                                                             match_date=dbframe.MatchDate,
        #                                                             match_id=dbframe.id,
        #                                                             team1=team1,
        #                                                             team2=team2,
        #                                                             toss_winner=models.Team.objects.get(name=dbframe.TossWinner),
        #                                                             toss_decision=toss,
        #                                                             result=result,
        #                                                             dl_applied=dl_applied,
        #                                                             match_winner=winner,
        #                                                             win_by_runs=dbframe.Winbyruns,
        #                                                             win_by_wickets=dbframe.Winbywickets,
        #                                                             umpire1=models.Umpire.objects.get(name=dbframe.Umpire1),
        #                                                             umpire2=models.Umpire.objects.get(name=dbframe.Umpire2),
        #                                                             )
        #     except:
        #         print(dbframe.id)
        #     # TODO: UPDATE PLAYER OF THE MATCH

        dbframe = pd.read_excel(delivery_file_loc, sheet_name='deliveries', na_filter=False)
        for dbframe in dbframe.itertuples():
            print(dbframe)

            match = models.Match.objects.get(match_id=dbframe.MatchId)
            if str(dbframe.Innings) == '1':
                innings = models.Delivery.FIRST
            else:
                innings = models.Delivery.SECOND
            batting_team = models.Team.objects.get(name=dbframe.BattingTeam)
            bowling_team = models.Team.objects.get(name=dbframe.BowlingTeam)

            batsman, created = models.Player.objects.get_or_create(name=dbframe.Batsman)
            non_striker, created = models.Player.objects.get_or_create(name=dbframe.NonStriker)
            bowler, created = models.Player.objects.get_or_create(name=dbframe.Bowler)

            if int(dbframe.IsSuperOver) == 1:
                is_super_over = True
            else:
                is_super_over = False

            if dbframe.PlayerDismissed:
                player_dismissed, created = models.Player.objects.get_or_create(name=dbframe.PlayerDismissed)
            else:
                player_dismissed = None

            if dbframe.Feilder:
                fielder, created = models.Player.objects.get_or_create(name=dbframe.Feilder)
            else:
                fielder = None

            delivery, created = models.Delivery.objects.get_or_create(match=match,
                                                                      innings=innings,
                                                                      batting_team=batting_team,
                                                                      bowling_team=bowling_team,
                                                                      over=dbframe.Over,
                                                                      ball=dbframe.Ball,
                                                                      batsman=batsman,
                                                                      non_striker=non_striker,
                                                                      bowler=bowler,
                                                                      is_super_over=is_super_over,
                                                                      wide_runs=dbframe.WideRuns,
                                                                      bye_runs=dbframe.ByeRuns,
                                                                      leg_bye_runs=dbframe.LegByeRuns,
                                                                      no_ball_runs=dbframe.NoBallRuns,
                                                                      penalty_runs=dbframe.PenaltyRuns,
                                                                      batsman_runs=dbframe.BatsmanRuns,
                                                                      extra_runs=dbframe.ExtraRuns,
                                                                      total_runs=dbframe.TotalRuns,
                                                                      player_dismissed=player_dismissed,
                                                                      dismissal_kind=dbframe.DismissalKind,
                                                                      fielder=fielder,
                                                                      )



        print("COMPLETED DELIVERY, STARTED PLAYER OF THE MATCH UPDATE")
        dbframe = pd.read_excel(loc, sheet_name='matches')
        for dbframe in dbframe.itertuples():
            print(dbframe)
            try:
                player = models.Player.objects.get(name=dbframe.Playerofthematch)
                player.player_of_the_match += 1
                player.save()
                match = models.Match.objects.get(match_id=dbframe.id)
                match.player_of_the_match = player
                match.save()
            except Exception as e:
                print(e)








