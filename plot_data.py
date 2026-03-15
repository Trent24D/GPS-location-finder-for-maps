import pandas as pd
import plotly.express as px

def parse_log_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or '|' not in line: continue  # skip empty lines
            parts = line.split('|')  # break line by the | (pipe)
            print(parts)
            try:  # sorry mr. keithley, im using try except to not crash on bad outputs just in case
                coords = parts[2].strip().split(',')
                lat, lon = float(coords[0].strip()), float(coords[1].strip())  # This is all based on current_location_pi.py output format, so adjust if you changed that format

                # checks
                if lat == 0 or lon == 0: continue  # skip invalid coords, but if you are traveling to the Gulf of Guinea or West Africa, remove this check
                if lat < -90 or lat > 90 or lon < -180 or lon > 180: continue  # skip out of bounds coords (this shouldn't happen naturally, but if there was a bad edit to cords, remove that data)
                if parts[0].strip() == " GPS: NO_FIX ": continue  # skip no fix lines
                
                data.append({
                    'Timestamp': parts[0].strip(),
                    'Latitude': lat,
                    'Longitude': lon,
                    'Coord_Label': f"{lat:.8f}, {lon:.8f}"  # round to 8 decimals
                    # 'Speed': parts[3].strip(),
                    # 'Heading': parts[5].strip(),
                    # 'Altitude': parts[4].strip(),
                    # ignoring speed, altitude, and heading as I am creating a 2D map, but if you create a 3D diagram throw them here as well
                })
            except: continue
    # create a dateframe object from the data list
    dataframe = pd.DataFrame(data)
    if not dataframe.empty:
        dataframe['Timestamp_DT'] = pd.to_datetime(dataframe['Timestamp'])  # convert to Timestamp type for pandas
        dataframe['Legend_Label'] = dataframe['Timestamp_DT'].dt.strftime('%H:%M:%S') + " | " + dataframe['Coord_Label']
        dataframe['Time_Unix'] = dataframe['Timestamp_DT'].astype('int64') // 10**9  # convert a unix timestamp for color scaling (since epoch)
        dataframe = dataframe.sort_values(by='Time_Unix') 
    return dataframe

dataframe = parse_log_file("gps_parsed.txt")

# change these to wherever you want your map to start, this is Port Hueneme, CA (testing at an FRC event)
home_lat = 34.151383
home_lon = -119.201874

fig = px.scatter_mapbox(
    dataframe,
    lat='Latitude',
    lon='Longitude',
    color='Legend_Label', 
    color_discrete_sequence=px.colors.sample_colorscale("Turbo", [i/(len(dataframe)-1) for i in range(len(dataframe))]),
    hover_name='Timestamp',
    height=900
)

for trace in fig.data:
    trace.update(
        marker=dict(size=12, opacity=0.9),
        showlegend=True
    )
    fig.add_trace(trace)

fig.update_layout(
    showlegend=True,
    legend= dict(
        title="Timestamp | Lat, Lon",
        orientation="v",
        bgcolor='rgba(255,255,255,0.5)'
    ),
    mapbox={
        'style': "white-bg",
        'center': {'lat': home_lat, 'lon': home_lon},  # when you double click, returns to the home location
        'zoom': 12,  # how far zoomed in on the map to home location (starts at 1 for all zoomed out)
        'layers': [
            {
                "below": 'traces',
                "sourcetype": "raster",
                "source": ["https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"],  # satellite map from ArcGIS, it's free!
            }
        ]
    },
    margin={"r":0,"t":40,"l":0,"b":0},
    uirevision='constant' 
)

fig.update_traces(marker=dict(size=12, opacity=0.9))

output_file = "map.html"  # output file is an .html from plotly.express

fig.write_html(
    output_file, 
    config={
        'scrollZoom': True,  # important to be able to zoom in and out
        'displayModeBar': True,
        'displaylogo': False,
    }
)

print(f"Map created. Starting at {home_lat}, {home_lon}")