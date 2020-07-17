import builtins

import wecs.panda3d as wp3d
from panda3d.core import Vec3, CardMaker
from wecs import panda3d

import DustSytem
import camera
import comm
import heat
import laser
import misc
import propulsion
import tank
import turret

system_types = [
    # Attach the entity's Model. This gives an entity a node as
    # presence in the scene graph.
    panda3d.SetupModels,
    # Attach Geometry to the Model's node.
    panda3d.ManageGeometry,
    DustSytem.SmokeSystem,
    misc.LifeSystem,
    camera.CameraSystem,
    misc.TextLabelSystem,
    misc.PrintMsg,
    heat.HeatSystem,
    propulsion.PropulsionSystem,
    propulsion.KbsControlSystem,
    tank.GiveTankMoveCommands,
    DustSytem.DustSystem,
    turret.OperateTurrets,
    laser.LaserSystem,
    tank.HandleTankDestruction,
    turret.HandleTurretDestruction,
    comm.ReportSystem,
]

# noinspection PyUnresolvedReferences
base = builtins.base
# noinspection PyUnresolvedReferences
loader = builtins.loader
# noinspection PyUnresolvedReferences
render = builtins.render


def creat_tank(x=0, y=0, angle=45, mass=2000, file="resources/tank.bam", print_rate=0, turn=3):
    t = base.ecs_world.create_entity(
        tank.Tank(),
        wp3d.UpdateBillboards(),
        wp3d.Model(),
        panda3d.Geometry(file),
        wp3d.Scene(node=base.render),
        wp3d.Position(value=Vec3(x, y, 0)),
        heat.Platform(mass=mass),
        propulsion.Propulsion(heading=angle, turn=turn),
        # DustSystem.Duster(),
        laser.LaserGun(nozzle_length=5, range=20),
        misc.TakesDamage(sphere_size=3),
        misc.Msg(rate=print_rate),
        misc.Life(),
        misc.TextLabel(text="-TANK-"),
        comm.Reporting(),
    )
    print(f"Created tank:{t}")


def create_turret(x, y):
    base.ecs_world.create_entity(
        turret.Turret(rotate_speed=60),
        panda3d.Model(),
        panda3d.Geometry(file="resources/ground_turret.bam"),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        heat.Platform(mass=500),
        misc.TakesDamage(sphere_size=1),
        laser.LaserGun(damage=1, nozzle_length=2, range=25, temp=100),
        misc.Msg(rate=0),
        misc.Life(hp=30),
        # misc.Reporting(),
        misc.TextLabel(text="-new-"),
    )


create_turret(20, 0)


# create_turret(-20, 0)
# create_turret(0, 20)
# create_turret(0, -20)


# noinspection PyUnusedLocal
def creat_tank_target(x=0, y=0, angle=90, mass=2000, file="resources/tank.bam", print_rate=0):
    return base.ecs_world.create_entity(
        tank.Tank(),
        panda3d.Model(),
        panda3d.Geometry(file),
        panda3d.Scene(node=base.render),
        panda3d.Position(value=Vec3(x, y, 0)),
        heat.Platform(mass=mass),
        propulsion.Propulsion(heading=angle),
        misc.TakesDamage(),
        misc.Msg(rate=print_rate),
        misc.Life(hp=200),
        misc.TextLabel(text="-TARGET-"),
    )


# player
player = base.ecs_world.create_entity(
    tank.Tank(),
    panda3d.Model(),
    panda3d.Geometry(file="resources/tank.bam"),
    panda3d.Scene(node=base.render),
    panda3d.Position(value=Vec3(20, -20, 0)),
    heat.Platform(mass=1111),
    propulsion.Propulsion(heading=90),
    misc.TakesDamage(),
    laser.LaserGun(mass=500),
    misc.Msg(),
    misc.Life(hp=200),
    misc.TextLabel(text="-new-"),
    propulsion.KbdControlled(),
    # camera.LookAt(),
    comm.Reporting(),
)

print(f"created player: {player}")

creat_tank(x=-20, y=-30, angle=0, mass=500, print_rate=120)
creat_tank(x=10, y=0, angle=0, mass=2000, print_rate=120)
creat_tank(x=30, y=10, angle=0, mass=2000, print_rate=120)
creat_tank(x=-30, y=-10, angle=0, mass=200, print_rate=120)
# creat_tank(x=-0, y=-20, angle=0, mass=8000, print_rate=120)

# for j in range(1, 5, 2):
#     creat_tank_target(20 * j - 60, -2 + 10 * j, mass=500 * j)
#
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
