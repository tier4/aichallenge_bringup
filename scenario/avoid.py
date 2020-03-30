import os
import lgsvl
import random
import math

sim = lgsvl.Simulator(os.environ.get("SIMULATOR_HOST", "127.0.0.1"), 8181)
if sim.current_scene == "Borregas Avenue":
  sim.reset()
else:
  sim.load("Borregas Avenue")

spawns = sim.get_spawn()
state = lgsvl.AgentState()
state.transform = spawns[0]
state.transform.position.y = state.transform.position.y - 2.0
state.transform.position.x = state.transform.position.x - 33.5
state.transform.position.z = state.transform.position.z - 150
state.transform.rotation.y = state.transform.rotation.y + 180
agent = sim.add_agent("Lexus", lgsvl.AgentType.EGO, state)
agent.connect_bridge(os.environ.get("BRIDGE_HOST", "127.0.0.1"), 9090)

sx = state.transform.position.x + 10
sy = state.transform.position.y 
sz = state.transform.position.z + 20
point = lgsvl.Vector(sx,sy,sz)
npc_state = lgsvl.AgentState()
npc_state.transform = sim.map_point_on_lane(point)
#npc_state.transform = point
npc = sim.add_agent("Sedan", lgsvl.AgentType.NPC, npc_state)
#npc.follow_closest_lane(True, 0)

sim.run(time_limit = 30.0)
