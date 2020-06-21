from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Vec3
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Position
from wecs.panda3d import Scene


@Component()
class MovingMass:
    mass: int  # mass - Kg
    angle: float = 0  # heading - degrees
    max_turn: int = 30  # max turn ability - Degreesd/sec
    speed: int = 15  #  speed - m/sec


class MoveMassSystem(System):
    entity_filters = {
        'move': and_filter([
            Position,
            MovingMass,
        ]),
    }

    def update(self, entities_by_filter):
        dt = globalClock.dt
        for entity in entities_by_filter['move']:
            position = entity[Position]
            entity[MovingMass].angle += 30*dt
            model = entity[Model]

            model.node.set_pos(model.node, (0, entity[MovingMass].speed*dt, 0))
            model.node.set_h(entity[MovingMass].angle)


# Yes, nodepath.set_pos(nodepath, (0, 1, 0)) will move it forward by 
# 1 unit relative to its own coordinate system, which will include its rotation
# There are other ways to do it, like 
# nodepath.parent.get_relative_vector(nodepath, (0, 1, 0)) or 
# nodepath.get_quat().get_forward() which both get the forward vector.


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
