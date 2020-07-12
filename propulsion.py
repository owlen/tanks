from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import KeyboardButton
from wecs.core import Component
from wecs.core import System
from wecs.core import and_filter
from wecs.panda3d import Model
from wecs.panda3d import Position

import game
from heat import Platform
from misc import Msg


@Component()
class Propulsion:
    heading: float = 0  # heading - degrees
    min_turn_radius: int = 10  # how tight it can turn? max turn ability - Degrees/m
    turn: int = 180 / (min_turn_radius * 3.1413)  # actual turning
    velocity: int = 1  # velocity - m/sec
    acceleration: float = 0  # m/sec**2
    forward_force = 1000  # force ??
    break_force = 0
    friction = 100  # force


class PropulsionSystem(System):
    entity_filters = {
        'movers': and_filter([
            Position,
            Platform,
            Propulsion,
            Msg,
        ]),
    }

    def update(self, entities_by_filter):
        dt = globalClock.dt
        for entity in entities_by_filter['movers']:
            moving_mass = entity[Propulsion]
            model = entity[Model]
            mass = entity[Platform].mass  # connect to host platform

            # air_resistance grow at speed^2 times aerodynamic_factor
            aerodynamic_factor = 2
            air_resistance = moving_mass.velocity ** 2 * aerodynamic_factor
            # resultant force is sum of forces
            resultant_force = \
                moving_mass.forward_force - air_resistance - moving_mass.friction - moving_mass.break_force
            # velocity grows by acceleration*dt, can't be negative
            moving_mass.acceleration = resultant_force / mass
            moving_mass.velocity = max(0, moving_mass.velocity + moving_mass.acceleration * dt)

            # limit turn rate
            moving_mass.turn = min(moving_mass.turn, 180 / (moving_mass.min_turn_radius * 3.1413))
            moving_mass.turn = max(moving_mass.turn, -180 / (moving_mass.min_turn_radius * 3.1413))
            # turn based on speed
            moving_mass.heading += moving_mass.turn * moving_mass.velocity * dt
            model.node.set_h(moving_mass.heading)

            model.node.set_pos(model.node, (0, moving_mass.velocity * dt, 0))

            entity[Position].value = entity[Model].node.getPos()

            entity[Msg].msg = f"Weight:{mass:>4} temp:{entity[Platform].temp} speed:{moving_mass.velocity: >6.2f} " \
                              f"turn: {moving_mass.turn}"
            # f"accel:{moving_mass.acceleration:.2f} " f"force:{moving_mass.forward_force} " \
            # f"resultant_force:{resultant_force:.2f}  - {moving_mass.acceleration * mass}"


@Component()
class KbdControlled:
    keys: str = 'ad '
    turn_rate: int = 10


class KbsControlSystem(System):
    entity_filters = {"controlled": and_filter([KbdControlled, Propulsion])}

    def update(self, entities_by_filter):
        for entity in entities_by_filter['controlled']:
            controlled = entity[KbdControlled]
            moving = entity[Propulsion]
            t = moving.turn
            key_left, key_right, key_laser = controlled.keys
            if t > -20 and game.base.mouseWatcherNode.is_button_down(KeyboardButton.ascii_key(key_right)):
                t -= controlled.turn_rate * globalClock.dt
            if t < 20 and game.base.mouseWatcherNode.is_button_down(KeyboardButton.ascii_key(key_left)):
                t += controlled.turn_rate * globalClock.dt
            moving.turn = t
