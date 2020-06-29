from direct.particles import ParticleEffect
from panda3d.core import KeyboardButton
from wecs.core import Component, System, and_filter
from wecs.panda3d import Model

LASER_KEY = KeyboardButton.ascii_key('l')


@Component()
class Smoking:
    particle_mgr: ParticleEffect = None


class SmokeSystem(System):
    entity_filters = {
        'smokers': and_filter([Smoking, Model])
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['smokers']:
            print(f"smoke:{entity}")


@Component()
class Living:
    hp: int = 100
    accum_damage: int = 0


class LifeSystem(System):
    entity_filters = {
        'mortals': and_filter([Living, Model])
    }

    def enter_filter_mortals(self, entity):
        mortal = entity[Living]
        print(mortal)

    def update(self, entities_by_filter):
        for mortal in entities_by_filter['mortals']:
            model = mortal[Model]
            living = mortal[Living]
            if living.accum_damage > 0:
                living.hp -= living.accum_damage
                # print(f"got {living.accum_damage} damage. HP:{living.hp}")
                living.accum_damage = 0
                if living.hp < 0:
                    print("BOOM")
                    model.node.set_r(160)
                    del mortal[Living]


@Component()
class TakesDamage:
    size: int = 2


