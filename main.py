from panda3d.core import loadPrcFileData, Vec3, LPoint3f

# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "win-origin 1000 400")
loadPrcFileData("", "window-title TANKS")
loadPrcFileData("", "audio-library-name null")
loadPrcFileData("", "show-frame-rate-meter true")
# loadPrcFileData("", "win-size 600 400")

# noinspection PyPep8


def run_game():
    def heading(p1, p2):
        zero_heading = Vec3.forward()
        relative_vector = Vec3(p2 - p1).normalized()
        return zero_heading.signed_angle_deg(relative_vector, Vec3.down())

    for p in [(110, 10, 0), (90, 10, 0), (90, -10, 0), (110, -10, 0),
              (100, 5, 0), (105, 0, 0), (95, 0, 0), (100, -5, 0), ]:
        p1 = LPoint3f(100, 0, 0)
        p2 = LPoint3f(p)
        print(f"heading from (100, 0, 0) to {p}: {heading(p1, p2)} deg")

    # boilerplate.run_game(
    #     console=False,
    #     keybindings=False,
    #     debug_keys=True,
    #     simplepbr=False,
    # )


if __name__ == '__main__':
    run_game()

# dont forget
# primitives = loader.load_model("primitives.bam")
# cube = primitives.find("cube")
# cube.reparent_to(render)


# from panda3d.core import VBase4
# from panda3d.core import LineSegs
#
#
# segs = LineSegs()
# segs.set_thickness(2.0)
# segs.set_color(VBase4(1, 1, 1, 1))
# segs.move_to(0, 0, 0)
# segs.draw_to(0, 0, 1)
# base.render.attach_new_node(segs.create())
