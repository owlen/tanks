from panda3d.core import KeyboardButton
from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Position, Model
from direct.particles.ParticleEffect import ParticleEffect, LinearVectorForce, LVector3

# from movement import Movement
from movement import MovingMass


@Component()
class Duster:
    particleMgr: ParticleEffect = None
    dustFactor: int = 1


class DustSystem(System):
    entity_filters = {
        'dusters': and_filter([
            Duster,
            Model,
            MovingMass,
        ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['dusters']:
            duster = entity[Duster]
            moving = entity[MovingMass]
            print(f"dust: factor:{duster.dustFactor} birth:{duster.dustFactor/moving.velocity:.3f}")
            duster.particleMgr.getParticlesList()[0].setBirthRate(duster.dustFactor / moving.velocity)

    def enter_filter_dusters(self, entity):
        print('in enter_filter_dusters')
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

        p = ParticleEffect()
        p.loadConfig('resources/dust.ptf')
        p.start(parent=model.node, renderParent=render)
        p.set_y(-3)
        p0 = p.getParticlesList()[0]
        p0.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 2.0000))
        p.softStart(1)
        entity[Duster].particleMgr = p
        entity[Duster].dustFactor = 1000/entity[MovingMass].mass


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
