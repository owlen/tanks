from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Scene
from wecs.panda3d import Position

from movement import Movement
from movement import Players


@Component()
class Tank:
    player: int
    size: float = 0.2
    weight: int = 2000


class GiveTankMoveCommands(System):
    entity_filters = {
        'tank': and_filter([
            Model,
            Scene,
            Position,
            Movement,
            Tank,
        ]),
    }

    def enter_filter_model(self, entity):
        geometry = entity[Geometry]
        print(geometry)

    def update(self, entities_by_filter):
        for entity in entities_by_filter['tank']:
            tank = entity[Tank]
            movement = entity[Movement]

            # What keys does the player use?
            if tank.player == Players.LEFT:
                up_key = KeyboardButton.ascii_key(b'w')
                down_key = KeyboardButton.ascii_key(b's')
            elif tank.player == Players.RIGHT:
                up_key = KeyboardButton.up()
                down_key = KeyboardButton.down()

            # Read player input
            delta = 0
            if base.mouseWatcherNode.is_button_down(up_key):
                delta += 1
            if base.mouseWatcherNode.is_button_down(down_key):
                delta -= 1

            # Store movement
            movement.value.z = delta


class TankTouchesBoundary(System):
    entity_filters = {
        'tanks': and_filter([
            Model,
            Scene,
            Position,
            Tank,
        ]),
    }

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):
            model = entity[Model]
            position = entity[Position]
            tank = entity[Tank]

            z = position.value.z
            size = tank.size

            if z + size > 1:
                position.value.z = 1 - size
            elif (z - size) < -1:
                position.value.z = -1 + size
            model.node.set_z(position.value.z)
