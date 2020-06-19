from panda3d.core import Vec3

from wecs import panda3d
from wecs.panda3d import Model

# These modules contain the actual game mechanics, which we are tying
# together into an application in this file:

import movement
import paddles
import tank


system_types = [
    # Attach the entity's Model. This gives an entity a node as
    # presence in the scene graph.
    panda3d.SetupModels,
    # Attach Geometry to the Model's node.
    panda3d.ManageGeometry,
    # Read player input and store it on Movement
    tank.GiveTankMoveCommands,
    paddles.GivePaddlesMoveCommands,
    # Apply the Movement
    movement.MoveObject,
    # Did the paddle move too far? Back to the boundary with it!
    tank.TankTouchesBoundary,
]


tank1_entity = base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='tank.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(-2, 10, 0)),
    movement.Movement(value=Vec3(2, 0, 0)),
    paddles.Paddle(player=paddles.Players.LEFT),
)

tank2_entity = base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='tank.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(-3, 10, 0)),
    movement.Movement(value=Vec3(0, 0, 0)),
    paddles.Paddle(player=paddles.Players.LEFT),
)

base.ecs_world._flush_component_updates()

tank_node1 = tank1_entity[Model].node
tank_node1.set_r(-45)
tank_node1.set_h(90)
tank_node1.set_scale(.1)

tank_node2 = tank2_entity[Model].node
tank_node2.set_r(-45)
tank_node2.set_h(90)
tank_node2.set_scale(.1)

