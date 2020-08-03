import builtins

import wecs.panda3d as wp3d
from panda3d.bullet import BulletRigidBodyNode, BulletWorld, BulletBoxShape, BulletDebugNode
from panda3d.core import Vec3, CardMaker, TransformState, Point3
from wecs import panda3d
from wecs.mechanics import clock
from wecs.panda3d import prototype
from wecs.panda3d.prototype import Model

import DustSytem
import camera
import comm
import heat
import laser
import misc
import propulsion
import radar
import tank
import turret

system_types = [

    prototype.ManageModels,
    clock.DetermineTimestep,
    prototype.DeterminePhysicsTimestep,
    prototype.DoPhysics,

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
    radar.RadarSystem,
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
        # wp3d.Scene(node=base.render),
        wp3d.Position(value=Vec3(x, y, 0)),
        heat.Platform(mass=mass),
        propulsion.Propulsion(heading=angle, turn=turn),
        # DustSystem.Duster(),
        laser.LaserGun(nozzle_length=5, range=20),
        misc.TakesDamage(sphere_size=3),
        misc.Msg(rate=print_rate),
        misc.Life(),
        misc.TextLabel(text="-TANK-"),
        # comm.Reporting(),
    )
    print(f"Created tank:{t}")


# noinspection PyUnusedLocal
def creat_tank_target(x=0, y=0, angle=90, mass=2000, file="resources/tank.bam", print_rate=0):
    return base.ecs_world.create_entity(
        tank.Tank(),
        prototype.Model(post_attach=prototype.transform(pos=Vec3(x, y, 0))),
        prototype.Geometry(file=file),
        heat.Platform(mass=mass),
        propulsion.Propulsion(heading=angle),
        misc.TakesDamage(),
        misc.Msg(rate=print_rate),
        misc.Life(hp=200),
        misc.TextLabel(text="-TARGET-"),
    )


bullet_world = BulletWorld()
bullet_world.set_gravity(Vec3(0, 0, -9.81))
world = base.ecs_world.create_entity(
    clock.Clock(clock=clock.panda3d_clock),
    prototype.PhysicsWorld(world=bullet_world, timestep=1 / 30),
)

debugNode = BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()
bullet_world.setDebugNode(debugNP.node())

bullet_floor = BulletRigidBodyNode()
bullet_floor.set_mass(0.0)
bullet_floor.add_shape(BulletBoxShape(Vec3(50, 50, 0)),
                       TransformState.make_pos(Point3(0, 0, 0)))
base.ecs_world.create_entity(
    prototype.Model(post_attach=prototype.transform(pos=Vec3(0, 0, 0)), ),
    prototype.PhysicsBody(body=bullet_floor, world=world._uid, ),
)

# player
bullet_tank = BulletRigidBodyNode()
bullet_tank.set_linear_sleep_threshold(0)
bullet_tank.set_angular_sleep_threshold(0)
bullet_tank.set_mass(100.0)

bullet_tank.add_shape(BulletBoxShape(Vec3(2.5, 3, 1)),
                      TransformState.make_pos(Point3(0, 0, 1)))

player = base.ecs_world.create_entity(
    tank.Tank(),
    prototype.Model(post_attach=prototype.transform(pos=Vec3(20, -49, 5))),
    prototype.Geometry(file='resources/tank.bam'),
    prototype.PhysicsBody(body=bullet_tank, world=world._uid, ),
    heat.Platform(mass=1111),
    propulsion.Propulsion(heading=45),
    misc.TakesDamage(),
    laser.LaserGun(mass=500),
    misc.Msg(rate=0),
    misc.Life(hp=200),
    misc.TextLabel(text="-new-"),
    propulsion.KbdControlled(),
    # camera.LookAt(),
    comm.Reporting(),
    radar.FrontRadar(),

)
print(f"created player: {player}")


def create_turret(x, y):
    bullet_turret = BulletRigidBodyNode()
    bullet_turret.set_linear_sleep_threshold(0)
    bullet_turret.set_angular_sleep_threshold(0)
    bullet_turret.set_mass(100.0)

    bullet_turret.add_shape(BulletBoxShape(Vec3(1, 1, 1)), TransformState.make_pos(Point3(0, 0, 1)))
    base.ecs_world.create_entity(
        turret.Turret(rotate_speed=30),
        prototype.Model(post_attach=prototype.transform(pos=Vec3(x, y, 0))),
        prototype.Geometry(file='resources/ground_turret.bam'),
        prototype.PhysicsBody(body=bullet_turret, world=world._uid, ),
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


# creat_tank(x=0, y=10, angle=45, mass=500, print_rate=0)
# creat_tank(x=10, y=0, angle=0, mass=2000, print_rate=120)
# creat_tank(x=30, y=10, angle=0, mass=2000, print_rate=120)
# creat_tank(x=-30, y=-10, angle=0, mass=200, print_rate=120)
# creat_tank(x=-0, y=-20, angle=0, mass=8000, print_rate=120)

# for j in range(1, 5, 2):
#     creat_tank_target(20 * j - 60, -2 + 10 * j, mass=500 * j)
circle = base.ecs_world.create_entity(
    prototype.Model(post_attach=prototype.transform(pos=Vec3(0, 0, .1))),
    prototype.Geometry(file='resources/circle.bam'),
)

# show a 50m circle
base.ecs_world._flush_component_updates()
circle[Model].node.set_scale(50)

base.camera.set_pos(0, -50, 20)
base.camLens.set_fov(60)
base.camera.set_pos(0, -80, 40)
base.camLens.set_fov(70)
base.camera.look_at(0, 0, -10)

base.enableParticles()

groundTexture = loader.loadTexture("resources/ground1.jpg")
cm = CardMaker('card')
cm.set_frame(-50, 50, -50, 50)
card = render.attachNewNode(cm.generate())
card.set_p(-90)
card.set_z(0)
card.set_texture(groundTexture)
