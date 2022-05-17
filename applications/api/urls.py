from django.urls import path

from applications.api import views


urlpatterns = [
    path('token', views.TokenView.as_view(), name='token'),
    path('most-toss-winner', views.MostTossWinnerView.as_view(), name='most-toss-winner'),
    path('most-player-of-the-match-winner', views.MostPlayerOfMatchWinnerView.as_view(),
         name='most-player-of-the-match-winner'),
    path('most-won-teams', views.MostMatchWinnersView.as_view(), name='most-won-teams'),
    path('maximum-won-team', views.MaximumMatchWinnerView.as_view(), name='maximum-won-team'),
    path('toss-won-bat-selected-teams', views.TossWonBatSelectedTeamView.as_view(), name='toss-won-bat-selected-teams'),
    path('location-hosted-most-match', views.LocationHostedMostMatchView.as_view(), name='location-hosted-most-match'),
    path('team-won-highest-margin-run', views.TeamWonHighestMarginView.as_view(), name='team-won-highest-margin-run'),
    path('team-won-by-highest-wicket-margin', views.TeamWonByHighestWicketView.as_view(),
         name='team-won-by-highest-wicket-margin'),
    path('team-won-toss-and-match', views.TeamWonTossAndMatchView.as_view(),
         name='team-won-toss-and-match'),
    path('most-catches-by-a-fielder', views.MostCatchesByFielderView.as_view(), name='most-catches-by-a-fielder'),
    path('high-score-player', views.HighestRunOfTheSeasonView.as_view(), name='high-score-player'),
]



