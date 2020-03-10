from manimlib.imports import *
import numpy as np

class FerrersDiagram(VGroup):
    def __init__(self, partition_sequence, padding = .5, center_x = 0, center_y = 0):
        self.partition_sequence = partition_sequence
        self.constituent_dots = [];
        VGroup.__init__(self)
        for i in range(np.size(partition_sequence)):
             cell = partition_sequence[i]
             for j in range(cell):
                dot = Dot()
                dot.location = (i,j)
                dot.layer = min(i, j)
                dot.row_length = cell
                self.constituent_dots.append(dot)
                dot.move_to(np.array([center_x - .5 * padding * np.max(partition_sequence) + padding * j, center_y - .5 * padding * np.size(partition_sequence) + padding * (np.size(partition_sequence)-i), 0]))
                self.add(dot)
        self.coordinate_dictionary = self.updateDictionary()
        self.corner = self.updateCornerPosition()
        self.layers = self.updateLayers()
        self.padding = self.updatePaddingDistance()
        self.RELATIVE_RIGHT = padding*RIGHT
        self.RELATIVE_DOWN = padding*DOWN
        self.parts = self.updateParts()
    def updateLayers(self):
        diagonals = []
        for dot in self.constituent_dots:
            if dot.location[0] == dot.location[1]:
                diagonals.append(dot)
        number_of_layers = len(diagonals)
        layers = [[] for i in range(number_of_layers)]
        for dot in self.constituent_dots:
            dot.layer = min(dot.location[0], dot.location[1])
            layers[dot.layer].append(dot)
        # update position_in_layer attribute for dots.
        def ahead_of_me(dot, first, second):
            if dot.location[0] > first:
                return 1 # true if lower
            elif dot.location[1] < second:
                return 1 # true if further left
            else:
                return 0
        for layer in layers:
            for dot in layer:
                list_of_dots_ahead_of_me_in_a_layer = list(filter(lambda x: ahead_of_me(x, dot.location[0], dot.location[1]), layer))
                dot.position_in_layer = len(list_of_dots_ahead_of_me_in_a_layer)
        self.layers = layers # I'm not really sure why this line is necessary, but, without it, _ShiftALayerCompletely will have ferrer.updateLayers() == ferrer.layers return false.
        return layers
    def updateDictionary(self):
        new_dict = {}
        for dot in self.constituent_dots:
            new_dict[dot.location] = dot
        self.coordinate_dictionary = new_dict
        return new_dict
    def updateCornerPosition(self):
        return self.coordinate_dictionary[(0,0)].get_center()
    def updatePaddingDistance(self):
        self.RELATIVE_RIGHT = self.coordinate_dictionary[(0,1)].get_center()-self.coordinate_dictionary[(0,0)].get_center()
        self.RELATIVE_DOWN = self.coordinate_dictionary[(1,0)].get_center()-self.coordinate_dictionary[(0,0)].get_center()
        self.padding = abs(self.coordinate_dictionary[(0,1)].get_center()[0]-self.coordinate_dictionary[(0,0)].get_center()[0])
        return self.padding
    def updateParts(self):
        parts = [[] for i in range(len(self.partition_sequence))]
        for dot in self.constituent_dots:
            dot.part = dot.location[0]
            parts[dot.part].append(dot)
        self.parts = parts
        return parts

class _ShiftALayerOnce(AnimationGroup):
    CONFIG = {
        "run_time": .5
    }
    def __init__(self, ferrer, layer_to_shift):
        self.check_if_input_is_ferrers_diagram(ferrer)
        animations = []
        ferrer.updateLayers()
        layer = ferrer.layers[layer_to_shift]
        for reference_dot in layer:
            next_dot = [dot for dot in layer if dot.position_in_layer == reference_dot.position_in_layer+1]
            if next_dot:
                animations.append(ApplyMethod(reference_dot.move_to, next_dot[0]))
            else:
                animations.append(ApplyMethod(reference_dot.shift, ferrer.RELATIVE_RIGHT))
        super().__init__(*animations)
    def check_if_input_is_ferrers_diagram(self, ferrer):
        if not isinstance(ferrer, FerrersDiagram):
            raise Exception("Convolution must take in a Ferrer's Diagram object")

class _ShiftALayerCompletely(Succession):
    def __init__(self, ferrer, layer_to_shift):
        self.check_if_input_is_ferrers_diagram(ferrer)
        ferrer.updateLayers()
        if max([dot.location[0] for dot in ferrer.layers[layer_to_shift]])-layer_to_shift > 0:
            animations = [
                _ShiftALayerOnce(ferrer, layer_to_shift) for i in range(max([dot.location[0] for dot in ferrer.layers[layer_to_shift]])-layer_to_shift)
            ]
        else:
            ferrer.updateLayers()
            animations = [ScaleInPlace(ferrer, 1)]
        super().__init__(*animations)
    def check_if_input_is_ferrers_diagram(self, ferrer):
        if not isinstance(ferrer, FerrersDiagram):
            raise Exception("Convolution must take in a Ferrer's Diagram object")

class _Justify(AnimationGroup):
    CONFIG = {
        "run_time": .5
    }
    def __init__(self, ferrer):
        self.check_if_input_is_ferrers_diagram(ferrer)
        animations = []
        for layer in ferrer.layers:
            for dot in layer:
                animations.append(ApplyMethod(dot.shift, ferrer.RELATIVE_RIGHT*(-dot.layer)))
        super().__init__(*animations)
    def check_if_input_is_ferrers_diagram(self, ferrer):
        if not isinstance(ferrer, FerrersDiagram):
            raise Exception("Convolution must take in a Ferrer's Diagram object")

class SortingParts(AnimationGroup):
    def __init__(self, ferrer):
        self.check_if_input_is_ferrers_diagram(ferrer)
        ferrer.updatePaddingDistance()
        animations = []
        if list(ferrer.partition_sequence) == sorted(list(ferrer.partition_sequence), reverse=True):
            print("⚠️ Warning: sorting an array with a partition sequence that is already sorted")
        else:
            print(str(list(ferrer.partition_sequence)), "is being sorted to", str(sorted(list(ferrer.partition_sequence), reverse=True)))
            ferrer.partition_sequence = sorted(list(ferrer.partition_sequence), reverse=True)
            parts = ferrer.parts
            rank = 0
            for i in range(max(ferrer.partition_sequence)+1):
                for part_index in range(len(ferrer.parts)):
                    if len(parts[part_index]) == i:
                        original_rank = len(parts) - part_index
                        rank += 1
                        difference = original_rank - rank
                        partgroup = VGroup()
                        for dot in parts[part_index]:
                            dot.location = (len(parts)-rank, dot.location[1])
                            partgroup.add(dot)
                        animations.append(ApplyMethod(partgroup.shift, difference*ferrer.RELATIVE_DOWN))
            ferrer.updateLayers()
            ferrer.updateCornerPosition()
            ferrer.updateDictionary()
            ferrer.updateParts()
        super().__init__(*animations)

    def check_if_input_is_ferrers_diagram(self, ferrer):
        if not isinstance(ferrer, FerrersDiagram):
            raise Exception("Convolution must take in a Ferrer's Diagram object")

class Convoluting(Succession):
    def __init__(self, ferrer):
        self.check_if_input_is_ferrers_diagram(ferrer)
        if len(ferrer.partition_sequence)<2 or (max(ferrer.partition_sequence))<2:
            raise Exception("⚠️ Convolution cannot be performed on partitions with fewer than two parts or with a maximum part size less than two")
        ferrer.updatePaddingDistance()
        new_partition_sequence = []
        for i in range(len(ferrer.layers)):
            new_partition_sequence.append(len(ferrer.layers[i]))
        print(ferrer.partition_sequence, "is convolving to", new_partition_sequence)
        ferrer.partition_sequence = new_partition_sequence
        animations = [
            _ShiftALayerCompletely(ferrer, i) for i in range(len(ferrer.layers))
        ]
        animations.append(_Justify(ferrer))
        for dot in ferrer.constituent_dots:
            dot.location = (dot.layer, dot.position_in_layer)
            dot.layer = min(dot.location[0], dot.location[1])
        ferrer.updateLayers()
        ferrer.updateCornerPosition()
        ferrer.updateDictionary()
        ferrer.updateParts()
        super().__init__(*animations)
    def check_if_input_is_ferrers_diagram(self, ferrer):
        if not isinstance(ferrer, FerrersDiagram):
            raise Exception("Convolution must take in a Ferrer's Diagram object")

class Conjugating(Rotating):
    CONFIG = {
        "run_time": .5,
        "rate_func": linear,
        "about_edge": None,
    }
    def __init__(self, ferrer):
        self.mobject = ferrer
        partition_sequence = ferrer.partition_sequence
        # update the diagram's partition_sequence property so it accurately reflects the conjugation
        conjugated_partition_sequence = []
        for i in range(max(partition_sequence)):
            conjugated_partition_sequence.append(sum(part > i for part in partition_sequence))
        print(list(ferrer.partition_sequence), "is conjugating to", conjugated_partition_sequence)
        ferrer.partition_sequence = conjugated_partition_sequence
        # update the location property for every dot.
        for dot in ferrer.constituent_dots:
            dot.location = dot.location[::-1]
        # update the coordinate dictionary based on each dots location.
        ferrer.updateDictionary()
        ferrer.updateParts()
    def check_if_input_is_ferrers_diagram(self, ferrer):
        if not isinstance(ferrer, FerrersDiagram):
            raise Exception("Convolution must take in a Ferrer's Diagram object")
    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)
        self.mobject.rotate(
            alpha * TAU/2,
            axis=np.array([1,-1,0]),
            about_point=self.mobject.updateCornerPosition(),
            about_edge=self.about_edge,
        )

class FerrersDiagramDemonstration(Scene):
    def construct(self):
        ferrer = FerrersDiagram(partition_sequence=np.array([3,7,9,5,7]))
        self.play(ShowCreation(ferrer))
        self.play(SortingParts(ferrer))
        self.play(Conjugating(ferrer))
        self.play(Convoluting(ferrer))