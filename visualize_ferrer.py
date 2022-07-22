from manim import *
from ferrers_patching import ferrers_diagram as fer
import json

class FerrersDiagramDemonstration(Scene):
    def construct(self):
        self.add(visualize())


def readPartitions():
    """Reads from a file for the partitions we want to visualize
    Returns
    ------------------------
    list of lists numbered with partitions
    """
    

    print("anything?")
    with open("partitions.txt") as f:
        lst = json.load(f)
    f.close()

    print("afterwards:")
    print(lst)
    print(type(lst))

    return lst


def visualize():
    """Returns an animation of a set of Ferrer_diagram mobject
    Reads the partition in partitions.list
    
    Returns
    ------------
    Returns an animation group
    """
                        #!FIXME: Maybe add a funciton that changes the size of these FerrerDiagrams based on their space?

    pa_list = readPartitions()
    # Completely arbitrary. I just like these colors to appear for different partitions
    my_colors = [RED_D,GREEN_D,BLUE_D,YELLOW_D,PURPLE_D,ORANGE]

    mobs = VGroup() # The group of partitions in one place
    
    sum_blocks = 0
    average_block = 0
    count = 0

    # The animation will be all on the same line. Find size needed.
    for i in range(len(pa_list)):
        sum_blocks += pa_list[i][0]

    average_block = sum_blocks/len(pa_list)

    all_blocks = average_block*(2*len(pa_list) + 1)
    
    for i in range(len(pa_list)):
        mobs.add(fer.FerrersDiagram(partition_sequence=pa_list[i], shape="square", color=my_colors[i%len(my_colors)],
        center_x=
                (average_block*1    # starting point
                +count              # the amount added by a block and the space following it
                +pa_list[i][0]/2    # from center of the mobject
                )/all_blocks * 14 - 7
                ))

        count += pa_list[i][0] + average_block  # amount of space before it
        
    return mobs


#!FIXME: NOT YET IMPLEMENTED
def isPartition():
    """Checks that a list is a partition

    """

    return False



# def debugAnimateGroup():
#     """
#     Parameters
#     --------------
#     nothing at this time for this test function
#     
#     Returns
#     --------------
#     A VGroup() of all elements on a screen for the partitions needed
#     """
#     mobs = VGroup()
# 
#     diagram = fer.FerrersDiagram(partition_sequence=np.array([9,5,5,2]), shape="square", center_x=-4, center_y=0)
#     diagram2 = fer.FerrersDiagram(partition_sequence=np.array([8,3,1,1]), shape="square", center_x=4, center_y=0)
# 
#     
#     mobs.add(diagram, diagram2)  # maybe add an asterisk before this? Maybe it's needed if it's a list
# 
#     return mobs