import gtfs_functions as gtfs
import geopandas as gpd
import pandas as pd
import networkx as nx

class Feed_Handler(object):
    
    feed = None

    def __init__(self, input_file):
        self.feed = gtfs.Feed(gtfs_path=input_file)

    def get_connected_stops(self, start_station_name):                
        # Find trips that serve the start station
        start_trips = self.feed.stop_times.loc[self.feed.stop_times['stop_name'] == start_station_name, 'trip_id'].unique()        
        # Find all stations served by these trips
        connected_stations = self.feed.stop_times.loc[self.feed.stop_times['trip_id'].isin(start_trips), 'stop_name'].unique()        
        # Remove the start station from the list of connected stations
        connected_stations = list(set(connected_stations) - set([start_station_name]))
        return connected_stations

    def get_number_of_connections_between_stations(self, start_station_name, end_station_name):
        my_stops = self.feed.stop_times.loc[self.feed.stop_times['trip_id'].isin(self.feed.trips)].stop_name.value_counts().rename_axis('stop_name').reset_index(name='connections')
        res_df = pd.merge(my_stops, self.feed.stops[["stop_name", 'geometry', 'stop_lat', 'stop_lon']], on='stop_name')
        return res_df
    
    def get_travel_time(self, start_station, end_station, calculate_type='min'):
        my_trips = self.feed.stop_times.loc[self.feed.stop_times.stop_name==start_station].trip_id.unique()
        start_df = self.feed.stop_times.loc[(self.feed.stop_times.trip_id.isin(my_trips))&(self.feed.stop_times.stop_name.str.contains(start_station))][['trip_id', 'departure_time']]
        end_df = self.feed.stop_times.loc[(self.feed.stop_times.trip_id.isin(my_trips)&(self.feed.stop_times.stop_name.str.contains(end_station)))][['trip_id', 'arrival_time']]
        merged_df = pd.merge(start_df, end_df, on='trip_id')
        merged_df['travel_time'] = merged_df['arrival_time'] - merged_df['departure_time']    
        merged_df = merged_df.loc[merged_df['travel_time']>0]
        if len(merged_df):
            if calculate_type=='min':
                return min(merged_df['travel_time']) / 60
            if calculate_type=='mean':
                return (merged_df['travel_time'].mean()) / 60
            if calculate_type=='max':
                return (merged_df['travel_time'].max()) / 60
            
    def get_travel_time_from_graph(self, G, start_station, end_station):
        try:
            path = nx.shortest_path(G, start_station, end_station, weight = 'weight')
            travel_time = nx.classes.path_weight(G, path=path, weight='weight')        
            return travel_time
        except Exception as e:
            print('No success with station: %s' % end_station)
            print(e)

    def get_stop_name_from_id(self, station_id):                
        res = self.feed.stops.query("stop_id=='{}'".format(station_id))
        if len(res):
            return res.iloc[0]['stop_name']

    