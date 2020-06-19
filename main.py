from wecs import boilerplate


def run_game():
    boilerplate.run_game(
        console=False,
        keybindings=False,
        debug_keys=True
    )


if __name__ == '__main__':
    run_game()


# dont forget
# primitives = loader.load_model("primitives.bam")
# cube = primitives.find("cube")
# cube.reparent_to(render)
