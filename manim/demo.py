from manimlib import *
from os import system

class SquareToCircle(Scene):
    def construct(self):
        circle = Circle()
        circle.set_fill(BLUE, opacity=0.5)
        circle.set_stroke(BLUE_E, width=4)

        square = Square()
        square.set_stroke(BLACK, width=4)
        self.play(ShowCreation(square))
        self.wait()
        self.play(ReplacementTransform(square, circle))
        self.wait()

if __name__ == "__main__":
    # system("manimgl {} SquareToCircle -c white".format(__file__))
    system("manimgl %s SquareToCircle" % __file__)