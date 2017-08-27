import numpy as np
import pygame


def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def initial_weight():
    return 2 * np.random.random()

class Node:
    def __init__(self):
        self.weights = []
        self.value = 0

    def add_weight(self, node):
        self.weights.append((node, initial_weight()))

class Network:
    def __init__(self, inputs, layers, layer_size, outputs):
        
        self.inputs = inputs
        self.layers = layers
        self.outputs = outputs
        self.layer_size = layer_size
        self.input_nodes = []
        self.hidden_nodes = [[]]
        self.output_nodes = []

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


    def display(self):
        for i in range(0, self.inputs):
            print(self.input_nodes[i].weights)

        for i in range(0, self.layers):
            for j in range(0, self.layer_size):
                print(self.hidden_nodes[i][j].weights)

net = Network(2,2,3,2)
net.display()
