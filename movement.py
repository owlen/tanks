from direct.showbase.ShowBaseGlobal import globalClock
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Position


@Component()
class Msg:
    msg: str = "."  # mass - Kg
    rate: int = 30  # print every
    rate_c: int = 0


class PrintMsg(System):
    entity_filters = {
        'print': and_filter([
            Position,
            Msg,
        ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['print']:
            if entity[Msg].rate < 1:
                continue
            entity[Msg].rate_c += 1
            if entity[Msg].rate_c % entity[Msg].rate == 0:
                print(f"msg:{entity}, {entity[Msg].msg}")


@Component()
class MovingMass:
    mass: int  # mass - Kg
    angle: float = 0  # heading - degrees
    turn: int = 3  # max turn ability - Degrees/m
    velocity: int = 1  # velocity - m/sec
    acceleration: float = 0  # m/sec**2
    forward_force = 1000  # force ??
    friction = 100  # force


class MoveMassSystem(System):
    entity_filters = {
        'move': and_filter([
            Position,
            MovingMass,
            Msg,
        ]),
    }

    def update(self, entities_by_filter):
        dt = globalClock.dt
        for entity in entities_by_filter['move']:
            mass = entity[MovingMass]
            model = entity[Model]

            # air_resistance grow at speed^2 times aerodynamic_factor
            aerodynamic_factor = 2
            air_resistance = mass.velocity ** 2 * aerodynamic_factor
            # resultant force is sum of forces
            resultant_force = mass.forward_force - air_resistance - mass.friction
            # velocity grows by acceleration*dt, can't be negative
            mass.acceleration = resultant_force / mass.mass
            mass.velocity = max(0, mass.velocity + mass.acceleration * dt)
            entity[Msg].msg = f"Weight:{mass.mass:>4} speed:{mass.velocity: >6.2f} accel:{mass.acceleration:.2f} " \
                              f"force:{mass.forward_force} " \
                              f"resultant_force:{resultant_force:.2f}"

            # turn based on speed
            mass.angle += mass.turn * mass.velocity * dt
            model.node.set_h(mass.angle)

            model.node.set_pos(model.node, (0, mass.velocity * dt, 0))

# Yes, nodepath.set_pos(nodepath, (0, 1, 0)) will move it forward by
# 1 unit relative to its own coordinate system, which will include its rotation
# There are other ways to do it, like 
# nodepath.parent.get_relative_vector(nodepath, (0, 1, 0)) or 
# nodepath.get_quat().get_forward() which both get the forward vector.
