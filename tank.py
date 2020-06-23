from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Position, Model
from direct.particles.ParticleEffect import ParticleEffect, LinearVectorForce, LVector3

# from movement import Movement
from movement import MovingMass


@Component()
class Smoker:
    pass




@Component()
class Tank:
    # size: float = 0.2
    weight: int = 1


class GiveTankMoveCommands(System):
    entity_filters = {
        # 'tanks': Tank

        'tanks': and_filter([
            MovingMass,
            Tank,
        ]),
    }

    def enter_filter_tanks(self, entity):
        print('in enter_filter_tanks')
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

        p = ParticleEffect()
        p.loadConfig('resources/dust.ptf')
        p.start(parent=model.node, renderParent=render)
        p.set_y(-3)
        p.getParticlesList()[0].emitter.setOffsetForce(LVector3(0.0000, 0.0000, 2.0000))
        print(p.getForceGroupDict())
        print(p.getForceGroupList()[0])
        print(p.getForceGroupNamed('gravity'))
        p.disable()
        p.softStart(1)
        p.removeAllForces()
        p.start(parent=model.node, renderParent=render)
        p.enable()


    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:
            # movement = entity[Movement]

            # What keys does the player use?
            up_key = KeyboardButton.ascii_key(b'w')
            down_key = KeyboardButton.ascii_key(b's')

            # Read player input
            delta = 0
            if base.mouseWatcherNode.is_button_down(up_key):
                delta += 1
                print(f"move {entity[Tank]}")
            if base.mouseWatcherNode.is_button_down(down_key):
                delta -= 1

            # Store movement
            # movement.value.y = delta

            throttle_key = KeyboardButton.ascii_key(b'+')
            break_key = KeyboardButton.ascii_key(b'-')
            if base.mouseWatcherNode.is_button_down(throttle_key):
                entity[MovingMass].forward_force = min(4000, entity[MovingMass].forward_force + 100.0)
            if base.mouseWatcherNode.is_button_down(break_key):
                entity[MovingMass].forward_force = max(0, entity[MovingMass].forward_force - 100.0)


class TankTouchesBoundary(System):
    entity_filters = {
        # 'tanks': and_filter([Position, Tank])
        'tanks': Tank
    }

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['tanks']):
            # pdb.set_trace()
            position = entity[Position]

            if position.value.y >= 30:
                position.value.y = 30
            elif position.value.y <= -30:
                position.value.y = -30

            if position.value.x >= 30:
                position.value.x = 30
            elif position.value.x <= -30:
                position.value.x = -30
