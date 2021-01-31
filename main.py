from gps_class import GPSVis

vis = GPSVis(data_path='data.csv',
             map_path='map.png',  # Path to map downloaded from the OSM.
             points=(45.8357, 15.9645, 45.6806, 16.1557)) # Two coordinates of the map (upper left, lower right)

vis.create_image(color=(0, 0, 255), width=3)  # Set the color and the width of the GNSS tracks.
vis.plot_map(output='save')

print()
