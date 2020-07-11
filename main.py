from panda3d.core import loadPrcFileData

# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "win-origin 1000 400")
loadPrcFileData("", "window-title TANKS")
loadPrcFileData("", "audio-library-name null")
loadPrcFileData("", "show-frame-rate-meter true")
# loadPrcFileData("", "win-size 600 400")

# noinspection PyPep8
from wecs import boilerplate


def run_game():
    boilerplate.run_game(
        console=False,
        keybindings=False,
        debug_keys=True,
        simplepbr=False,
    )


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
