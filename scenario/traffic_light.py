import os
import lgsvl

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
if sim.current_scene == "Borregas Avenue":
  sim.reset()
else:
  sim.load("Borregas Avenue")

spawns = sim.get_spawn()
state = lgsvl.AgentState()
state.transform = spawns[0]
state.transform.position.y = state.transform.position.y
state.transform.position.x = state.transform.position.x
state.transform.position.z = state.transform.position.z
forward = lgsvl.utils.transform_to_forward(spawns[0])
state.velocity = 5 * forward
agent = sim.add_agent("Lexus", lgsvl.AgentType.EGO, state)
agent.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)

sim.weather = lgsvl.WeatherState(rain=0.8, fog=0.6, wetness=0.6)
sim.set_time_of_day(12)
sim.run(time_limit = 30.0)
