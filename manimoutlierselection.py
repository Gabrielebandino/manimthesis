from manim import *

class GrayText(Text):
    def __init__(self, *args, **kwargs):
        kwargs['color'] = kwargs.get('color', '#000000')  # Set default color to gray
        super().__init__(*args, **kwargs)

class OutlierSelection(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#f1f1f1"

        # Step 1: Create a table with 4 columns and 6 rows (only columns 1, 2, 5, 6)
        table_data = [
            ["A1", "A2", "A5", "A6"],
            ["B1", "T2", "B5", "B6"],
            ["C1", "C2", "C5", "C6"],
            ["D1", "D2", "D5", "D6"],
            ["E1", "E2", "E5", "E6"],
            ["F1", "F2", "F5", "F6"]
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
        table.scale(0.7)  # Scale the table to fit within the video space
        table.move_to(ORIGIN)  # Center the table in the scene
        table.set_color("#373737")
        
        self.play(Create(table))
        self.wait(0.5)

        # Step 2: Highlight a specific cell in red (let's say cell (3, 3) in the displayed table)
        outlier_cell = table.get_cell((3, 3))
        outlier_cell.set_fill(RED, opacity=1)
        outlier_cell.set_color(WHITE)
        
        self.play(outlier_cell.animate.set_fill(RED), run_time=1)
        self.wait(0.5)  # Wait for 0.5 seconds

        # Step 2.1: Reset the cell color to original after 0.5 seconds
        outlier_cell.set_fill("#ffffff", opacity=1)
        outlier_cell.set_color("#afafaf")

        self.play(outlier_cell.animate.set_opacity(0),run_time=1)
        #self.play(outlier_cell.animate.set_fill("#f1f1f1"), run_time=1)
        self.wait(0.5)

        # Step 3: Add a big red X on top of the table
        cross = Cross(table, stroke_color=RED, stroke_width=10)
        self.play(Create(cross))
        self.wait(1)

        # Step 4: Fade out the table and the X
        self.play(FadeOut(table), FadeOut(cross))
        self.wait(1)

if __name__ == "__main__":
    os.system("manim -pql __file__ OutlierSelection")
