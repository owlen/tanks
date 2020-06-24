from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import LVector3
from wecs.core import Component, System, and_filter
from wecs.panda3d import Model

from movement import MovingMass


@Component()
class Duster:
    particleMgr: ParticleEffect = None
    dustFactor: int = 1


class DustSystem(System):
    """Makes dust come out of :Duster: entities who are :MovingMass: and have :Model:"""
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
            if duster.particleMgr.isEnabled():
                if moving.velocity < 2:
                    duster.particleMgr.disable()
                else:
                    # TODO should be acceleration * mass
                    r = duster.dustFactor / moving.velocity
                    duster.particleMgr.getParticlesList()[0].setBirthRate(r)
            elif moving.velocity > 3:
                # duster.particleMgr.enable()
                duster.particleMgr.start(parent=entity[Model].node, renderParent=render)

    def enter_filter_dusters(self, entity):
        model = entity[Model]
        model.node.set_hpr(0, 0, 0)

        p = ParticleEffect()
        p.loadConfig('resources/dust.ptf')
        # p.start(parent=model.node, renderParent=render)
        p.set_y(-3)
        p0 = p.getParticlesList()[0]
        p0.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 2.0000))
        entity[Duster].particleMgr = p
        entity[Duster].dustFactor = 1000 / entity[MovingMass].mass
