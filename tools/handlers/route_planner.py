import networkx as nx


class Route_Planner(object):
    """
    Object to handle routing, get shortest paths and travel times.
    """

    feed = None
    G = None
    
    def __init__(self, feed, G):
        """
        :param feed: gtfs_functions.Feed object
        :param G: networkx.Graph object, It can be any Graph object. 

        Initializing the Route_Planners object.
        """
        self.feed = feed
        self.G = G

    def get_shortest_path(self, start_station, end_station):
        """
        :param start_station: str, stop_id of the starting station
        :param end_station: str, stop_id of the ending station
        Returns the shortest path between two stations.
        """
        try:
            path = nx.shortest_path(self.G, start_station, end_station, weight = 'weight')            
            return path            
        except Exception as e:
            print('No success with station: %s' % end_station)
            print(e)

    def get_path_cost(self, path, weight="weight"):
        """
        :param path:[str], array of station_ids that we are travelling through
        
        Returns path cost.        
        """    
        return nx.path_weight(self.G, path=path, weight=weight)

    def get_next_services_for_path(self, start_node, end_node, weight="weight"):
        # TODO: Filtering for the time here? Or later? 
        # Stop times at the starting station  
        starts = self.feed.stop_times.query("stop_id=='{}'".format(start_node))
        # 

        ends = self.feed.stop_times.query("stop_id=='{}'".format(end_node))
        # All possible arrivals from the starting node        
        arrivals = ends.loc[ends.trip_id.isin(starts.trip_id.values)]        
        best_arrival = arrivals.sort_values('arrival_time').iloc[0]
        best_start = starts.loc[starts.trip_id==best_arrival.trip_id]
        print('Start: ')
        print(best_start[['stop_name', 'route_name', 'arrival_time', 'departure_time']].iloc[0])
        print('Arrival Time: ')
        print(best_arrival[['stop_name', 'route_name', 'arrival_time', 'departure_time']])


        

        # Returns the start end end stations of the trip with stop_times