import requests
import plotly.express as px
import config

def getDayOfYear(str):
    date = str[5:10]
    mon = date[0:2]
    day = date[3:5]
    return int(mon)*12 + int(day)

auth_url = "https://www.strava.com/oauth/token"

payload = {
    'client_id': config.client_id,
    'client_secret': config.client_secret,
    'refresh_token': config.refresh_token,
    'grant_type': "refresh_token",
    'f': 'json'
}

print("requesting...")
res = requests.post(auth_url, data=payload, verify=False)
access_token = res.json()['access_token']

print("getting activities...")
activities_url = "https://www.strava.com/api/v3/athlete/activities"
header = {'Authorization': 'Bearer ' + access_token}
param = {'per_page': 200, 'page': 1}
my_dataset = requests.get(activities_url, headers=header, params=param).json()

x = []
y = []
time = []
date = []
#achieve = []
for i in range(len(my_dataset)):
    x.append(my_dataset[i]["distance"])
    y.append(my_dataset[i]["total_elevation_gain"])
    time.append(my_dataset[i]["moving_time"])
    date.append(getDayOfYear(my_dataset[i]["start_date"]))
    #achieve.append(my_dataset[i]["achievement_count"])
fig = px.scatter(x=x, y=y, size=time, color=date, size_max=35)
fig.update_layout(
    xaxis_title="distance (m)",
    yaxis_title="elevation gain (m)"
)
fig.update_layout(legend_title_text='Trend')
fig.show()
