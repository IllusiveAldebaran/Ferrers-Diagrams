from manim import *

class Young(Scene):

    def construct(self):
        partition = [5,4,2,1]

        young_diagram(partition)

        square1 = Square()
        square2 = Square()
        square3 = Square()
        

        self.play(FadeIn(square1, square2, square3), run_time = 3)





def young_diagram(part_list):
    """ Makes a young diagram of elemnts in part_list"""
    #!FIXME need to make sure part_list is a list of integers

    # make sure it is a partition
    if (len(part_list) == 0):
        return  -1

    for i in range(len(part_list)-1):
        if part_list[i+1] < part_list[i]:
            return -1
    
    # create young diagram
    partition = []
    for i in part_list:
        temp_p = []
        temp_p.append(Square())

        #!FIXME ADD FOR OTHER ROWS
        for j in range(i-1):
            partition.append(Square().align_to(temp_p.get_right))
            print(partition)


    # return partition object
    return partition
