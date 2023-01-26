import carla
import time 
from agents.navigation.basic_agent import BasicAgent
from agents.navigation.controller import VehiclePIDController
import math

# Create a new CARLA client
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

# Load the scenario
world = client.load_world('Town03')

# # Get the blueprint for a Cybertruck
cybertruck_bp = world.get_blueprint_library().find('vehicle.tesla.cybertruck')

# # Set the starting location and orientation for the Cybertruck
start_transform = carla.Transform(carla.Location(x=150, y=-100, z=8.5), carla.Rotation(yaw=0))

# # Spawn the Cybertruck at the specified location and orientation
cybertruck = world.spawn_actor(cybertruck_bp, start_transform)

map = world.get_map()

def draw_waypoints(waypoints, road_id=None, life_time=50.0):

  for waypoint in waypoints:

    if(waypoint.road_id == road_id):
        world.debug.draw_string(waypoint.transform.location, str(road_id), draw_shadow=False,
                                   color=carla.Color(r=0, g=255, b=0), life_time=life_time,
                                   persistent_lines=True)

def draw_all_waypoints(waypoints, life_time=50.0):

  for waypoint in waypoints:
        world.debug.draw_string(waypoint.transform.location, str(waypoint.road_id), draw_shadow=False,
                                   color=carla.Color(r=0, g=255, b=0), life_time=life_time,
                                   persistent_lines=True)

waypoints = client.get_world().get_map().generate_waypoints(distance=1.0)
# draw_all_waypoints(waypoints)
draw_waypoints(waypoints, road_id=24, life_time=100)
draw_waypoints(waypoints, road_id=30, life_time=100)
draw_waypoints(waypoints, road_id=110, life_time=100)


filtered_waypoints = []
for waypoint in waypoints:
    if(waypoint.road_id == 24):
      filtered_waypoints.append(waypoint)

spawn_point = filtered_waypoints[10].transform
spawn_point.location.z += 2

vehicle = client.get_world().spawn_actor(cybertruck_bp, spawn_point)
agent = BasicAgent(vehicle)

# Get the spectator camera
spectator = world.get_spectator()

# Get the position of an actor in the scene
actor = vehicle
actor_location = actor.get_location()

# Set the camera to look at the actor
spectator.set_transform(carla.Transform(actor_location+carla.Location(z=40), carla.Rotation(pitch=-90)))

target_road_waypoints = []
for waypoint in waypoints:
    if(waypoint.road_id == 30):
      target_road_waypoints.append(waypoint)

furthest_waypoint = None
max_distance = 0
# for waypoint in target_road_waypoints:
#     distance = actor_location.distance(waypoint.transform.location)
#     if distance > max_distance:
#         max_distance = distance
#         furthest_waypoint = waypoint

target_waypoint = target_road_waypoints[len(target_road_waypoints)-1].transform
# target_waypoint = furthest_waypoint

agent.set_destination([target_waypoint.location.x, 
                       target_waypoint.location.y, 
                       target_waypoint.location.z])

client.get_world().debug.draw_string(target_waypoint.location, 
                                        'O', draw_shadow=False,
                                        color=carla.Color(r=255, g=0, b=0), life_time=20,
                                        persistent_lines=True)




while True:
    actor_location = actor.get_location()
    actor_transform = actor.get_transform()
    actor_yaw = actor_transform.rotation.yaw
    spectator.set_transform(carla.Transform(actor_location+carla.Location(  z=10, 
                                                                            x= - 10*math.cos(math.radians(actor_yaw)), 
                                                                            y= - 10*math.sin(math.radians(actor_yaw))),
                                                                            carla.Rotation(pitch= -30 ,yaw=actor_yaw)))
    if agent.done():
        print("The target has been reached, stopping the simulation")
        break

    vehicle.apply_control(agent.run_step())

# custom_controller = VehiclePIDController(cybertruck, args_lateral = {'K_P': 0, 'K_D': 0.0, 'K_I': 0}, args_longitudinal = {'K_P': 1, 'K_D': 0.0, 'K_I': 0})
# ticks_to_track = 5
# for i in range(ticks_to_track):
#     control_signal = custom_controller.run_step(1, target_waypoint)
#     vehicle.apply_control(control_signal)
	
    