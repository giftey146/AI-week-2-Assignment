from sklearn.cluster import KMeans
import pandas as pd
import numpy as np

# Load and preprocess data
data = pd.read_csv('CTA_Bus_Tracker.csv')
coordinates = data[['latitude', 'longitude']].values

# Determine optimal k using elbow method
inertias = []
for k in range(1, 15):
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(coordinates)
    inertias.append(kmeans.inertia_)

# Plot elbow curve to select k=8 as optimal cluster count

# Final clustering
kmeans = KMeans(n_clusters=8)
data['cluster'] = kmeans.fit_predict(coordinates)

# Visualize clusters on map
import folium
map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightblue', 'pink']

for idx, row in data.iterrows():
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=5,
        color=colors[row['cluster']],
        fill=True
    ).add_to(map)
# Convert timestamps to cyclical features
data['hour_sin'] = np.sin(2*np.pi*data['hour']/24)
data['hour_cos'] = np.cos(2*np.pi*data['hour']/24)

# Time-aware clustering
time_features = data[['latitude', 'longitude', 'hour_sin', 'hour_cos', 'passenger_count']]
kmeans_time = KMeans(n_clusters=12)
data['time_cluster'] = kmeans_time.fit_predict(time_features)