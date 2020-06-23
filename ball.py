from panda3d.core import KeyboardButton
from panda3d.core import Vec3
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Position
from wecs.panda3d import Scene

from movement import Movement


@Component()
class Ball:
    pass


@Component()
class Resting:
    pass


class BallTouchesBoundary(System):
    entity_filters = {
        'ball': and_filter([
            Model,
            Scene,
            Position,
            Movement,
            Ball,
        ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['ball']:
            model = entity[Model]
            movement = entity[Movement]

            # The ball's size is assumed to be 0.1, and if it moved over
            # the upper or lower boundary (1 / -1), we reflect it.
            z = model.node.get_z()
            if z > 0.9:
                model.node.set_z(0.9 - (z - 0.9))
                movement.value.z = -movement.value.z
            if z < -0.9:
                model.node.set_z(-0.9 - (z + 0.9))
                movement.value.z = -movement.value.z


class StartBallMotion(System):
    entity_filters = {
        'ball': and_filter([
            Model,
            Scene,
            Position,
            Resting,
            Ball,
        ]),
    }

    def update(self, entities_by_filter):
        # Should resting balls be started?
        start_key = KeyboardButton.space()
        start_balls = base.mouseWatcherNode.is_button_down(start_key)

        if start_balls:
            for entity in set(entities_by_filter['ball']):
                del entity[Resting]
                entity[Movement] = Movement(value=Vec3(-1, 0, 0))
