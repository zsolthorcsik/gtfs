import networkx as nx
import pickle
class Graph_Handler(object):
    """
    This class handles Graph objects from the feeds
    """

    def __init__(self) -> None:
        pass

    def create_simple_graph_from_feed(self, feed):        
        """
        Creates a simple feed Graph object from the feed.
        """
        G = nx.Graph()        
        my_trips_df = feed.trips
        for i, trip_row in my_trips_df.iterrows():
            trip_stops = feed.stop_times.loc[feed.stop_times['trip_id']==trip_row.trip_id].sort_values('departure_time', ascending=True)
            stop_count = 0
            for s, stop_row in trip_stops.iterrows():    
                if stop_count >= 1:
                    travel_time = trip_stops.iloc[[stop_count]]['arrival_time'].values[0] - trip_stops.iloc[[stop_count-1]]['departure_time'].values[0]
                    # TODO: Add more options for the edge creation
                    G.add_edge(trip_stops.iloc[[stop_count-1]]['stop_name'].values[0], trip_stops.iloc[[stop_count]]['stop_name'].values[0], weight=travel_time)
                stop_count += 1    
        return G
    

    def create_simple_graph_from_feed_stop_ids(self, feed):        
        """
        Creates a simple feed Graph object from the feed.
        """
        G = nx.Graph()        
        my_trips_df = feed.trips
        for i, trip_row in my_trips_df.iterrows():
            trip_stops = feed.stop_times.loc[feed.stop_times['trip_id']==trip_row.trip_id].sort_values('departure_time', ascending=True)
            stop_count = 0
            for s, stop_row in trip_stops.iterrows():    
                if stop_count >= 1:
                    travel_time = trip_stops.iloc[[stop_count]]['arrival_time'].values[0] - trip_stops.iloc[[stop_count-1]]['departure_time'].values[0]
                    # TODO: Add more options for the edge creation
                    G.add_edge(trip_stops.iloc[[stop_count-1]]['stop_id'].values[0], trip_stops.iloc[[stop_count]]['stop_id'].values[0], weight=travel_time)
                stop_count += 1    
        return G
    
    def read_graph(self, pickle_path):
        """
        Reads in networkx Graph from pickle
        """
        G = pickle.load(open(pickle_path,'rb' ))
        return G
