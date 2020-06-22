from panda3d.core import loadPrcFileData
# loadPrcFileData("", "want-directtools #t")
# loadPrcFileData("", "want-tk #t")
loadPrcFileData("", "win-origin 1000 400")
loadPrcFileData("", "window-title TANKS")
loadPrcFileData("", "audio-library-name null")
loadPrcFileData("", "show-frame-rate-meter true")

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
