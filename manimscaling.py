from manim import *
import numpy as np

class GrayText(Text):
    def __init__(self, *args, **kwargs):
        kwargs['color'] = kwargs.get('color', '#000000')  # Set default color to gray
        super().__init__(*args, **kwargs)

class Scaling(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#f1f1f1"

        # Step 1: Create a table with 4 columns and 6 rows (only columns 1, 2, 5, 6)
        table_data = [
            ["-7.5", "8.0", "2.8", "4.5"],
            ["7.9", "-5.7", "8.5", "2.1"],
            ["-2.3", "-3.2", "4.4", "5.4"],
            ["-3.2", "2.3", "8.4", "-9.0"],
            ["4.3", "4.4", "-3.2", "8.6"],
            ["-8.3", "7.3", "-7.3", "-4.2"]
        ]

        table = Table(
            table_data,
            row_labels=[GrayText(str(i)) for i in range(1, 7)],
            col_labels=[GrayText(str(i)) for i in [1, 2, 5, 6]],
            top_left_entry=GrayText("Outlier Selection")
        )
        for i, col in enumerate((table.get_columns())[1:]):
            for j, cell in enumerate(col[1:]):
                cell.set_fill("#ffffff", opacity=1)
                cell.set_color("#afafaf")
        table.scale(0.6)  # Scale the table to fit within the video space
        table.move_to(LEFT * 1.5)  # Move the table to the left
        table.set_color("#373737")
        
        self.play(Create(table))
        self.wait(0.5)

        # Function to create custom box plot
        def create_custom_box_plot(data, x_pos, box_width=0.5):
            min_val, max_val, median, q1, q3 = np.percentile(data, [0, 100, 50, 25, 75])
            box = Rectangle(
                width=box_width,
                height=(q3 - q1) / 3,  # Adjust the height scale for visibility
                fill_color=BLUE,
                fill_opacity=0.5,
                stroke_color=BLUE
            ).move_to([x_pos, (q1 + q3) / 6, 0])  # Adjust vertical position
            median_line = Line(
                [x_pos - box_width / 2, median / 3, 0],
                [x_pos + box_width / 2, median / 3, 0],
                color=RED
            )
            lower_whisker = Line(
                [x_pos, min_val / 3, 0],
                [x_pos, q1 / 3, 0],
                color=BLUE
            )
            upper_whisker = Line(
                [x_pos, q3 / 3, 0],
                [x_pos, max_val / 3, 0],
                color=BLUE
            )
            lower_cap = Line(
                [x_pos - box_width / 4, min_val / 3, 0],
                [x_pos + box_width / 4, min_val / 3, 0],
                color=BLUE
            )
            upper_cap = Line(
                [x_pos - box_width / 4, max_val / 3, 0],
                [x_pos + box_width / 4, max_val / 3, 0],
                color=BLUE
            )
            return VGroup(box, median_line, lower_whisker, upper_whisker, lower_cap, upper_cap)

        # Original box plot
        box_data = [float(cell) for row in table_data for cell in row]
        original_box_plot = create_custom_box_plot(box_data, 4)
        self.play(Create(original_box_plot))
        self.wait(1)

        # Step 3: Apply MinMax scaler to the table and update the box plot
        min_val = min(box_data)
        max_val = max(box_data)
        scaled_data = [
            [(float(x) - min_val) / (max_val - min_val) for x in row] for row in table_data
        ]

        scaled_table_data = [[f"{value:.2f}" for value in row] for row in scaled_data]

        scaled_table = Table(
            scaled_table_data,
            row_labels=[GrayText(str(i)) for i in range(1, 7)],
            col_labels=[GrayText(str(i)) for i in [1, 2, 5, 6]],
            top_left_entry=GrayText("Scaled Data")
        )
        for i, col in enumerate((scaled_table.get_columns())[1:]):
            for j, cell in enumerate(col[1:]):
                cell.set_fill("#ffffff", opacity=1)
                cell.set_color("#afafaf")
        scaled_table.scale(0.6)  # Scale the table to fit within the video space
        scaled_table.move_to(LEFT * 1.5)  # Move the table to the left
        scaled_table.set_color("#373737")
        
        self.play(Transform(table, scaled_table))
        self.wait(1)

        new_box_data = [value for row in scaled_data for value in row]
        scaled_box_plot = create_custom_box_plot(new_box_data, 4)

        self.play(
            Transform(original_box_plot, scaled_box_plot)
        )
        #self.wait(1)

        # Step 4: Fade out the table and the box plot
        self.play(FadeOut(scaled_table), FadeOut(scaled_box_plot))
        self.wait(1)

if __name__ == "__main__":
    os.system("manim -pql __file__ Scaling")
