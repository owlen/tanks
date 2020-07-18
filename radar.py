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
    sees = None
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


class RadarSystem(SlowSystem):
    blippers = []
    sees_at = {}
    entity_filters = {
        'radars': and_filter([FrontRadar, Platform, Model]),
        'blippers': and_filter([Position, or_filter(Tank, Turret)]),
    }

    def enter_filter_blippers(self, entity):
        print(f"adding blipper: {entity}")
        self.blippers.append(entity)

        # for p in [(110, 10, 0), (90, 10, 0), (90, -10, 0), (110, -10, 0),
        #           (100, 5, 0), (105, 0, 0), (95, 0, 0), (100, -5, 0), ]:
        #     p1 = LPoint3f(100, 0, 0)
        #     p2 = LPoint3f(p)
        #     print(f"heading from (100, 0, 0) to {p}: {heading(p1, p2)} deg")
        # exit()

    def slow_update(self, entities_by_filter):
        # print(f"\nblippers: {self.blippers}")
        for looker in self.blippers:
            self.sees_at[looker] = []
            for blipper in self.blippers:
                if looker is blipper:
                    continue
                lp = looker[Position].value
                bp = blipper[Position].value
                direction = heading(lp, bp)
                self.sees_at[looker].append((blipper, direction))
        # print(self.sees_at)

        for radar in entities_by_filter['radars']:
            rdr_pos = radar[Position].value
            rdr_heading = radar[Model].node.get_h()
            radar[FrontRadar].sees = []
            for blipper, direction in self.sees_at[radar]:
                delta = direction - rdr_heading
                if delta > 180:
                    delta = (360 - delta) % 360
                print(f"radar ar {rdr_pos} heading:{rdr_heading:.1f} sees:{direction:.1f} delta: {delta:.1f}")
                if abs(delta) < radar[FrontRadar].open_deg:
                    distance = (rdr_pos - blipper[Position].value).length()
                    print(f"SEE!!! {blipper} distance:{distance}")
                    radar[FrontRadar].sees.append((direction, distance))
