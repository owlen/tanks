from panda3d.core import Vec3
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Position
from wecs.panda3d import Scene


@Component
class MovingMass:
    dir: Vec3
    # weight: int = 1
    # speed: float = 0


@Component()
class Movement2:
    dir: Vec3


@Component()
class Movement:
    value: Vec3


class MoveObject(System):
    entity_filters = {
        'move': and_filter([
            Model,
            Scene,
            Position,
            Movement,
        ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['move']:
            position = entity[Position]
            movement = entity[Movement]
            model = entity[Model]

            position.value += movement.value * globalClock.dt
            model.node.set_pos(position.value)
            model.node.set_h(model.node.get_h()+1)
