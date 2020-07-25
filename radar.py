from heat import Platform
from misc import SlowSystem
from tank import Tank
from turret import Turret
from wecs.core import Component, and_filter
from wecs.panda3d import Position, or_filter
from wecs.panda3d.prototype import Model


@Component()
class FrontRadar:
    range: int = 60
    helper_np = None
    temp: int = 99
    mass: int = 100
    open_deg: int = 15  # range in degrees both left and right
    report_temp = None
    blips = None


def get_radar_info(scanner, blipper):
    # print(f"find data between {scanner} and {blipper}")
    scanner_np = scanner[Model].node
    blipper_np = blipper[Model].node
    distance_to_blipper = scanner_np.get_distance(blipper_np)
    helper = scanner[FrontRadar].helper_np
    helper.headsUp(blipper_np)
    direction_to_blipper = helper.get_h()
    # print(f"direction: {direction_to_blipper} distance: {distance_to_blipper}")
    return direction_to_blipper, distance_to_blipper


class RadarSystem(SlowSystem):
    blippers = []
    blips_by_scanner = {}
    entity_filters = {
        'radars': and_filter([FrontRadar, Platform, Model]),
        'blippers': and_filter([Position, or_filter(Tank, Turret)]),
    }

    def enter_filter_radars(self, entity):
        entity[FrontRadar].helper_np = entity[Model].node.attach_new_node("helper")

    def slow_update(self, entities_by_filter):
        """
        Start by filling blips_by_scanner with info about all distances and directions between radar scanner and
        blipping entities.
        Continue by going over radars and updating blips that are withing the radar opening.
        """
        for scanner in entities_by_filter['radars']:
            self.blips_by_scanner[scanner] = []
            for blipper in entities_by_filter['blippers']:
                if scanner is blipper:
                    continue
                self.blips_by_scanner[scanner].append(get_radar_info(scanner, blipper))

        for radar in entities_by_filter['radars']:
            radar[FrontRadar].blips = []
            for direction, distance in self.blips_by_scanner[radar]:
                # print(f"radar ar {rdr_pos} sees: dir:{direction:.1f} distance: {distance:.1f}")
                opn = radar[FrontRadar].open_deg
                if opn > direction > -opn:
                    radar[FrontRadar].blips.append((direction, distance))
            if radar[FrontRadar].blips:
                print(radar[FrontRadar].blips)
