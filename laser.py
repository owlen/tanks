from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionHandlerQueue, CollisionTraverser, LineSegs, VBase4, CollisionSegment, CollisionNode, \
    CollisionSphere
from wecs.core import System, and_filter, Component
from wecs.panda3d import Model

import game
from misc import TakesDamage, Living, LASER_KEY


@Component()
class LaserGun:
    range: int = 30
    fire_time: int = None
    laser_node_path = None
    damage: int = 2


class LaserSystem(System):
    entity_filters = {
        'targets': and_filter([TakesDamage, Model, TakesDamage, Living]),
        'guns': and_filter([LaserGun, Model, Living]),
    }
    duration = 0.3

    def __init__(self):
        super().__init__()
        self.handler = CollisionHandlerQueue()
        self.traverser = CollisionTraverser()
        self.traverser.showCollisions(game.base.render)

    def enter_filter_guns(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

        # create green laser line
        segs = LineSegs()
        segs.set_thickness(2.0)
        segs.set_color(VBase4(.6, 1, .1, 1))
        segs.move_to(0, 2, 2)
        segs.draw_to(0, 40, 1)
        entity[LaserGun].laser_node_path = model.node.attach_new_node(segs.create())
        entity[LaserGun].laser_node_path.hide()

        # Make a ray with length as "from" collider
        ray = CollisionSegment((0, 5, 1), (0, 70, 0))
        ray_node = CollisionNode("RAY")
        ray_node.add_solid(ray)
        ray_node.set_from_collide_mask(1)
        ray_node.set_into_collide_mask(0)
        ray_np = model.node.attach_new_node(ray_node)
        ray_np.set_python_tag("damage", entity[LaserGun].damage)
        ray_np.show()
        self.traverser.add_collider(ray_np, self.handler)

    def exit_filter_guns(self, entity):
        print("remove LaserGun")

    def enter_filter_targets(self, entity):
        model = entity[Model]
        damage = entity[TakesDamage]
        model.node.set_hpr(0, 0, 0)

        sphere = CollisionSphere((0, 0, 1), damage.sphere_size)
        sphere_node = CollisionNode("TANK-SPHERE")
        sphere_node.add_solid(sphere)
        sphere_node.set_into_collide_mask(1)
        into_np = model.node.attach_new_node(sphere_node)
        into_np.set_python_tag("live", entity[Living])

    def update(self, entities_by_filter):
        self.traverser.traverse(game.base.render)
        for entry in self.handler.getEntries():
            life = entry.getIntoNodePath().get_python_tag('live')
            damage = entry.getFromNodePath().get_python_tag('damage')
            life.accum_damage += damage

        for gun in entities_by_filter['guns']:
            laser_gun = gun[LaserGun]

            if not laser_gun.fire_time:
                if game.base.mouseWatcherNode.is_button_down(LASER_KEY):
                    laser_gun.fire_time = globalClock.getRealTime()
                else:
                    return
            laser_gun.laser_node_path.show()
            if globalClock.getRealTime() - laser_gun.fire_time > self.duration:
                laser_gun.laser_node_path.hide()
                laser_gun.fire_time = None
