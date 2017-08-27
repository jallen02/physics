import numpy as np
import pygame

#np.random.seed(1)

def sigmoid(x):
    return 1 / (1 + np.exp(-(x/100)))

def initial_weight():
    return 2 * np.random.random()

class Node:
    def __init__(self):
        self.weights = []
        self.value = 0

    def add_weight(self, node):
        self.weights.append((node, initial_weight()))

    def activate(self):
        return sigmoid(self.value)

class Network:
    def __init__(self, inputs, layers, layer_size, outputs, node_draw_size = 15, node_draw_spacing = 100):
        
        self.inputs = inputs
        self.layers = layers
        self.outputs = outputs
        self.layer_size = layer_size
        self.input_nodes = []
        self.hidden_nodes = [[]]
        self.output_nodes = []
        self.node_draw_size = node_draw_size
        self.node_draw_spacing = node_draw_spacing
        self.fitness = 0
        self.complete = False

        for i in range(0, inputs):
            self.input_nodes.append(Node())

        for i in range(0, layers):
            if i != 0:
                self.hidden_nodes.append([])
            for j in range(0, layer_size):
                self.hidden_nodes[i].append(Node())

        for i in range(0, self.outputs):
            self.output_nodes.append(Node())

        for i in range(0, inputs):
            for j in range(0, layer_size):
                self.input_nodes[i].add_weight(self.hidden_nodes[0][j])

        for i in range(0, layers):
            if i != (layers - 1):
                for j in range(0, layer_size):
                    for k in range(0, layer_size):
                        self.hidden_nodes[i][j].add_weight(self.hidden_nodes[i+1][k])

        for i in range(0, layer_size):
            for j in range(0, outputs):
                self.hidden_nodes[-1][i].add_weight(self.output_nodes[j])

    def set_zero(self):
        for layer in self.hidden_nodes:
            for node in layer:
                node.value = 0
        for node in self.output_nodes:
            node.value = 0

    def max_output(self):
        outputs = []
        for output in self.output_nodes:
            print(output.activate())
            print(output.value)
            outputs.append(output.activate())

        return outputs.index(max(outputs))

    def propogate(self):
        self.propogate_forward(self.input_nodes)

    def propogate_forward(self, node_list):
        next_list = []
        if len(node_list) != 0:
            for node in node_list:
                for weight in node.weights:
                    pass_val = node.activate()
                    dest_node = weight[0]
                    next_list.append(dest_node)
                    dest_node.value += pass_val * weight[1]
            self.propogate_forward(next_list)

    def process_input(self, inputs):
        for i in range(0, len(inputs)):
            self.input_nodes[i].value = inputs[i] 
        self.set_zero()


    def display(self):
        for i in range(0, self.inputs):
            print(self.input_nodes[i].weights)

        for i in range(0, self.layers):
            for j in range(0, self.layer_size):
                print(self.hidden_nodes[i][j].weights)

    def draw(self, screen, pos):
        input_node_pos = []
        for i in range(0, self.inputs):
            color = pygame.color.THECOLORS["black"]
            input_node_pos.append((pos[0], pos[1] + (self.node_draw_spacing*i)))
            pygame.draw.circle(screen, color, input_node_pos[i], self.node_draw_size) 

        hidden_node_pos = [[]]
        for i in range(0, self.layers):
            if i == len(hidden_node_pos):
                hidden_node_pos.append([])
            for j in range(0, self.layer_size):
                color = pygame.color.THECOLORS["black"]
                hidden_node_pos[i].append((pos[0] + (self.node_draw_spacing*(i+1)), \
                        pos[1] + (self.node_draw_spacing*j)))
                pygame.draw.circle(screen, color, hidden_node_pos[i][j], \
                        self.node_draw_size)

        output_node_pos = []
        for i in range(0, self.outputs):
            color = pygame.color.THECOLORS["black"]
            output_node_pos.append((pos[0] + (self.node_draw_spacing*(self.layers + 1)), \
                    pos[1] + (self.node_draw_spacing*i)))
            pygame.draw.circle(screen, color, output_node_pos[i], self.node_draw_size) 

        for i in range(0, self.inputs):
            for j in range(0, self.layer_size):
                color = pygame.color.THECOLORS["black"]
                pygame.draw.line(screen, color, input_node_pos[i], hidden_node_pos[0][j])

        for i in range(0, self.layers - 1):
            for j in range(0, self.layer_size):
                for k in range(0, self.layer_size):
                    color = pygame.color.THECOLORS["black"]
                    pygame.draw.line(screen, color, hidden_node_pos[i][j], hidden_node_pos[i+1][k])

        for i in range(0, self.layer_size):
            for j in range(0, self.outputs):
                color = pygame.color.THECOLORS["black"]
                pygame.draw.line(screen, color, hidden_node_pos[-1][i], output_node_pos[j])
                
