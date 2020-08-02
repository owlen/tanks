from math import sqrt

from direct.particles.ParticleEffect import ParticleEffect
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import TextNode
from wecs.core import Component, System, and_filter
from wecs.panda3d import Position
from wecs.panda3d.prototype import Model

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
        # p0 = p.get_particles_list()[0]
        # p0.emitter.set_offset_force(LVector3(0.0000, 0.0000, 3.0000))
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
        entity[TextLabel].text_node.set_text(text)
        entity[TextLabel].text_node.set_align(TextNode.ACenter)
        entity[TextLabel].text_node.set_text_color(1, 1, 0.2, 1)
        # entity[TextLabel].text_node.set_shadow(0.05, 0.05)
        # entity[TextLabel].text_node.set_shadow_color(0.2, 0.2, 1, 1)

        text_node_path = model.node.attachNewNode(entity[TextLabel].text_node)
        text_node_path.set_scale(2)
        text_node_path.set_pos(0, 0, 4)
        text_node_path.set_billboard_point_eye()

    def update(self, entities_by_filter):
        for entity in entities_by_filter['labels']:
            entity[TextLabel].text_node.set_text(entity[TextLabel].text)


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


class SlowSystem(System):
    last_update = globalClock.get_frame_time()
    frequency: int = 0.5  # seconds

    def __init__(self, frequency=None):
        super().__init__()
        if frequency:
            self.frequency = frequency

    def update(self, entities_by_filter):
        if self.last_update + self.frequency > globalClock.get_frame_time():
            return
        self.last_update = globalClock.get_frame_time()
        self.slow_update(entities_by_filter)

    def slow_update(self, entities_by_filter):
        pass
