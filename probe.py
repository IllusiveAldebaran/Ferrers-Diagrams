from manim import *
from ferrers_patching import ferrers_diagram as fer


class FerrersDiagramDemonstration(Scene):

    def construct(self):
        ferrers_diagram = fer.FerrersDiagram(partition_sequence=np.array([12,11,10,9,5,4]), shape="square", color="#46a0ee", center_x=-3, center_y=2).scale(.8)
        
        text = Text("Franklin Involution").next_to(ferrers_diagram, direction=UP, buff=SMALL_BUFF).scale(.5)
        ferrers_diagram2 = fer.FerrersDiagram(partition_sequence=np.array([7,6,5,3,1]), color="#8949d2", center_x=3, center_y=2)
        text2 = Text("Conjugation").next_to(ferrers_diagram2, direction=UP, buff=SMALL_BUFF).scale(.5)
        ferrers_diagram3 = fer.FerrersDiagram(partition_sequence=np.array([3,11,8,12,7,14]), color="#3ae9d5", center_x=-3, center_y=-2)
        text3 = Text("Sorting Parts").next_to(ferrers_diagram3,direction=UP, buff=SMALL_BUFF).scale(.5)
        ferrers_diagram4 = fer.FerrersDiagram(partition_sequence=np.array([8,7,5,5,3,1]), shape="square", color="#e87335", center_x=3, center_y=-2)
        text4 = Text("Convolution").next_to(ferrers_diagram4, direction=UP, buff=SMALL_BUFF).scale(.5)

        # self.play(Create(ferrers_diagram), Create(text))
        # self.play(FranklinInvoluting(ferrers_diagram))
        # pprint.pprint(dir(FerrersDiagram))
        # pprint.pprint(vars(FerrersDiagram))
        # ferrers_diagram.informMe()
        # self.play(CustomAnimation(ferrers_diagram))

        # creation
        self.play(Create(ferrers_diagram), Create(ferrers_diagram2), Create(ferrers_diagram3), Create(ferrers_diagram4), Create(text), Create(text2),Create(text3), Create(text4))
        # animations
        # self.play(Create(ferrers_diagram), Create(ferrers_diagram4), Create(ferrers_diagram4))
        self.play(fer.FranklinInvoluting(ferrers_diagram), fer.SortingParts(ferrers_diagram3), fer.Convoluting(ferrers_diagram4))

        # self.play(Conjugating(ferrers_diagram2))

        self.wait(1)