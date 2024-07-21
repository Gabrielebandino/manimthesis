from manim import *
import numpy as np

class GrayText(Text):
    def __init__(self, *args, **kwargs):
        kwargs['color'] = kwargs.get('color', '#000000')  # Set default color to gray
        super().__init__(*args, **kwargs)

class FeatureSelection2(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#f1f1f1"

        # Step 1: Create a table with 10 columns and 6 rows
        table_data = [
            ["A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8", "A9", "A10"],
            ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10"],
            ["C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9", "C10"],
            ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8", "D9", "D10"],
            ["E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9", "E10"],
            ["F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10"]
        ]

        table = Table(
            table_data,
            row_labels=[GrayText(str(i)) for i in range(1, 7)],
            col_labels=[GrayText(str(i)) for i in range(1, 11)],
            top_left_entry=GrayText("Feature Selection")
        )
        for i, col in enumerate((table.get_columns())[1:]):
            for j, cell in enumerate(col[1:]):
                cell.set_fill("#ffffff", opacity=1)
                cell.set_color("#afafaf")
        table.scale(0.5)  # Scale the table to fit within the video space
        table.move_to(ORIGIN)  # Center the table in the scene
        table.set_color("#373737")
        
        self.play(Create(table))
        self.wait(0.5)

        # Step 2: Highlight columns 2, 3, 6, and 7
        highlighted_columns = [2, 3, 6, 7]
        highlight_color = "#ffffff"  # Light grey background for highlighted cells

        for i, col in enumerate(highlighted_columns):
            col_cells = table.get_columns()[col - 1]
            for j, cell in enumerate(col_cells):
                table.add_highlighted_cell((j, col), color=GREEN)
                cell.set_fill(highlight_color, opacity=1)
                cell.set_color("#373737")

        # Step 3: Create a new table with the selected columns
        selected_data = [
            [row[i - 1] for i in highlighted_columns]
            for row in table_data
        ]

        self.wait(1.5)

        new_table = Table(
            selected_data,
            row_labels=[GrayText(str(i)) for i in range(1, 7)],
            col_labels=[GrayText(str(i)) for i in highlighted_columns],
            top_left_entry=GrayText("Selected Features")
        )
        new_table.set_color("#373737")
        for i, col in enumerate((new_table.get_columns())[1:]):
            for j, cell in enumerate(col[1:]):
                cell.set_fill("#ffffff", opacity=1)
                cell.set_color("#afafaf")

        new_table.scale(0.5)  # Scale the new table to fit within the video space
        new_table.move_to(ORIGIN)  # Center the new table in the scene

        self.play(ReplacementTransform(table, new_table))
        self.wait(2)

        # Fade out the table and wait 1 second
        self.play(FadeOut(new_table))
        self.wait(1)

if __name__ == "__main__":
    script = __file__
    os.system(f"manim -pql {script} FeatureSelection2")
