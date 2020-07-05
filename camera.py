from direct.showbase.ShowBaseGlobal import globalClock
from panda3d.core import Vec3, KeyboardButton
from wecs.core import Component, System, and_filter
from wecs.panda3d import Model

import game

ZOOM_IN_KEY = KeyboardButton.ascii_key('z')
ZOOM_OUT_KEY = KeyboardButton.ascii_key('x')
LOOK_AT_KEY = KeyboardButton.ascii_key('1')


@Component()
class LookAt:
    look_at: Model = None


class CameraSystem(System):
    entity_filters = {'follow': and_filter([LookAt, Model]),
                      }

    def enter_filter_follow(self, entity):
        entity[LookAt].look_at = entity[Model]

    def update(self, entities_by_filter):
        following = False
        for entity in entities_by_filter['follow']:
            look_at = entity[LookAt].look_at.node.get_pos()
            following = True
            break

        base = game.base
        camera = game.base.camera
        if base.mouseWatcherNode.hasMouse():
            x = base.mouseWatcherNode.getMouseX()
            y = base.mouseWatcherNode.getMouseY()
            if abs(x) > 0.7:
                camera.set_pos(camera, 20 * x * globalClock.dt, 0, 0)
            if abs(y) > 0.7 and camera.get_p() > -85:
                camera.set_pos(camera, 0, 0, 25 * y * globalClock.dt)
                if camera.get_z() < 1:
                    camera.set_z(1)

        if following:
            camera.lookAt(look_at)
        else:
            camera.lookAt(Vec3(0, 0, -10))

        zoom = base.camLens.get_fov()[0]
        if zoom < 70 and base.mouseWatcherNode.is_button_down(ZOOM_OUT_KEY):
            zoom = base.camLens.get_fov()[0] + 5 * globalClock.dt
        if zoom > 40 and base.mouseWatcherNode.is_button_down(ZOOM_IN_KEY):
            zoom = base.camLens.get_fov()[0] - 5 * globalClock.dt
        base.camLens.set_fov(zoom)
