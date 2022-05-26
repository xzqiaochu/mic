from turtle import color
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

        for _ in range(2):
                self.play(ApplyMethod(line4.set_style, {"stroke_color" : RED}), run_time = 1/2)
                self.play(ApplyMethod(line4.set_style, {"stroke_color" : BLUE}), run_time = 1/2)

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
        l1 = Line(2 * DOWN + 0.8 * RIGHT, 2 * DOWN + 0.8 * LEFT)
        g1 = VGroup(p1, p2, c1, c2, l1)
        self.play(FadeIn(g1), FadeOut(image_person))

        g0 = VGroup(b1, b1text, b2, b2text, b3, b3text, line5, line6)
        self.play(FadeOut(image_car), FadeOut(g0))

        self.play(ApplyMethod(g1.move_to, LEFT * 2.5 + 0.5 * UP))
        
        p3 = Dot().move_to(LEFT)
        p4 = Dot()
        p5 = Dot().move_to(RIGHT)
        c3 = Circle(radius = 0.2, color = WHITE).move_to(LEFT)
        c4 = Circle(radius = 0.2, color = WHITE)
        c5 = Circle(radius = 0.2, color = WHITE).move_to(RIGHT)
        l2 = Line(LEFT, RIGHT)
        g2 = VGroup(p3, p4, p5, c3, c4, c5, l2).move_to(LEFT * 2.5 + 0.5 * DOWN)
        self.play(ShowCreation(g2))

        p31 = Dot().move_to(np.array((1, 0, 0)))
        p32 = Dot().move_to(np.array((1/2, 3**0.5/2, 0)))
        p33 = Dot().move_to(np.array((-1/2, 3**0.5/2, 0)))
        p34 = Dot().move_to(np.array((-1, 0, 0)))
        p35 = Dot().move_to(np.array((-1/2, -3**0.5/2, 0)))
        p36 = Dot().move_to(np.array((1/2, -3**0.5/2, 0)))
        c31 = Circle(radius = 0.2, color = WHITE).move_to(p31)
        c32 = Circle(radius = 0.2, color = WHITE).move_to(p32)
        c33 = Circle(radius = 0.2, color = WHITE).move_to(p33)
        c34 = Circle(radius = 0.2, color = WHITE).move_to(p34)
        c35 = Circle(radius = 0.2, color = WHITE).move_to(p35)
        c36 = Circle(radius = 0.2, color = WHITE).move_to(p36)
        l31 = Line(np.array((1, 0, 0)), np.array((1/2, 3**0.5/2, 0)))
        l32 = Line(np.array((1/2, 3**0.5/2, 0)), np.array((-1/2, 3**0.5/2, 0)))
        l33 = Line(np.array((-1/2, 3**0.5/2, 0)), np.array((-1, 0, 0)))
        l34 = Line(np.array((-1, 0, 0)), np.array((-1/2, -3**0.5/2, 0)))
        l35 = Line(np.array((-1/2, -3**0.5/2, 0)), np.array((1/2, -3**0.5/2, 0)))
        l36 = Line(np.array((1/2, -3**0.5/2, 0)), np.array((1, 0, 0)))
        g3 = VGroup(p31, p32, p33, p34, p35, p36,
                c31, c32, c33, c34, c35, c36,
                l31, l32, l33, l34, l35, l36)
        g4 = g3.copy()
        p41 = Dot()
        c41 = Circle(radius = 0.2, color = WHITE)
        g4.add(p41, c41)
        g4.next_to(g3, DOWN)
        g34 = VGroup(g3, g4).move_to(RIGHT * 2.5)
        self.play(ShowCreation(g34))

        g12 = VGroup(g1, g2)
        r1 = RoundedRectangle(corner_radius = 0.2, width = 6, height = 12, fill_color = RED, fill_opacity = 0).surround(g12)
        r2 = RoundedRectangle(corner_radius = 0.2, width = 6, height = 12, fill_color = RED, fill_opacity = 0).surround(g34)
        t1 = Text("线性阵列", font="SimSun", font_size = 24).next_to(r1, DOWN)
        t2 = Text("平面阵列", font="SimSun", font_size = 24).next_to(r2, DOWN)
        self.play(ShowCreation(r1), ShowCreation(r2), ShowCreation(t1), ShowCreation(t2))
        self.remove(g12, g34)
        self.add(g12, g34)

        for _ in range(2):
            self.play(ApplyMethod(r1.set_style, {"fill_opacity" : 1}), run_time = 1/2)
            self.play(ApplyMethod(r1.set_style, {"fill_opacity" : 0}), run_time = 1/2)

        for _ in range(2):
            self.play(ApplyMethod(r2.set_style, {"fill_opacity" : 1}), run_time = 1/2)
            self.play(ApplyMethod(r2.set_style, {"fill_opacity" : 0}), run_time = 1/2)
        
        self.play(FadeOut(r1), FadeOut(r2),
                FadeOut(t1), FadeOut(t2),
                FadeOut(g1), FadeOut(g4)) # 擦除多余麦克风阵列

        # 平面坐标系

        axe1 = Axes(height = 4, width = 4, depth = 4,
                        x_range = (-3, 3), y_range=(-3, 3),
                        axis_config = {"include_tip" : True})
        axe1.move_to(LEFT * 2.5)
        p3n = Dot().move_to(axe1.c2p(-1, 0))
        p4n = Dot().move_to(axe1.c2p(0, 0))
        p5n = Dot().move_to(axe1.c2p(1, 0))
        c3n = Circle(radius = 0.2, color = WHITE).move_to(axe1.c2p(-1, 0))
        c4n = Circle(radius = 0.2, color = WHITE).move_to(axe1.c2p(0, 0))
        c5n = Circle(radius = 0.2, color = WHITE).move_to(axe1.c2p(1, 0))
        l2n = Line(axe1.c2p(-1, 0), axe1.c2p(1, 0))
        g2n = VGroup(p3n, p4n, p5n, c3n, c4n, c5n, l2n)
        self.play(ReplacementTransform(g2, g2n), ShowCreation(axe1)) # 坐标系和麦克风阵列

        d11 = Dot(point = axe1.c2p(2, 1), color = YELLOW)
        l11 = Line(axe1.c2p(2, 1), axe1.c2p(1, 0), color = BLUE)
        l21 = Line(axe1.c2p(2, 1), axe1.c2p(-1, 0), color = BLUE)
        self.play(ShowCreation(VGroup(d11, l11, l21))) # 定位原理连线示意

        d12 = Dot(point = axe1.c2p(1, 2), color = YELLOW)
        l12 = Line(axe1.c2p(1, 2), axe1.c2p(1, 0), color = BLUE)
        l22 = Line(axe1.c2p(1, 2), axe1.c2p(-1, 0), color = BLUE)
        self.play(ReplacementTransform(d11, d12),
                ReplacementTransform(l11, l12),
                ReplacementTransform(l21, l22)) # 定位点运动

        # 空间坐标系

        axe2 = ThreeDAxes(height = 4, width = 4, depth = 4,
                        x_range = (-3, 3), y_range=(-3, 3), z_range = (-3, 3),
                        axis_config = {"include_tip" : True})
        axe2.rotate(- PI / 2, RIGHT)
        axe2.rotate(-45 * DEGREES, UP)
        axe2.rotate(-30 * DEGREES, RIGHT + UP)
        axe2.move_to(RIGHT * 2.5)

        p31n = Dot().move_to(axe2.c2p(1, 0))
        p32n = Dot().move_to(axe2.c2p(1/2, 3**0.5/2))
        p33n = Dot().move_to(axe2.c2p(-1/2, 3**0.5/2))
        p34n = Dot().move_to(axe2.c2p(-1, 0))
        p35n = Dot().move_to(axe2.c2p(-1/2, -3**0.5/2))
        p36n = Dot().move_to(axe2.c2p(1/2, -3**0.5/2))
        c31n = Circle(radius = 0.2, color = WHITE).move_to(p31n)
        c32n = Circle(radius = 0.2, color = WHITE).move_to(p32n)
        c33n = Circle(radius = 0.2, color = WHITE).move_to(p33n)
        c34n = Circle(radius = 0.2, color = WHITE).move_to(p34n)
        c35n = Circle(radius = 0.2, color = WHITE).move_to(p35n)
        c36n = Circle(radius = 0.2, color = WHITE).move_to(p36n)
        l31n = Line(axe2.c2p(1, 0, 0), axe2.c2p(1/2, 3**0.5/2, 0))
        l32n = Line(axe2.c2p(1/2, 3**0.5/2, 0), axe2.c2p(-1/2, 3**0.5/2, 0))
        l33n = Line(axe2.c2p(-1/2, 3**0.5/2, 0), axe2.c2p(-1, 0, 0))
        l34n = Line(axe2.c2p(-1, 0, 0), axe2.c2p(-1/2, -3**0.5/2, 0))
        l35n = Line(axe2.c2p(-1/2, -3**0.5/2, 0), axe2.c2p(1/2, -3**0.5/2, 0))
        l36n = Line(axe2.c2p(1/2, -3**0.5/2, 0), axe2.c2p(1, 0, 0))
        g3n = VGroup(p31n, p32n, p33n, p34n, p35n, p36n,
                c31n, c32n, c33n, c34n, c35n, c36n,
                l31n, l32n, l33n, l34n, l35n, l36n)
        self.play(ReplacementTransform(g3, g3n), ShowCreation(axe2)) # 坐标系和麦克风阵列

        dn1 = Dot(point = axe2.c2p(1, 2, 3), color = YELLOW)
        ln1 = Line(axe2.c2p(1, 2, 3), axe2.c2p(0, 0, 0), color = BLUE)
        self.play(ShowCreation(VGroup(dn1, ln1))) # 定位原理连线示意

        dn2 = Dot(point = axe2.c2p(3, 2, 1), color = YELLOW)
        ln2 = Line(axe2.c2p(3, 2, 1), axe2.c2p(0, 0, 0), color = BLUE)
        self.play(ReplacementTransform(VGroup(dn1, ln1), VGroup(dn2, ln2))) # 定位点运动

        self.play(FadeOut(VGroup(g2n, axe1, d12, l12, l22, dn2, ln2, g3n)),
                ApplyMethod(axe2.move_to, ORIGIN))
                
        self.play(ApplyMethod(axe2.scale, 1.5))

class Scene3(Scene):
    def construct(self):
        axe = ThreeDAxes(height = 4, width = 4, depth = 4,
                        x_range = (-3, 3), y_range=(-3, 3), z_range = (-3, 3),
                        axis_config = {"include_tip" : True})
        axe.rotate(- PI / 2, RIGHT)
        axe.rotate(-45 * DEGREES, UP)
        axe.rotate(-30 * DEGREES, RIGHT + UP)
        axe.scale(1.5)
        self.add(axe)

        mic1_p = axe.c2p(-2, 0, 0)
        mic2_p = axe.c2p(0, 2, 0)
        mic1 = Dot(mic1_p, color = WHITE)
        mic2 = Dot(mic2_p, color = WHITE)
        target_mic1p = axe.c2p(1, 0.75, 3)
        target_mic2p = axe.c2p(-0.25, -1, 3)
        mic1_line = Line(mic1_p, target_mic1p)
        mic2_line = Line(mic2_p, target_mic2p)
        self.play(Write(VGroup(mic1, mic2, mic1_line, mic2_line)))

        axe_all = VGroup(axe, mic1, mic2, mic1_line, mic2_line)
        self.play(ApplyMethod(axe_all.rotate, -105 * DEGREES, RIGHT))

        target = Dot(axe.c2p(-0.19553071, 0.38901435, 1.70528992), color = YELLOW)
        self.play(ShowCreation(target))

if __name__ == "__main__":
    system("manimgl %s Scene3" % __file__)

# manimgl manim/main.py -w --uhd