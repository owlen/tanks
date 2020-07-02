from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Model

import game
from laser import LaserGun
from misc import Living, TakesDamage, TextLabel, Smoking
from movement import MovingMass

BREAK_KEY = KeyboardButton.ascii_key('b')
THROTTLE_UP_KEY = KeyboardButton.ascii_key('+')
THROTTLE_DOWN_KEY = KeyboardButton.ascii_key('-')


@Component()
class Tank:
    # size: float = 0.2
    weight: int = 1


class GiveTankMoveCommands(System):
    entity_filters = {
        # 'tanks': Tank

        'tanks': and_filter([MovingMass, Tank, Living]),
    }

    def enter_filter_tanks(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:
            if entity[Living].hp < 0:
                continue

            # What keys does the player use?
            up_key = KeyboardButton.ascii_key(b'w')
            down_key = KeyboardButton.ascii_key(b's')

            # Read player input
            delta = 0
            if game.base.mouseWatcherNode.is_button_down(up_key):
                delta += 1
            if game.base.mouseWatcherNode.is_button_down(down_key):
                delta -= 1

            # Store movement
            # movement.value.y = delta

            if game.base.mouseWatcherNode.is_button_down(THROTTLE_UP_KEY):
                entity[MovingMass].forward_force = min(4000, entity[MovingMass].forward_force + 100.0)
            if game.base.mouseWatcherNode.is_button_down(THROTTLE_DOWN_KEY):
                entity[MovingMass].forward_force = max(0, entity[MovingMass].forward_force - 100.0)
            if game.base.mouseWatcherNode.is_button_down(BREAK_KEY):
                entity[MovingMass].break_force = 10000
            else:
                entity[MovingMass].break_force = 0


class TankTouchesBoundary(System):
    entity_filters = {
        'tanks': and_filter([MovingMass, Tank])
    }

    arena_radius = 50

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):

            distance = entity[Model].node.getPos().length()

            if distance > self.arena_radius:
                print(f"  out  {entity} distance: {distance}")


class HandleTankDestruction(System):
    entity_filters = {'tanks': and_filter([Tank, Living])}

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):
            living = entity[Living]
            if living.hp <= 0:
                print(f"tank: {entity} is dead")
                if Smoking not in entity:
                    entity[Smoking] = Smoking()
                if TextLabel in entity:
                    entity[TextLabel].text = 'XXX'
                del entity[Living]
                if LaserGun in entity:
                    del entity[LaserGun]
                if TakesDamage in entity:
                    del entity[TakesDamage]
                if MovingMass in entity:  # fixme still doesn't stop
                    entity[MovingMass].friction *= 15
                    entity[MovingMass].turn /= 2
                    entity[MovingMass].velocity /= 2
                else:
                    print(f"{entity} is not MovingMass but alive?")
