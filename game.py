from panda3d.core import Vec3, CollisionSphere, CollisionNode
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
    # New moving system
    movement.MoveMassSystem,
    DustSytem.DustSystem,
    # tank.TankTouchesBoundary,
    movement.PrintMsg,
    tank.LaserSystem
]


def creat_tank(x=0, y=0, angle=45, mass=2000, file="resources/tank.bam", print_rate=0):
    base.ecs_world.create_entity(
        tank.Tank(),
        panda3d.Model(),
        panda3d.Geometry(file),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        movement.MovingMass(heading=angle, mass=mass),
        DustSytem.Duster(),
        tank.LaserGun(),
        movement.Msg(rate=print_rate),
    )


def creat_tank_target(x=0, y=0, angle=45, mass=2000, file="resources/tank.bam", print_rate=0):
    base.ecs_world.create_entity(
        tank.Tank(),
        panda3d.Model(),
        panda3d.Geometry(file),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        # movement.MovingMass(heading=angle, mass=mass),  NO MOVING MASS
        movement.Msg(rate=print_rate),
    )


creat_tank(x=0, y=30, angle=0, mass=500, print_rate=120)
creat_tank(x=30, y=-20, angle=0, mass=2000, print_rate=120)

# for j in range(1, 5):
#     creat_tank_target(20 * j - 30, -10, mass=100 * j)

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

# Make a CollisionSphere as "into" collider
sphere = CollisionSphere((0, 10, 0), 2)
into_node = CollisionNode("TARGET-SPHERE")
into_node.add_solid(sphere)
into_node.set_into_collide_mask(1)
into_np = render.attach_new_node(into_node)
into_np.show()
