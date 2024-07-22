from manim import *
import os

class PointTransitionScene(ThreeDScene):
    def construct(self):
        # Define colors based on NeuralNetworkMobject palette
        background_color = "#f1f1f1"
        point_color = RED
        line_color = "#373737"
        axes_color = "#373737"
        fill_color = "#ffffff"
        dot_fill_opacity = 1

        # Set background color
        self.camera.background_color = background_color

        # 1D Space with Y-axis
        line_1d = NumberLine(x_range=[-5, 5, 1], length=10, color=line_color)
        point_1d = Dot(color=point_color, fill_color=fill_color, fill_opacity=dot_fill_opacity).move_to(line_1d.n2p(0))
        
        self.play(Create(line_1d), FadeIn(point_1d))
        self.wait(1)

        # Animate the point moving along the 1D line
        self.play(point_1d.animate.move_to(line_1d.n2p(3)), run_time=2)
        self.wait(1)

        # 3D Space Transition (showing only 2 axes initially)
        axes_3d = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            axis_config={"color": axes_color}
        )

        # Initially align the camera to make it look like 2D
        self.set_camera_orientation(phi=0 * DEGREES, theta=-90 * DEGREES)
        point_3d = Dot3D(color=point_color, fill_color=fill_color, fill_opacity=dot_fill_opacity).move_to(axes_3d.c2p(0, 0, 0))

        self.play(FadeOut(line_1d), FadeOut(point_1d), FadeIn(axes_3d), FadeIn(point_3d))
        self.wait(1)

        # Animate the point moving in 3D space
        self.play(point_3d.animate.move_to(axes_3d.c2p(2, 1, 0)), run_time=2)
        self.wait(1)

        # Rotate the camera to reveal the third axis
        self.move_camera(phi=75 * DEGREES, theta=-45 * DEGREES, run_time=2)
        self.play(point_3d.animate.move_to(axes_3d.c2p(2, 1, 1)), run_time=2)
        self.wait(1)

if __name__ == "__main__":
    os.system("manim -pql __file__ PointTransitionScene")
