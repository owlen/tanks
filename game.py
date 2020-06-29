import builtins

import wecs.panda3d as wp3d
from panda3d.core import Vec3, CardMaker
from wecs import panda3d

import DustSytem
import laser
import misc
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
    laser.LaserSystem,
    misc.SmokeSystem,
    misc.LifeSystem,
    misc.CameraSystem,
    misc.TextLabelSystem,
]

# noinspection PyUnresolvedReferences
base = builtins.base
# noinspection PyUnresolvedReferences
loader = builtins.loader
# noinspection PyUnresolvedReferences
render = builtins.render


def creat_tank(x=0, y=0, angle=45, mass=2000, file="resources/tank.bam", print_rate=0, turn=3):
    return base.ecs_world.create_entity(
        tank.Tank(),
        wp3d.UpdateBillboards(),
        wp3d.Model(),
        panda3d.Geometry(file),
        wp3d.Scene(node=base.render),
        wp3d.Position(value=Vec3(x, y, 0)),
        movement.MovingMass(heading=angle, mass=mass, turn=turn),
        DustSytem.Duster(),
        laser.LaserGun(),
        misc.TakesDamage(),
        movement.Msg(rate=print_rate),
        misc.Living(),
        misc.TextLabel(text="-TANK-"),
    )


# noinspection PyUnusedLocal
def creat_tank_target(x=0, y=0, angle=45, mass=2000, file="resources/tank.bam", print_rate=0):
    return base.ecs_world.create_entity(
        tank.Tank(),
        panda3d.Model(),
        panda3d.Geometry(file),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        # movement.MovingMass(heading=angle, mass=mass),  NO MOVING MASS
        misc.TakesDamage(),
        movement.Msg(rate=print_rate),
        misc.Living(),
        misc.TextLabel(text="-TANK-"),
    )


t1 = creat_tank(x=20, y=-30, angle=0, mass=500, print_rate=120)
creat_tank(x=10, y=0, angle=0, mass=2000, print_rate=120)

# print(f"t1 - {t1} {t1[tank.Tank()]}")
# base.ecs_world.create_entity(
#     misc.TextLabel(text="-TANK-", parent=t1)
# )

for j in range(1, 5):
    creat_tank_target(20 * j - 60, -2 + 10 * j, mass=100 * j)

circle = base.ecs_world.create_entity(
    panda3d.Model(),
    panda3d.Geometry(file='resources/circle.bam'),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(0, 0, 0)),
)

# the rest is to show a 50m circle
base.ecs_world._flush_component_updates()
circle[wp3d.Model].node.set_scale(50)

base.camera.set_pos(0, -50, 20)
base.camLens.setFov(60)
base.camera.set_pos(0, -80, 40)
base.camLens.setFov(70)
base.camera.look_at(0, 0, -10)

base.enableParticles()

groundTexture = loader.loadTexture("resources/ground1.jpg")
cm = CardMaker('card')
cm.set_frame(-50, 50, -50, 50)
card = render.attachNewNode(cm.generate())
card.setP(-90)
card.setZ(-1)
card.setTexture(groundTexture)
