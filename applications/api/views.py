from django.db.models import Count, F, Sum

from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from applications.match.models import Match, Season, Delivery


class TokenView(ObtainAuthToken):
    """
    Views for get authenticated by token
    @:return: dict: token: int, user_id: int, email: str
    """

    def post(self, request):
        print(request.data, "request.data")
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class MostMatchWinnersView(APIView):
    """
    Views for find four teams which won the most number of matches
    @:param season: Optional
    @:return: dict: team_name: str, win_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        match_queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                match_queryset = match_queryset.filter(season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        most_match_winners = match_queryset.values('match_winner__name').annotate(
            win_count=Count('match_winner')).order_by('-win_count')[:4]
        winners = []
        for winner in most_match_winners:
            winners.append({"team_name": winner['match_winner__name'], "win_count": winner["win_count"]})
        return Response(winners)


class MostTossWinnerView(APIView):
    """
    Views for find a team won the most number of tosses in the season
    @:param season: Optional
    @:return: dict: team_name: str, toss_win_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        match_queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                match_queryset = match_queryset.filter(season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        most_toss_winner = match_queryset.values('toss_winner__name').annotate(
            toss_count=Count('toss_winner')).order_by('-toss_count')
        if most_toss_winner:
            most_toss_winner = most_toss_winner[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response(
            {'team_name': most_toss_winner['toss_winner__name'], 'toss_win_count': most_toss_winner['toss_count']})


class MostPlayerOfMatchWinnerView(APIView):
    """
    Views for find a player won the maximum number of Player of the Match awards in the whole season
    @:param season: Optional
    @:return: dict: player_name: str, player_of_the_match_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        match_queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
            match_queryset = match_queryset.filter(season=season)
        most_player_of_the_match = match_queryset.values('player_of_the_match__name').annotate(
            count=Count('player_of_the_match')).order_by('-count')
        if most_player_of_the_match:
            most_player_of_the_match = most_player_of_the_match[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response({'player_name': most_player_of_the_match['player_of_the_match__name'],
                         'player_of_the_match_count': most_player_of_the_match['count']})


class MaximumMatchWinnerView(APIView):
    """
     Views for find a team won maximum number of matches in the whole season
     @:return:  dict: team_name: str, match_win_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        maximum_match_winner = Match.objects.values('match_winner__name').annotate(
            win_count=Count('match_winner')).order_by('-win_count')
        if maximum_match_winner:
            maximum_match_winner = maximum_match_winner[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response(
            {'team_name': maximum_match_winner['match_winner__name'],
             'match_win_count': maximum_match_winner['win_count']})


class TossWonBatSelectedTeamView(APIView):
    """
    Views for find percentage of teams decided to bat when they won the toss
    @:return: dict: toss_won_and_bat_selected_percentage: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        toss_bat_selected_count = Match.objects.filter(toss_decision=Match.BAT).count()
        total_match = Match.objects.all().count()
        bat_percentage = round((toss_bat_selected_count / total_match) * 100)
        return Response({'toss_won_and_bat_selected_percentage': bat_percentage})


class LocationHostedMostMatchView(APIView):
    """
    Views for find location hosted most number of matches
    @:param season: Optional
    @:return: dict: venue: str, match_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                queryset = queryset.filter(season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        location_hosted_most_match = queryset.values('venue__name').annotate(match_count=Count('venue')).order_by(
            '-match_count')
        if location_hosted_most_match:
            location_hosted_most_match = location_hosted_most_match[0]
        return Response({'venue': location_hosted_most_match["venue__name"],
                         "match_count": location_hosted_most_match["match_count"]})


class TeamWonHighestMarginView(APIView):
    """
    Views for find team won by highest runs
    @:param season: Optional
    @:return: dict: high_run_margin_winner: str, win_by_runs: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                queryset = queryset.filter(season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        team_won_highest_margin_run = queryset.values('win_by_runs', 'match_winner__name').order_by('-win_by_runs')
        if team_won_highest_margin_run:
            team_won_highest_margin_run = team_won_highest_margin_run[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response({'high_run_margin_winner': team_won_highest_margin_run})


class TeamWonByHighestWicketView(APIView):
    """
    Views for find team won by highest wickets
    @:param season: Optional
    @:return: dict: high_wicket_margin_winner: str, win_by_wickets: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                queryset = queryset.filter(season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        team_won_by_highest_wicket = queryset.values('win_by_wickets', 'match_winner__name').order_by('-win_by_wickets')
        if team_won_by_highest_wicket:
            team_won_by_highest_wicket = team_won_by_highest_wicket[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response({'high_wicket_margin_winner': team_won_by_highest_wicket})


class TeamWonTossAndMatchView(APIView):
    """
    Views for find how many times has a team won the toss and the match
    @:return: dict: team_name: str, win_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Match.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                queryset = queryset.filter(season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        toss_and_match_won_count = queryset.filter(match_winner=F('toss_winner'))
        result = toss_and_match_won_count.values('match_winner__name').annotate(
            win_count=Count('match_winner')).order_by('-win_count')
        return Response(result)


class MostCatchesByFielderView(APIView):
    """
    Views for find most catches by a fielder
    @:param season: Optional
    @:return: dict: fielder__name: str, match: int, catch_count: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Delivery.objects.filter(dismissal_kind='caught')
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
                queryset = queryset.filter(match__season=season)
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
        most_catches_by_fielder = queryset.values('fielder__name', 'match').annotate(catch_count=Count('fielder')).order_by(
            '-catch_count')
        if most_catches_by_fielder:
            most_catches_by_fielder = most_catches_by_fielder[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response({'most_catches': most_catches_by_fielder})


class HighestRunOfTheSeasonView(APIView):
    """
    Views for find highest score by a player per match
    @:param season: Optional
    @:return: dict: high_score_batsman: str, match__id: int, total_runs: int
    """
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        queryset = Delivery.objects.all()
        if request.GET.get('season'):
            try:
                season = Season.objects.get(name=request.GET.get('season'))
            except:
                return Response({'status': "error", "message": "Invalid season"}, status=status.HTTP_400_BAD_REQUEST)
            queryset = queryset.filter(match__season=season)
        highest_run_scorer = queryset.values('batsman__name', 'match__id').annotate(
            total_runs=Sum('batsman_runs')).order_by('-total_runs')
        if highest_run_scorer:
            highest_run_scorer = highest_run_scorer[0]
        else:
            return Response({'status': "error", "message": "Data not found"})
        return Response({'high_score_batsman': highest_run_scorer})
