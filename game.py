from panda3d.core import Vec3
from wecs import panda3d
from wecs.panda3d import Model

import DustSytem
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
    tank.TankTouchesBoundary,
    # New moving system
    movement.MoveMassSystem,
    DustSytem.DustSystem,
    movement.PrintMsg,
]


def creat_tank(x=0, y=0, angle=45, mass=2000, file="resources/tank.bam", print_rate=0):
    print(x, y, angle, mass, file)
    base.ecs_world.create_entity(
        tank.Tank(),
        panda3d.Model(),
        panda3d.Geometry(file),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        movement.MovingMass(heading=angle, mass=mass),
        DustSytem.Duster(),
        movement.Msg(rate=print_rate),
    )


creat_tank(x=0, y=30, angle=0, mass=500, print_rate=120)
creat_tank(x=40, y=0, angle=0, mass=2000, print_rate=120)
creat_tank(x=20, y=-20, angle=0, mass=5000, print_rate=120)

# for j in range(1, 5):
#     creat_tank(10 * j, 40, heading=90, mass=100*j)


# for i in range(-1, 2):
#     for j in range(-1, 2):
#         creat_tank(10 * i, 10 * j, heading=randint(0, 359), mass=3000)


circle = base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='resources/circle.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(0, 0, 0)),
)

# the rest is to show a 50m circle
base.ecs_world._flush_component_updates()
circle[Model].node.set_scale(50)

base.camera.set_pos(0, -50, 20)
base.camLens.setFov(60)
base.camera.set_pos(0, -70, 40)
base.camLens.setFov(60)
base.camera.look_at(0, 0, -10)

base.enableParticles()
