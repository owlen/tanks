from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Model

import game
from DustSytem import Smoking
from laser import LaserGun
from misc import Living, TakesDamage, Smoking
from propulsion import Propulsion, KbdControlled

BREAK_KEY = KeyboardButton.ascii_key('b')
THROTTLE_UP_KEY = KeyboardButton.ascii_key('+')
THROTTLE_DOWN_KEY = KeyboardButton.ascii_key('-')


@Component()
class Tank:
    weight: int = 1


class GiveTankMoveCommands(System):
    entity_filters = {
        # 'tanks': Tank

        'tanks': and_filter([Propulsion, Tank, Living]),
    }

    def enter_filter_tanks(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:

            if game.base.mouseWatcherNode.is_button_down(THROTTLE_UP_KEY):
                entity[Propulsion].forward_force = min(4000, entity[Propulsion].forward_force + 100.0)
            if game.base.mouseWatcherNode.is_button_down(THROTTLE_DOWN_KEY):
                entity[Propulsion].forward_force = max(0, entity[Propulsion].forward_force - 100.0)
            if game.base.mouseWatcherNode.is_button_down(BREAK_KEY):
                entity[Propulsion].break_force = 10000
            else:
                entity[Propulsion].break_force = 0


class HandleTankDestruction(System):
    entity_filters = {'tanks': and_filter([Tank, Living])}

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):
            living = entity[Living]
            if living.hp <= 0:
                print(f"tank: {entity} is dead")
                if Smoking not in entity:
                    entity[Smoking] = Smoking()
                del entity[Living]
                if LaserGun in entity:
                    del entity[LaserGun]
                if TakesDamage in entity:
                    del entity[TakesDamage]
                if KbdControlled in entity:
                    del entity[KbdControlled]
                if Propulsion in entity:  # fixme still doesn't stop
                    entity[Propulsion].friction *= 15
                    entity[Propulsion].turn /= 2
                    entity[Propulsion].velocity /= 2
                else:
                    print(f"{entity} is not MovingMass but alive?")
