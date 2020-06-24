from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Model

from movement import MovingMass


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
        print('in enter_filter_tanks')
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

            throttle_up_key = KeyboardButton.ascii_key(b'+')
            throttle_down_key = KeyboardButton.ascii_key(b'-')
            break_key = KeyboardButton.ascii_key(b'b')
            if base.mouseWatcherNode.is_button_down(throttle_up_key):
                entity[MovingMass].forward_force = min(4000, entity[MovingMass].forward_force + 100.0)
            if base.mouseWatcherNode.is_button_down(throttle_down_key):
                entity[MovingMass].forward_force = max(0, entity[MovingMass].forward_force - 100.0)
            if base.mouseWatcherNode.is_button_down(break_key):
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
