from panda3d.core import Vec3
from wecs import panda3d
from wecs.panda3d import Model, Position

import movement
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
    # Did the paddle move too far? Back to the boundary with it!
    # tank.TankTouchesBoundary,
    # New moving system
    movement.MoveMassSystem,
]

base.ecs_world.create_entity(
    tank.Tank(),
    panda3d.Model(),
    panda3d.Geometry(file='resources/tank.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(20, 10, 0)),
    movement.MovingMass(angle=45, mass=2000),
)

base.ecs_world.create_entity(
    tank.Tank(),
    panda3d.Model(),
    panda3d.Geometry(file='resources/tank.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(10, -10, 0)),
    movement.MovingMass(angle=45, mass=1000),
)

# base.ecs_world.create_entity(
#     tank.Tank(),
#     panda3d.Model(),
#     panda3d.Geometry(file='resources/tank.bam'),
#     panda3d.Scene(node=base.render),
#     panda3d.Position(value=Vec3(-15, -20, 0)),
#     movement.MovingMass(angle=135, mass=1000, friction=0.2),
# )

circle = base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='resources/circle.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(0, 0, 0)),
)

# the rest is to show a 10m circle
base.ecs_world._flush_component_updates()
circle[Model].node.set_scale(50)

base.camera.set_pos(0, -90, 50)
base.camLens.setFov(60)
base.camera.look_at(0, 0, -20)
