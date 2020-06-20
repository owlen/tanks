from wecs.core import Component, and_filter
from wecs.core import System
from wecs.panda3d import Model


@Component()
class Tank:
    # size: float = 0.2
    weight: int = 2000


class GiveTankMoveCommands(System):
    entity_filters = {
        'tanks': Tank

        # 'tanks': and_filter([
        #     Model,
        #     Tankk
        # ]),
    }

    def update(self, entities_by_filter):
        for entity in entities_by_filter['tanks']:
            if Tank not in entity:
                print(f"wrong entity is given! {entity.get_components()}")
            else:
                print(f"Valid entity is given! {entity.get_components()}")


