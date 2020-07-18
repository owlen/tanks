from panda3d.core import LPoint3f, Vec3
from wecs.core import Component, and_filter
from wecs.panda3d import Model, Position, or_filter

from heat import Platform
from misc import SlowSystem
from tank import Tank
from turret import Turret


@Component()
class FrontRadar:
    range: int = 60
    ray_np = None
    laser_np = None
    temp: int = 99
    mass: int = 100
    platform = None
    open_deg: int = 15  # range in degrees both left and right
    report_temp = None
    blips = None
    report_sees = None

def deg(lp: LPoint3f, bp: LPoint3f):
    vec1 = Vec3(lp).normalized()
    vec2 = Vec3(bp).normalized()
    angle = vec1.angle_deg(vec2)
    print(f"between:{lp, bp} angle:{angle}")
    return angle


def heading(p1, p2):
    zero_heading = Vec3(0, 0, 0).forward().get_xy()
    relative_vector = Vec3(p2 - p1).get_xy()
    degrees = zero_heading.signed_angle_deg(relative_vector)
    return degrees


def get_radar_info(scanner, blipper):
    print(f"find data between {scanner} and {blipper}")
    scanner_np = scanner[Model].node
    blipper_np = blipper[Model].node
    print(f"scanner: {scanner} pos:{scanner_np.get_pos()} heading:{scanner_np.get_h()}")
    print(f"blipper: {blipper} pos:{blipper_np.get_pos()} heading:{blipper_np.get_h()}")
    distance_to_blipper = scanner_np.get_distance(blipper_np)
    xy = Vec3(0, 0, 0).forward().get_xy()
    direction = (scanner_np.get_pos().get_xy() - blipper_np.get_pos().get_xy()).signed_angle_deg(xy)
    print(f"direction: {scanner_np.get_h(blipper_np)} distance: {distance_to_blipper}")


class RadarSystem(SlowSystem):
    blippers = []
    blips_by_scanner = {}
    entity_filters = {
        'radars': and_filter([FrontRadar, Platform, Model]),
        'blippers': and_filter([Position, or_filter(Tank, Turret)]),
    }

    def slow_update(self, entities_by_filter):
        print(f"\nblippers: {entities_by_filter['blippers']}")
        for scanner in entities_by_filter['radars']:
            self.blips_by_scanner[scanner] = []
            for blipper in entities_by_filter['blippers']:
                if scanner is blipper:
                    continue
                self.blips_by_scanner[scanner].append(get_radar_info(scanner, blipper))
        print(self.blips_by_scanner)

        # for radar in entities_by_filter['radars']:
        #     radar_node = radar[Model].node
        #     rdr_pos = radar_node.get_pos()
        #     rdr_heading = radar_node.get_h()
        #     radar[FrontRadar].blips = []
        #     for blipper, direction in self.blips_by_scanner[radar]:
        #         delta = direction - rdr_heading
        #         if delta > 180:
        #             delta = (360 - delta) % 360
        #         print(f"radar ar {rdr_pos} heading:{rdr_heading:.1f} sees:{direction:.1f} delta: {delta:.1f}")
        #         if abs(delta) < radar[FrontRadar].open_deg:
        #             distance = (rdr_pos - blipper[Position].value).length()
        #             print(f"SEE!!! {blipper} distance:{distance}")
        #             radar[FrontRadar].blips.append((direction, distance))
