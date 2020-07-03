from direct.showbase.ShowBaseGlobal import globalClock
from wecs.core import and_filter, System, Component
from wecs.panda3d import Model

from laser import LaserGun
from misc import Living, Smoking, TakesDamage


@Component()
class Turret:
    rotate_speed: int = 10
    heading: float = 0  # heading - degrees


class OperateTurrets(System):
    entity_filters = {'turrets': and_filter([Turret, Living, Model])}

    def enter_filter_turrets(self, entity):
        model = entity[Model]
        model.node.set_hpr(45, 45, 0)

    def update(self, entities_by_filter):
        for entity in entities_by_filter['turrets']:
            model = entity[Model]
            model.node.set_h(model.node, entity[Turret].rotate_speed * globalClock.dt)


class HandleTurretDestruction(System):
    entity_filters = {'turrets': and_filter([Turret, Living])}

    def update(self, entities_by_filter):
        for entity in set(entities_by_filter['turrets']):
            living = entity[Living]
            if living.hp <= 0:
                if Smoking not in entity:
                    entity[Smoking] = Smoking()
                del entity[Living]
                if LaserGun in entity:
                    del entity[LaserGun]
                if TakesDamage in entity:
                    del entity[TakesDamage]
