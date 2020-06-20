from panda3d.core import Vec3

from wecs import panda3d
from wecs.panda3d import Model, Position

# These modules contain the actual game mechanics, which we are tying
# together into an application in this file:

import tank


system_types = [
    tank.GiveTankMoveCommands,
]


base.ecs_world.create_entity(
      panda3d.Model(),
#     panda3d.Geometry(file='resources/tank.bam'),
#     panda3d.Scene(node=base.render),
#     panda3d.Position(value=Vec3(-5, -20, 0)),
#     movement.Movement(value=Vec3(0, 0, 0)),
      tank.Tank(),
)

circle = base.ecs_world.create_entity(
    # panda3d.Model(),
    # panda3d.Geometry(file='resources/circle.bam'),
    # panda3d.Scene(node=base.render),
    # panda3d.Position(value=Vec3(0, 0, 0)),
)


