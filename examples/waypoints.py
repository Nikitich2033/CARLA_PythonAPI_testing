import carla

# Create a new CARLA client
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the scenario
world = client.load_world('Town03')

# Get the blueprint for a Cybertruck
cybertruck_bp = world.get_blueprint_library().find('vehicle.tesla.cybertruck')

# Set the starting location and orientation for the Cybertruck
start_transform = carla.Transform(carla.Location(x=154, y=-95, z=8.5), carla.Rotation(yaw=0))

# Spawn the Cybertruck at the specified location and orientation
cybertruck = world.spawn_actor(cybertruck_bp, start_transform)

# # Get the waypoint at the current location of the Cybertruck
# waypoint = map.get_location(cybertruck.get_location())

# # Get the next waypoint in front of the Cybertruck
# next_waypoint = waypoint.next()
map = world.get_map()


spawn_points = world.get_map().get_spawn_points()

# Nearest waypoint on the center of a Driving or Sidewalk lane.
waypoint01 = map.get_waypoint(cybertruck.get_location(),project_to_road=True, lane_type=(carla.LaneType.Driving | carla.LaneType.Sidewalk))

waypoints = map.generate_waypoints(5)
# waypoints = map.next_until_lane_end(5)
for w in waypoints:
    # world.debug.draw_string(carla.Location(x=cybertruck.get_location().x, y=cybertruck.get_location().y, z=1), 'O', draw_shadow=False,
    #                                    color=carla.Color(r=255, g=0, b=0), life_time=120.0,
    #                                    persistent_lines=True)
    world.debug.draw_string(w.transform.location, str(w.transform.location.x) + " , " + str(w.transform.location.y) + " , " + str(w.transform.location.z), draw_shadow=False,
                                       color=carla.Color(r=255, g=0, b=0), life_time=120.0,
                                       persistent_lines=True)
                                       
# #Nearest waypoint but specifying OpenDRIVE parameters. 
# waypoint02 = map.get_waypoint_xodr(road_id,lane_id,s)

waypoint_list = map.generate_waypoints(2.0)