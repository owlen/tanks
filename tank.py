import pdb

from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Position, Model

from movement import Movement


@Component()
class Tank:
    # size: float = 0.2
    weight: int = 2000


class GiveTankMoveCommands(System):
    entity_filters = {
        'tanks': Tank

        # 'tanks': and_filter([
        #     Movement,
        #     Tank,
        # ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:
            print(entity.get_components())
            movement = entity[Movement]

            # What keys does the player use?
            up_key = KeyboardButton.ascii_key(b'w')
            down_key = KeyboardButton.ascii_key(b's')

            # Read player input
            delta = 0
            if base.mouseWatcherNode.is_button_down(up_key):
                delta += 1
                print(f"move {entity[Tank]}")
            if base.mouseWatcherNode.is_button_down(down_key):
                delta -= 1

            # Store movement
            movement.value.y = delta


class TankTouchesBoundary(System):
    entity_filters = {
        # 'tanks': and_filter([Position, Tank])
        'tanks': Tank
    }

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):
            # pdb.set_trace()
            position = entity[Position]
            print(position)

            if position.value.z >= 30:
                position.value.z = 30
            elif position.value.z <= -30:
                position.value.z = -30

            if position.value.x >= 30:
                position.value.x = 30
            elif position.value.x <= -30:
                position.value.x = -30
