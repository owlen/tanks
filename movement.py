from direct.showbase.ShowBaseGlobal import globalClock
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Position


@Component()
class MovingMass:
    mass: int  # mass - Kg
    angle: float = 0  # heading - degrees
    max_turn: int = 30  # max turn ability - Degreesd/sec
    velocity: int = 15  # velocity - m/sec
    friction: float = 2  # m/sec**2
    acceleration: float = 4  # m/sec**2


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
            mass = entity[MovingMass]
            model = entity[Model]

            drag = 0

            # velocity grows by acceleration*dt, can't be negative
            mass.velocity = max(0, mass.velocity + mass.acceleration * dt - drag*dt)
            # Acceleration drops by friction*dt. Deceleration can't be higher than velocity
            mass.acceleration = max(mass.acceleration - mass.friction * dt, -1 * mass.velocity)
            print(f"speed:{mass.velocity} acceleration:{mass.acceleration}")

            # just turn around if moving
            mass.angle += 30 * dt * (mass.velocity > 0)

            model.node.set_pos(model.node, (0, mass.velocity * dt, 0))
            model.node.set_h(mass.angle)

# Yes, nodepath.set_pos(nodepath, (0, 1, 0)) will move it forward by
# 1 unit relative to its own coordinate system, which will include its rotation
# There are other ways to do it, like 
# nodepath.parent.get_relative_vector(nodepath, (0, 1, 0)) or 
# nodepath.get_quat().get_forward() which both get the forward vector.
