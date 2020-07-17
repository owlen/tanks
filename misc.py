from direct.particles.ParticleEffect import ParticleEffect
from panda3d.core import TextNode
from wecs.core import Component, System, and_filter
from wecs.panda3d import Model, Position, sqrt

from heat import Platform


@Component()
class Smoking:
    particle_mgr: ParticleEffect = None


class SmokeSystem(System):
    entity_filters = {
        'smokers': and_filter([Smoking, Model])
    }

    def enter_filter_smokers(self, entity):
        model = entity[Model]

        p = ParticleEffect()
        p.loadConfig('resources/smoke.ptf')
        p.start(parent=model.node, renderParent=render)
        p.set_z(3)
        # p0 = p.getParticlesList()[0]
        # p0.emitter.setOffsetForce(LVector3(0.0000, 0.0000, 3.0000))
        entity[Smoking].particle_mgr = p

    def update(self, entities_by_filter):
        for entity in entities_by_filter['smokers']:
            if Life in entity:
                entity[Smoking].rate = 10 - sqrt(entity[Life].hp)  # todo do something w this


@Component()
class TakesDamage:
    sphere_size: int = 2
    target_np = None


@Component()
class TextLabel:
    text: str = 'not set!'
    text_node: TextNode = None


class TextLabelSystem(System):
    entity_filters = {
        'labels': and_filter([TextLabel, Model])
    }

    def enter_filter_labels(self, entity):
        model = entity[Model]
        text = entity[TextLabel].text
        entity[TextLabel].text_node = TextNode('text node')
        entity[TextLabel].text_node.setText(text)
        entity[TextLabel].text_node.setAlign(TextNode.ACenter)
        entity[TextLabel].text_node.setTextColor(1, 1, 0.2, 1)
        # entity[TextLabel].text_node.setShadow(0.05, 0.05)
        # entity[TextLabel].text_node.setShadowColor(0.2, 0.2, 1, 1)

        text_node_path = model.node.attachNewNode(entity[TextLabel].text_node)
        text_node_path.setScale(2)
        text_node_path.set_pos(0, 0, 4)
        text_node_path.setBillboardPointEye()

    def update(self, entities_by_filter):
        for entity in entities_by_filter['labels']:
            entity[TextLabel].text_node.setText(entity[TextLabel].text)


@Component()
class Life:
    hp: int = 100
    accum_damage: int = 0
    alive: bool = True
    is_alive = True
    report_hp = None


class LifeSystem(System):
    entity_filters = {
        'mortals': and_filter([Life, Model])}

    def enter_filter_mortals(self, entity):  # todo remove
        mortal = entity[Life]

    def update(self, entities_by_filter):
        for mortal in entities_by_filter['mortals']:
            living = mortal[Life]
            if living.accum_damage > 0:
                living.hp -= living.accum_damage
                living.accum_damage = 0
            if TextLabel in mortal:
                mortal[TextLabel].text = f"hp:{mortal[Life].hp} t:{mortal[Platform].temp:.1f}"


@Component()
class Msg:
    msg: str = "."  # mass - Kg
    rate: int = 30  # print every
    rate_c: int = 0


class PrintMsg(System):
    entity_filters = {
        'print': and_filter([Position, Msg, ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['print']:
            if entity[Msg].rate < 1:
                continue
            entity[Msg].rate_c += 1
            if entity[Msg].rate_c % entity[Msg].rate == 0:
                print(f"msg:{entity}, {entity[Msg].msg}")


