from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Position

from movement import Movement


@Component()
class Tank:
    # size: float = 0.2
    weight: int = 1


class GiveTankMoveCommands(System):
    entity_filters = {
        # 'tanks': Tank

        'tanks': and_filter([
            Movement,
            Tank,
        ]),
    }

    # noinspection PyArgumentList
    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:
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

            if position.value.y >= 30:
                position.value.y = 30
            elif position.value.y <= -30:
                position.value.y = -30

            if position.value.x >= 30:
                position.value.x = 30
            elif position.value.x <= -30:
                position.value.x = -30
