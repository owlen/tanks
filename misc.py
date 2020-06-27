from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import CollisionHandlerQueue, CollisionTraverser, LineSegs, VBase4, CollisionSegment, CollisionNode, \
    CollisionSphere, KeyboardButton
from wecs.core import Component, System, and_filter
from wecs.panda3d import Model

LASER_KEY = KeyboardButton.ascii_key(b'l')

@Component()
class Living:
    hp: int = 100
    accum_damage: int = 0


class LifeSystem(System):
    entity_filters = {
        'mortals': and_filter([Living, Model])
    }

    def enter_filter_mortals(self, entity):
        mortal = entity[Living]
        print(mortal)

    def update(self, entities_by_filter):
        for mortal in entities_by_filter['mortals']:
            living = mortal[Living]
            if living.accum_damage > 0:
                living.hp -= living.accum_damage
                print(f"got {living.accum_damage} damage. HP:{living.hp}")


@Component()
class LaserGun:
    range: int = 30
    fire_time: int = None
    laser_node_path = None


class LaserSystem(System):
    entity_filters = {
        'guns': and_filter([LaserGun, Model])
    }
    duration = 0.3

    handler = CollisionHandlerQueue()
    base.cTrav = CollisionTraverser()
    base.cTrav.show_collisions(base.render)

    def enter_filter_guns(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

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
        ray_np = model.node.attach_new_node(ray_node)
        ray_np.show()
        base.cTrav.add_collider(ray_np, self.handler)

        sphere = CollisionSphere((0, 0, 1), 3)
        sphere_node = CollisionNode("TANK-SPHERE")
        sphere_node.add_solid(sphere)
        sphere_node.set_into_collide_mask(1)
        into_np = model.node.attach_new_node(sphere_node)
        # into_np.show()

    def update(self, entities_by_filter):
        for gun in entities_by_filter['guns']:
            laser_gun = gun[LaserGun]

            if not laser_gun.fire_time:
                if base.mouseWatcherNode.is_button_down(LASER_KEY):
                    laser_gun.fire_time = globalClock.getRealTime()
                else:
                    return
            laser_gun.laser_node_path.show()
            if globalClock.getRealTime() - laser_gun.fire_time > self.duration:
                laser_gun.laser_node_path.hide()
                laser_gun.fire_time = None

