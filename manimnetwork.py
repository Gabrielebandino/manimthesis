from manim import *
import itertools as it  # Importing itertools module
import random  # Importing random module

class NeuralNetworkMobject(VGroup):
    def __init__(self, neural_network, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.neuron_radius = 0.15
        self.neuron_to_neuron_buff = MED_SMALL_BUFF
        self.layer_to_layer_buff = 2 * LARGE_BUFF  # Increased the buffer space
        self.output_neuron_color = "#afafaf"
        self.input_neuron_color = "#afafaf"
        self.hidden_layer_neuron_color = "#afafaf"
        self.neuron_stroke_width = 2
        self.neuron_fill_color = "#ffffff"
        self.edge_color = "#373737"
        self.edge_stroke_width = 2
        self.edge_propogation_color = "#afafaf"
        self.edge_propogation_time = 1
        self.max_shown_neurons = 50
        self.brace_for_large_layers = True
        self.average_shown_activation_of_large_layer = True
        self.include_output_labels = False
        self.arrow = False
        self.arrow_tip_size = 0.1
        self.left_size = 1
        self.neuron_fill_opacity = 1

        self.layer_sizes = neural_network
        self.add_neurons()
        self.add_edges()
        self.add_to_back(self.layers)

    def add_neurons(self):
        layers = VGroup(*[
            self.get_layer(size, index)
            for index, size in enumerate(self.layer_sizes)
        ])
        layers.arrange_submobjects(RIGHT, buff=self.layer_to_layer_buff)
        self.layers = layers
        if self.include_output_labels:
            self.label_outputs_text()

    def get_nn_fill_color(self, index):
        if index == -1 or index == len(self.layer_sizes) - 1:
            return self.output_neuron_color
        if index == 0:
            return self.input_neuron_color
        else:
            return self.hidden_layer_neuron_color

    def get_layer(self, size, index=-1):
        layer = VGroup()
        n_neurons = size
        if n_neurons > self.max_shown_neurons:
            n_neurons = self.max_shown_neurons
        neurons = VGroup(*[
            Circle(
                radius=self.neuron_radius,
                stroke_color=self.get_nn_fill_color(index),
                stroke_width=self.neuron_stroke_width,
                fill_color=self.neuron_fill_color,
                fill_opacity=self.neuron_fill_opacity,
            )
            for x in range(n_neurons)
        ])
        neurons.arrange_submobjects(
            DOWN, buff=self.neuron_to_neuron_buff
        )
        for neuron in neurons:
            neuron.edges_in = VGroup()
            neuron.edges_out = VGroup()
        layer.neurons = neurons
        layer.add(neurons)

        if size > n_neurons:
            dots = Tex("\\vdots")
            dots.move_to(neurons)
            VGroup(*neurons[:len(neurons) // 2]).next_to(
                dots, UP, MED_SMALL_BUFF
            )
            VGroup(*neurons[len(neurons) // 2:]).next_to(
                dots, DOWN, MED_SMALL_BUFF
            )
            layer.dots = dots
            layer.add(dots)
            if self.brace_for_large_layers:
                brace = Brace(layer, LEFT)
                brace_label = brace.get_tex(str(size))
                layer.brace = brace
                layer.brace_label = brace_label
                layer.add(brace, brace_label)

        return layer

    def add_edges(self):
        self.edge_groups = VGroup()
        for l1, l2 in zip(self.layers[:-1], self.layers[1:]):
            edge_group = VGroup()
            for n1, n2 in it.product(l1.neurons, l2.neurons):
                edge = self.get_edge(n1, n2)
                edge_group.add(edge)
                n1.edges_out.add(edge)
                n2.edges_in.add(edge)
            self.edge_groups.add(edge_group)
        self.add_to_back(self.edge_groups)

    def get_edge(self, neuron1, neuron2):
        if self.arrow:
            return Arrow(
                neuron1.get_center(),
                neuron2.get_center(),
                buff=self.neuron_radius,
                stroke_color=self.edge_color,
                stroke_width=self.edge_stroke_width,
                tip_length=self.arrow_tip_size
            )
        return Line(
            neuron1.get_center(),
            neuron2.get_center(),
            buff=self.neuron_radius,
            stroke_color=self.edge_color,
            stroke_width=self.edge_stroke_width,
        )

    def label_inputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[0].neurons):
            label = Tex(f"{l}_"+"{"+f"{n + 1}"+"}")
            label.set_height(0.3 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    def label_outputs(self, l):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = Tex(f"{l}_"+"{"+f"{n + 1}"+"}")
            label.set_height(0.4 * neuron.get_height())
            label.move_to(neuron)
            self.output_labels.add(label)
        self.add(self.output_labels)

    def label_outputs_text(self, outputs):
        self.output_labels = VGroup()
        for n, neuron in enumerate(self.layers[-1].neurons):
            label = Tex(outputs[n])
            label.set_height(0.75*neuron.get_height())
            label.move_to(neuron)
            label.shift((neuron.get_width() + label.get_width()/2)*RIGHT)
            self.output_labels.add(label)
        self.add(self.output_labels)

    def label_hidden_layers(self, l):
        self.output_labels = VGroup()
        for layer in self.layers[1:-1]:
            for n, neuron in enumerate(layer.neurons):
                label = Tex(f"{l}_{n + 1}")
                label.set_height(0.4 * neuron.get_height())
                label.move_to(neuron)
                self.output_labels.add(label)
        self.add(self.output_labels)

class NN(Scene):
    def construct(self):
        # Set background color
        self.camera.background_color = "#f1f1f1"

        netw = NeuralNetworkMobject([10, 1, 10])
        self.add(netw)

        # Add trapezoids behind the first and third layer
        trapezoid1 = Polygon(
            [-3, -1.5, 0], [3, -1.5, 0], [2.7, 0, 0], [-2.7, 0, 0],
            fill_color=BLUE, fill_opacity=0.5
        )
        trapezoid2 = Polygon(
            [-3, -1.5, 0], [3, -1.5, 0], [2.7, 0, 0], [-2.7, 0, 0],
            fill_color=BLUE, fill_opacity=0.5
        )

        # Position the trapezoids behind the first and third layer, facing inward
        trapezoid1.move_to(netw.layers[0].get_center() + LEFT * 0.1)
        trapezoid1.rotate(PI / 2, axis=IN)
        trapezoid2.move_to(netw.layers[2].get_center() + RIGHT * 0.1)
        trapezoid2.rotate(-PI / 2, axis=IN)

        # Add LSTM Layer text on top of each trapezoid
        lstm_text1 = Text("Encoder", color="#373737")
        lstm_text1.next_to(trapezoid1, UP)
        lstm_text2 = Text("Decoder", color="#373737")
        lstm_text2.next_to(trapezoid2, UP)

        self.add(trapezoid1, trapezoid2, lstm_text1, lstm_text2)

        # Add values on the left side of the first layer
        input_values = [0.25, 0.53, 0.64, 0.23, 0.01, 0.98, 0.75, 0.74, 0.42, 0.22]
        input_labels = VGroup()
        for i, neuron in enumerate(netw.layers[0].neurons):
            label = Text(str(input_values[i]), color="#373737", font_size=24)
            label.next_to(neuron, LEFT, buff=0.1)
            input_labels.add(label)
        
        # Add values on the right side of the third layer
        output_values = [0.25, 0.53, 0.64, 0.23, 0.01, 0.98, 0.75, 0.74, 0.42, 0.22]
        output_labels = VGroup()
        for i, neuron in enumerate(netw.layers[2].neurons):
            label = Text(str(output_values[i]), color="#373737", font_size=24)
            label.next_to(neuron, RIGHT, buff=0.1)
            output_labels.add(label)

        self.add(input_labels, output_labels)
        self.add(netw)

        # Add a text label on top of the middle layer
        middle_label = Text("[0.22]", color="#373737", font_size=24)
        middle_label.next_to(netw.layers[1], UP*3)
        self.add(middle_label)

        # Animate the network results and edges
        animations = []
        
        # Animate edges from first to second layer
        for neuron in netw.layers[1].neurons:
            edge_animations = []
            for edge in neuron.edges_in:
                weight = random.uniform(0.5, 2.0)
                edge_animations.append(edge.animate.set_stroke(width=weight * 3))
            animations.extend(edge_animations)
        
        # Animate edges from second to third layer and display output labels
        for neuron, label in zip(netw.layers[2].neurons, output_labels):
            edge_animations = []
            for edge in neuron.edges_in:
                weight = random.uniform(0.5, 2.0)
                edge_animations.append(edge.animate.set_stroke(width=weight * 3))
            animations.extend(edge_animations)
            animations.append(FadeIn(label, shift=UP))

        self.play(AnimationGroup(*animations, lag_ratio=0.1))
        self.wait(1)

if __name__ == "__main__":
    os.system("manim -pql __file__ NN")
