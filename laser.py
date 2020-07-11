from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionHandlerQueue, CollisionTraverser, LineSegs, VBase4, CollisionSegment, CollisionNode, \
    CollisionSphere, KeyboardButton
from wecs.core import System, and_filter, Component
from wecs.panda3d import Model

import game
from misc import TakesDamage, Living, HeatSystem, Platform, Msg

LASER_KEY = KeyboardButton.ascii_key('l')


@Component()
class LaserGun:
    range: int = 15
    nozzle_length: int = 4
    damage: int = 2
    fire_time: int = None
    ray_np = None
    laser_np = None
    temp: int = 50
    mass: int = 100
    platform = None


class LaserSystem(HeatSystem, System):
    entity_filters = {
        'targets': and_filter([TakesDamage, Model, TakesDamage, Living]),
        'guns': and_filter([LaserGun, Model, Living]),
    }
    duration = 0.3

    def __init__(self):
        super().__init__()
        self.queue = CollisionHandlerQueue()
        self.traverser = CollisionTraverser()
        # self.traverser.showCollisions(game.base.render)

    def enter_filter_guns(self, entity):
        model = entity[Model]
        laser_gun = entity[LaserGun]
        laser_gun.platform = entity[Platform]

        # create green laser line
        segs = LineSegs()
        segs.set_thickness(2.0)
        segs.set_color(VBase4(.6, 1, .1, 1))
        segs.move_to(0, laser_gun.nozzle_length, 2)
        segs.draw_to(0, laser_gun.range, 1)
        laser_gun.laser_np = model.node.attach_new_node(segs.create())
        laser_gun.laser_np.hide()

        # Make a ray with length as "from" collider
        ray = CollisionSegment((0, laser_gun.nozzle_length, 1), (0, laser_gun.range, 0))
        ray_node = CollisionNode("RAY")
        ray_node.add_solid(ray)
        ray_node.set_from_collide_mask(1)
        ray_node.set_into_collide_mask(0)
        ray_np = model.node.attach_new_node(ray_node)
        ray_np.set_python_tag("damage", laser_gun.damage)
        ray_np.show()
        self.traverser.add_collider(ray_np, self.queue)
        laser_gun.ray_np = ray_np

    def exit_filter_guns(self, entity):
        laser_gun = entity[LaserGun]
        laser_gun.ray_np.hide()
        laser_gun.laser_np.hide()
        self.traverser.removeCollider(laser_gun.ray_np)

    def enter_filter_targets(self, entity):
        model = entity[Model]
        damage = entity[TakesDamage]
        model.node.set_hpr(0, 0, 0)

        sphere = CollisionSphere((0, 0, 1), damage.sphere_size)
        sphere_node = CollisionNode("TANK-SPHERE")
        sphere_node.add_solid(sphere)
        sphere_node.set_into_collide_mask(1)
        target_np = model.node.attach_new_node(sphere_node)
        target_np.set_python_tag('live', entity[Living])
        entity[TakesDamage].target_np = target_np

    def exit_filter_targets(self, entity):
        print("remove target!", entity)
        target_np = entity[TakesDamage].target_np
        target_np.hide()
        del entity[TakesDamage].target_np

    def update(self, entities_by_filter):
        self.traverser.traverse(game.base.render)
        for entry in self.queue.getEntries():
            life = entry.getIntoNodePath().get_python_tag('live')
            damage = entry.getFromNodePath().get_python_tag('damage')
            life.accum_damage += damage

        for gun in entities_by_filter['guns']:
            laser_gun = gun[LaserGun]
            gun[Msg].msg = f"gun temp:{laser_gun.temp}"

            self.exchange_heat(laser_gun)

            if not laser_gun.fire_time:
                if game.base.mouseWatcherNode.is_button_down(LASER_KEY):
                    laser_gun.fire_time = globalClock.getRealTime()
                else:
                    continue
            laser_gun.laser_np.show()
            if globalClock.getRealTime() - laser_gun.fire_time > self.duration:
                laser_gun.laser_np.hide()
                laser_gun.fire_time = None
