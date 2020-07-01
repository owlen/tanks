from direct.showbase.ShowBaseGlobal import globalClock
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model, sqrt
from wecs.panda3d import Position

from misc import Living


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
    heading: float = 0  # heading - degrees
    min_turn_radius: int = 10  # how tight it can turn?
    turn: int = 180 / (min_turn_radius * 3.1413)  # 3  # max turn ability - Degrees/m
    velocity: int = 1  # velocity - m/sec
    acceleration: float = 0  # m/sec**2
    forward_force = 1000  # force ??
    break_force = 0
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
            moving_mass = entity[MovingMass]
            model = entity[Model]

            if Living in entity and entity[Living].hp <= 0:
                if moving_mass.velocity > 0:
                    moving_mass.forward_force = 0
                    moving_mass.friction *= 15
                    moving_mass.turn /= 2

            # air_resistance grow at speed^2 times aerodynamic_factor
            aerodynamic_factor = 2
            air_resistance = moving_mass.velocity ** 2 * aerodynamic_factor
            # resultant force is sum of forces
            resultant_force = \
                moving_mass.forward_force - air_resistance - moving_mass.friction - moving_mass.break_force
            # velocity grows by acceleration*dt, can't be negative
            moving_mass.acceleration = resultant_force / moving_mass.mass
            moving_mass.velocity = max(0, moving_mass.velocity + moving_mass.acceleration * dt)
            entity[Msg].msg = f"Weight:{moving_mass.mass:>4} speed:{moving_mass.velocity: >6.2f} " \
                              f"accel:{moving_mass.acceleration:.2f} " f"force:{moving_mass.forward_force} " \
                              f"resultant_force:{resultant_force:.2f}  - {moving_mass.acceleration * moving_mass.mass}"

            # turn based on speed
            moving_mass.heading += moving_mass.turn * moving_mass.velocity * dt
            model.node.set_h(moving_mass.heading)

            model.node.set_pos(model.node, (0, moving_mass.velocity * dt, 0))

            x = entity[Model].node.getX()
            y = entity[Model].node.getY()
            entity[Msg].msg += f" dis: {sqrt(x * x + y * y)}"

            entity[Position].value = entity[Model].node.getPos()
