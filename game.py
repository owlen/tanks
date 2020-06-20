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
    # paddles.GivePaddlesMoveCommands,
    # Apply the Movement
    movement.MoveObject,
    # Did the paddle move too far? Back to the boundary with it!
    tank.TankTouchesBoundary,
]


base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='resources/tank.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(-2, 10, 0)),
    movement.Movement(value=Vec3(2, 2, 0)),
    tank.Tank(),
)

base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='resources/tank.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(-5, -20, 0)),
    movement.Movement(value=Vec3(0, 0, 0)),
    tank.Tank(),
)

circle = base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='resources/circle.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(0, 0, 0)),
)


# the rest is to show a 10m circle
base.ecs_world._flush_component_updates()

circle[Model].node.set_scale(30)

base.cam.set_pos(0, -20, 100); base.cam.look_at(0, 0.01, 0)