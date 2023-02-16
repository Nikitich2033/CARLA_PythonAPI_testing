import carla

# Create a new CARLA client
client = carla.Client('localhost', 2000)
client.set_timeout(10.0)

client.replay_file("test.log", 0, 0, 0)