## IPL Data Processing App (Django and Django-Rest )

This is a Django-Rest app for performing GET operations on the IPL data.


### Project setup
Start a python virtual env:
```
Clone the repository
# navigate to the ipl directory
cd ipl

# create the virtual environment for ipl app
python3 -m venv apl-venv --no-site-packages

# activate the virtual environment
source ipl-venv/bin/activate
```

Install dependencies
```
python3 -m pip install -r requirments.txt
```
Migrate database
```
python manage.py migrate
```

Import ipl xls data using custom management command
```
python manage.py update_db
```



### List of Routes
| Request | Endpoint | Parameters | Details |
| --- | --- | --- | --- |
| `GET` | `/api/most-won-teams/`| season:int Optional, Header: Token Required | Get most won 4 teams, use season parameter for filter by a season |
| `GET` | `/api/most-toss-winner/`| season:int Optional, Header: Token Required | Get most toss won team, use season parameter for filter by a season |
| `GET` | `/api/most-player-of-the-match-winner`| season:int Optional, Header: Token Required | Get most player of the match award winner, use season parameter for filter by a season |
| `GET` | `/api/maximum-won-team`|  Header: Token Required | Get maximum matches won team |
| `GET` | `/api/toss-won-bat-selected-teams`|  Header: Token Required | Get percentage of teams decided to BAT first |
| `GET` | `/api/location-hosted-most-match`| season:int Optional, Header: Token Required | Get most hosted venue |
| `GET` | `/api/team-won-highest-margin-run`| season:int Optional, Header: Token Required | Get highest margin win by run |
| `GET` | `/api/team-won-by-highest-wicket-margin`| season:int Optional, Header: Token Required | Get highest wicket win |
| `GET` | `/api/team-won-toss-and-match`| season:int Optional, Header: Token Required | Get team which won toss and match |
| `GET` | `/api/high-score-player`| season:int Optional, Header: Token Required | Get a batsman who score highest run in a match  |
| `GET` | `/api/most-catches-by-a-fielder`| season:int Optional, Header: Token Required | Get a fielder with maximum catch in a match  |



### Start the application
```
python manage.py runserver

```

