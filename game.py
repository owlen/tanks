from panda3d.core import Vec3

from wecs import panda3d

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
    # If the Paddle's size has changed, apply it to the Model.
    paddles.ResizePaddles,
    # Read player input and store it on Movement
    tank.GiveTankMoveCommands,
    # Apply the Movement
    movement.MoveObject,
    # Did the paddle move too far? Back to the boundary with it!
    tank.TankTouchesBoundary,
]


base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='tank.bam'),
    panda3d.Scene(node=base.aspect2d),
    panda3d.Position(value=Vec3(-1.1, 0, 0)),
    movement.Movement(value=Vec3(0, 0, 0)),
    paddles.Paddle(player=paddles.Players.LEFT),
)
