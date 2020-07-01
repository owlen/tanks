from direct.particles import ParticleEffect
from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import KeyboardButton, Vec3, TextNode
from wecs.core import Component, System, and_filter
from wecs.panda3d import Model

LASER_KEY = KeyboardButton.ascii_key('l')


@Component()
class LookAt:
    look_at = Vec3(0, 0, 0)


class CameraSystem(System):
    entity_filters = {"lookat": and_filter([LookAt, ])}

    def update(self, entities_by_filter):
        look_at = Vec3(0, 0, -10)
        for entity in entities_by_filter['lookat']:
            print(f"lookat:{entity[LookAt]}")
            look_at = entity[LookAt].look_at
        camera = base.camera
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
            if abs(x) > 0.7:
                camera.set_pos(camera, 20 * x * globalClock.dt, 0, 0)
                camera.lookAt(look_at)
            if abs(y) > 0.7:
                camera.set_pos(camera, 0, 0, 25 * y * globalClock.dt)
                if camera.get_z() < 1:
                    camera.set_z(1)

                camera.lookAt(0, 0, -10)


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
class TakesDamage:
    sphere_size: int = 2


@Component()
class TextLabel:
    text: str = 'not set!'
    text_node: TextNode = None


class TextLabelSystem(System):
    entity_filters = {
        'labels': and_filter([TextLabel, Model])
    }

    def enter_filter_labels(self, entity):
        print(entity[TextLabel])
        model = entity[Model]
        text = entity[TextLabel].text
        print(f"entered label. parent: {model}")
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
class Living:
    hp: int = 100
    accum_damage: int = 0
    alive: bool = True
    is_alive = True


class LifeSystem(System):
    entity_filters = {
        'mortals': and_filter([Living, Model])}

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
                if living.hp < 0:  # entity is dead
                    living.alive = False
                    print("BOOM")
                    model.node.set_r(160)
                    model.node.set_z(2)
                    del mortal[Living]
            if TextLabel in mortal:
                mortal[TextLabel].text = f"hp:{mortal[Living].hp}"
