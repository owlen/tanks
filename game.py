import builtins

import wecs.panda3d as wp3d
from panda3d.core import Vec3, CardMaker
from wecs import panda3d

import DustSytem
import camera
import laser
import misc
import movement
import tank
import turret

system_types = [
    # Attach the entity's Model. This gives an entity a node as
    # presence in the scene graph.
    panda3d.SetupModels,
    # Attach Geometry to the Model's node.
    panda3d.ManageGeometry,
    misc.SmokeSystem,
    misc.LifeSystem,
    camera.CameraSystem,
    misc.TextLabelSystem,
    misc.PrintMsg,
    movement.MoveMassSystem,
    tank.GiveTankMoveCommands,
    DustSytem.DustSystem,
    turret.OperateTurrets,
    laser.LaserSystem,
    tank.HandleTankDestruction,
    turret.HandleTurretDestruction,
    movement.KbsControlSystem,
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
        laser.LaserGun(nozzle_length=5, range=50),
        misc.TakesDamage(sphere_size=3),
        misc.Msg(rate=print_rate),
        misc.Living(),
        misc.TextLabel(text="-TANK-"),
    )


base.ecs_world.create_entity(
    turret.Turret(rotate_speed=45),
    panda3d.Model(),
    panda3d.Geometry(file="resources/ground_turret.bam"),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(20, 0, 0)),
    misc.TakesDamage(sphere_size=1),
    laser.LaserGun(damage=1, nozzle_length=2, range=20),
    misc.Msg(rate=0),
    misc.Living(hp=30),
    misc.TextLabel(text="-new-"),
)


# noinspection PyUnusedLocal
def creat_tank_target(x=0, y=0, angle=90, mass=2000, file="resources/tank.bam", print_rate=0):
    return base.ecs_world.create_entity(
        tank.Tank(),
        panda3d.Model(),
        panda3d.Geometry(file),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        movement.MovingMass(heading=angle, mass=mass),
        misc.TakesDamage(),
        # misc.Smoking(),
        misc.Msg(rate=print_rate),
        misc.Living(hp=200),
        misc.TextLabel(text="-TARGET-"),
    )


base.ecs_world.create_entity(
    tank.Tank(),
    panda3d.Model(),
    panda3d.Geometry(file="resources/tank.bam"),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(0, -40, 0)),
    movement.MovingMass(heading=90, mass=5000),
    misc.TakesDamage(),
    laser.LaserGun(),
    misc.Msg(rate=10),
    misc.Living(hp=200),
    misc.TextLabel(text="-new-"),
    movement.KbdControlled(),
    # camera.LookAt(),
)

# creat_tank(x=-20, y=-30, angle=0, mass=500, print_rate=120)
# creat_tank(x=10, y=0, angle=0, mass=2000, print_rate=120)

# for j in range(1, 5, 2):
#     creat_tank_target(20 * j - 60, -2 + 10 * j, mass=500 * j)

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
