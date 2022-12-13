import requests
import json
import plotly.express as px
import folium


"""
    This can be used to check all endpoints of the api are working correctly
     
"""
# TODO: Update when I add the remaining CRUD operations to the api

class Trails:
    def __init__(self, api_url):
        self.url = api_url

    def __repr__(self):
        return f"The url in this instance is:  {self.url} "

    def get_users(self):
        """
        Gets all users from TrailService
        :return:
        """
        user_url = self.url + '/users'
        print("Getting users from the endpoint: {}".format(user_url))
        res = requests.get(user_url)
        json_res = res.json()
        json_data = json.dumps(json_res, indent=4)
        return json_res

    def get_user_by_name(self, username):
        """
        Gets a user by username
        :param username: TrailService user
        :return: List: JSON response - a list of dicts
        """
        unique_user_url = self.url + '/users/' + username
        print(unique_user_url)
        res = requests.get(unique_user_url)
        json_res = res.json()
        json_data = json.dumps(json_res, indent=4)
        return json_res


    def get_trails(self):
        """
        Gets all trails from the /trails endpoint
        :return: list: JSON response dicts
        """
        trail_url = self.url + '/trails'
        print("Getting trails from the endpoint: {}".format(trail_url))
        res = requests.get(trail_url)
        json_res = res.json()
        json_data = json.dumps(json_res, indent=4)
        return json_res

    def get_location_points(self):
        """
        Gets all location points for all trails
        :return: list: JSON response dicts
        """
        location_url = self.url + '/locationpoints'
        print(location_url)
        res = requests.get(location_url)
        json_res = res.json()
        json_data = json.dumps(json_res, indent=4)
        return json_res

    def get_one_trail_points(self, trail_name):
        """
        Gets the location points for an individual trail
        :param trail_name: string: name of trail
        :return: list: JSON response dicts
        """
        individual_url = self.url + '/Locationpoints/' + trail_name
        print(individual_url)
        response = requests.get(individual_url)
        res_list = response.json()
        json_data = json.dumps(res_list, indent=4)
        return res_list

    def get_lat_and_longs(self, response_list):
        """
        Used to get lists of latitudes and longitudes of a trail
        :param response_list: dicts containing location points
        :return: lists: lats, longs
        """
        lats = []
        longs = []
        for d in response_list:
            lats.append(dict.get(d, 'latitude'))
            longs.append(dict.get(d, 'longitude'))
        coordinates = list(zip(lats, longs))
        return lats, longs

    def get_coords(self, response_list):
        """
        Gets all latitude and longitudes for a trail and creates points (lat&long)
        :param response_list: response_list: dicts containing location points
        :return: list: tuples of latitude and longitude
        """
        lats = []
        longs = []
        for d in response_list:
            lats.append(dict.get(d, 'latitude'))
            longs.append(dict.get(d, 'longitude'))
        coordinates = list(zip(lats, longs))
        return coordinates

    def get_elevation(self, response_list):
        """
        Gets the elevation for each point of a trail
        :param response_list: response_list: dicts containing location points
        :return: list: containing all elevations
        """
        elevations = []
        for d in response_list:
            elevations.append(dict.get(d, 'elevation'))
        return elevations


    def get_comments(self, response_list):
        """
        Gets all comments from each location point
        :param response_list: response_list: dicts containing location points
        :return: list: containing all comment id's
        """
        all_comments = []
        comment_ids = []
        for d in response_list:
            c = dict.get(d, 'commentId')
            all_comments.append(c)
            # print(c)
            if c != 'NC':
                comment_ids.append(c)
        print("Total number of comments in trail: {}".format(len(comment_ids)))
        return all_comments

    def plot_trail(self, returned_points):
        """
        Plots a trail (scatter plot) using the latitudes and longitudes
        Shows elevation as different colours
        :param returned_points: response_list: dicts containing location points
        :return: plotly Figure
        """
        points = returned_points
        ele = getting_trails.get_elevation(points)
        lats, longs = getting_trails.get_lat_and_longs(points)
        print(points[0])
        coordinates = list(zip(lats, longs))
        # Plotting the route
        fig = px.scatter(x=longs,
                         y=lats,
                         color=ele,
                         labels={
                             "lats": "lats",
                             "longs": "longs"
                         },
                         color_continuous_scale=px.colors.sequential.Sunsetdark,
                         title=dict.get(points[0], 'trailName'))
        fig.update_layout(xaxis_title="Longitude", yaxis_title="Latitude")
        fig.show()
        return fig

    def create_map (self, response_list):
        """
        Creates a map using the coordinates from a trail
        Can only be used in a jupyter notebook
        Can be implemented by writing a custom temporary-HTML renderer
        See: https://github.com/python-visualization/folium/issues/946
        :param response_list: dicts containing location points
        :return: folium map
        """
        m = folium.Map()
        coords = getting_trails.get_coords(response_list)
        for p in coords:
            folium.Marker(p).add_to(m)
        return m


if __name__ == '__main__':
    url = 'http://localhost:5026/api'
    getting_trails = Trails(url)
    print(getting_trails)

    user_data = getting_trails.get_users()
    trail_data = getting_trails.get_trails()
    all_location_points = getting_trails.get_location_points()

    # Trail names
    cadover_name = 'Cadover Bridge to Shaugh Bridge Circular'
    lynton_name = 'Lynton, Watersmeet and Valley of the Rocks'
    combe_name = 'Combe Martin Circular'

    # Users
    ada = 'Ada Lovelace'
    grace = 'Grace Hopper'
    tim = 'Tim Berners-Lee'

    # Cadover trail points
    cadover_points = getting_trails.get_one_trail_points(cadover_name)

    # Getting the comments from a response
    cadover_comments = getting_trails.get_comments(cadover_points)
    print(getting_trails.get_user_by_name(ada))

    # Plotting a trail
    getting_trails.plot_trail(cadover_points)
    map_print = getting_trails.create_map(cadover_points)

    print(map_print)  # This will only work in a jupyter notebook








