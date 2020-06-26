from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Model

from movement import MovingMass

LASER_KEY = KeyboardButton.ascii_key(b'l')
BREAK_KEY = KeyboardButton.ascii_key(b'b')
THROTTLE_UP_KEY = KeyboardButton.ascii_key(b'+')
THROTTLE_DOWN_KEY = KeyboardButton.ascii_key(b'-')


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

    def enter_filter_guns(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

        segs = LineSegs()
        segs.set_thickness(2.0)
        segs.set_color(VBase4(.6, 1, .1, 1))
        segs.move_to(0, 2, 2)
        segs.draw_to(0, 40, 0)
        entity[LaserGun].laser_node_path = model.node.attach_new_node(segs.create())
        entity[LaserGun].laser_node_path.hide()

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


@Component()
class Tank:
    # size: float = 0.2
    weight: int = 1


class GiveTankMoveCommands(System):
    entity_filters = {
        # 'tanks': Tank

        'tanks': and_filter([
            MovingMass,
            Tank,
        ]),
    }

    def enter_filter_tanks(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:
            # movement = entity[Movement]

            # What keys does the player use?
            up_key = KeyboardButton.ascii_key(b'w')
            down_key = KeyboardButton.ascii_key(b's')

            # Read player input
            delta = 0
            if base.mouseWatcherNode.is_button_down(up_key):
                delta += 1
            if base.mouseWatcherNode.is_button_down(down_key):
                delta -= 1

            # Store movement
            # movement.value.y = delta

            if base.mouseWatcherNode.is_button_down(THROTTLE_UP_KEY):
                entity[MovingMass].forward_force = min(4000, entity[MovingMass].forward_force + 100.0)
            if base.mouseWatcherNode.is_button_down(THROTTLE_DOWN_KEY):
                entity[MovingMass].forward_force = max(0, entity[MovingMass].forward_force - 100.0)
            if base.mouseWatcherNode.is_button_down(BREAK_KEY):
                entity[MovingMass].break_force = 10000
            else:
                entity[MovingMass].break_force = 0


class TankTouchesBoundary(System):
    entity_filters = {
        'tanks': and_filter([MovingMass, Tank])
    }

    arena_radius = 50

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):

            distance = entity[Model].node.getPos().length()

            if distance > self.arena_radius:
                print(f"  out  {entity} distance: {distance}")
