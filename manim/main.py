from turtle import left
from manimlib import *
from os import system

class Scene1(Scene):
    def construct(self):
        # my_plane = NumberPlane(axis_config = {"stroke_width": 0.2}, background_line_style={"stroke_color": WHITE, "stroke_width": 1, "stroke_opacity": 1})
        # self.add(my_plane)

        text1 = Text("声源定位", font="SimHei") # 宋体：SimSun | 黑体：SimHei
        self.play(Write(text1))
        # self.wait()

        text2 = Text("声源定位技术", font="SimHei")
        self.play(ReplacementTransform(text1, text2))
        # self.wait()

        text3 = Text("主动式、可在室内使用", font="SimSun")
        # text3.next_to(text2, DOWN)
        self.play(ApplyMethod(text2.shift, UP), FadeIn(text3, UP))
        # self.wait()

class Scene2(Scene):
    def construct(self):
        image_person = ImageMobject("./manim/img/person", height = 3)
        image_person.move_to(2 * DOWN)
        self.play(SpinInFromNothing(image_person))

        image_car = ImageMobject("./manim/img/car", height = 2)
        image_car.move_to(2 * UP + 4 * RIGHT)
        self.play(SpinInFromNothing(image_car))

        line1 = Line(2.4 * UP + 4 * RIGHT, 2 * DOWN + 0.8 * RIGHT, stroke_color = BLUE)
        line2 = Line(2.4 * UP + 4 * RIGHT, 2 * DOWN + 0.8 * LEFT, stroke_color = BLUE)
        self.play(ShowCreation(line1), ShowCreation(line2))

        line3 = Line(2.4 * UP + 4 * LEFT, 2 * DOWN + 0.8 * RIGHT, stroke_color = BLUE)
        line4 = Line(2.4 * UP + 4 * LEFT, 2 * DOWN + 0.8 * LEFT, stroke_color = BLUE)
        self.play(ApplyMethod(image_car.shift, 8 * LEFT),
                ReplacementTransform(line1, line3),
                ReplacementTransform(line2, line4),
                rate_func = smooth, run_time = 3)

        self.play(Indicate(line4, color = RED, scale_factor = 1))
        self.play(FadeOut(line4))

        line5 = Line(2.4 * UP + 4 * RIGHT, 2 * DOWN + 0.8 * RIGHT, stroke_color = BLUE)
        image_question = ImageMobject("./manim/img/question", height = 1)
        image_question.move_to(1 * DOWN + 1 * RIGHT)
        self.play(ApplyMethod(image_car.shift, 8 * RIGHT),
                ReplacementTransform(line3, line5),
                SpinInFromNothing(image_question),
                rate_func = smooth, run_time = 3)

        line6 = Line(2.4 * UP + 4 * RIGHT, 2 * DOWN + 0.8 * LEFT, stroke_color = BLUE)
        self.play(FadeIn(line6), FadeOut(image_question))

        b1 = Brace(line5, direction = line5.copy().rotate(PI / 2).get_unit_vector())
        b1text = b1.get_text("L", font="SimSun")
        line5_len = np.linalg.norm((2.4 * UP + 4 * RIGHT) - (2 * DOWN + 0.8 * RIGHT))
        line6_dir = (2 * DOWN + 0.8 * LEFT) - (2.4 * UP + 4 * RIGHT)
        line6_dir = line6_dir / np.linalg.norm(line6_dir)
        line6s1_start = 2.4 * UP + 4 * RIGHT
        line6s1_end = line6s1_start + np.array([_ * line5_len for _ in line6_dir])
        line6s1 = Line(line6s1_start, line6s1_end)
        b2 = Brace(line6s1, direction = line6s1.copy().rotate(- PI / 2).get_unit_vector())
        b2text = b2.get_text("L", font="SimSun")
        self.play(FadeIn(b1), FadeIn(b1text),
                FadeIn(b2), FadeIn(b2text))
        
        line6s2_start = line6s1_end
        line6s2_end = 2 * DOWN + 0.8 * LEFT
        line6s2 = Line(line6s2_start, line6s2_end)
        b3 = Brace(line6s2, direction = line6s2.copy().rotate(- PI / 2).get_unit_vector())
        b3text = b3.get_text("△L", font="SimSun")
        self.play(FadeIn(b3), FadeIn(b3text))

        self.play(Flash(b3text))

        p1 = Dot().move_to(2 * DOWN + 0.8 * RIGHT)
        p2 = Dot().move_to(2 * DOWN + 0.8 * LEFT)
        c1 = Circle(radius = 0.2, color = WHITE).move_to(2 * DOWN + 0.8 * RIGHT)
        c2 = Circle(radius = 0.2, color = WHITE).move_to(2 * DOWN + 0.8 * LEFT)
        l1 = Line(2 * DOWN + 0.6 * RIGHT, 2 * DOWN + 0.6 * LEFT)
        g1 = VGroup(p1, p2, c1, c2, l1)
        self.play(FadeIn(g1), FadeOut(image_person))

        g0 = VGroup(b1, b1text, b2, b2text, b3, b3text, line5, line6)
        self.play(FadeOut(image_car), FadeOut(g0), ApplyMethod(g1.move_to, LEFT * 3 + 0.2 * TOP))
        
        p3 = Dot().move_to(LEFT)
        p4 = Dot()
        p5 = Dot().move_to(RIGHT)
        c3 = Circle(radius = 0.2, color = WHITE).move_to(LEFT)
        c4 = Circle(radius = 0.2, color = WHITE)
        c5 = Circle(radius = 0.2, color = WHITE).move_to(RIGHT)
        l2 = Line(0.8 * LEFT, 0.2 * LEFT)
        l3 = Line(0.8 * RIGHT, 0.2 * RIGHT)
        g2 = VGroup(p3, p4, p5, c3, c4, c5, l2, l3).move_to(LEFT * 3 + 0.2 * DOWN)
        self.play(FadeIn(g2))

if __name__ == "__main__":
    system("manimgl %s Scene2" % __file__)

# manimgl manim/main.py -w --uhd