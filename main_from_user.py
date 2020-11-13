from plotter import Plotter
from main_from_file import *

def main():
    plotter = Plotter()

    print("read polygon.csv")
    path = input("Input the name of the relative path of your polygon (include .csv): ")
    res = import_csv(path)
    # print(res)
    poly_x, poly_y, poly = res[1], res[2], list(zip(res[1], res[2]))
    #poly_ = [poly_x], [poly_y]
    plotter.add_polygon(res[1], res[2])

    # first create the mbr from the polygon
    mbr = MBR(res)
    poly_mbr = mbr.mbr_coords()
    print(poly_mbr)
    plotter.add_poly_outline(poly_mbr[0], poly_mbr[1])
    #
    # # print("Insert point information")
    x = float(input("x coordinate: "))
    y = float(input("y coordinate: "))
    point = [(x, y)]

    # calculate if the point is inside the MBR
    mbr_test = InsideMBR(([x], [y]), poly_mbr[0], poly_mbr[1])
    mbr_output = mbr_test.is_inside()
    is_inside_mbr = mbr_output[0]
    is_outside_mbr = mbr_output[1]

    # plot the point if outside Minimum Boundary Rectangle
    if len(is_inside_mbr) == 0:
        plotter.add_point(is_outside_mbr[0][0], is_outside_mbr[0][1], 'outside')

    # If inside MBR check if a vertex or on boundary
    inside_mbr_points = Boundary(is_inside_mbr, poly)
    on_vertex = inside_mbr_points.on_vertex()

    classification = []
    # plot point if on vertex
    if len(on_vertex) != 0:
        plotter.add_point(on_vertex[0][0], on_vertex[0][1], 'boundary')
        classification.append('boundary')
    else:
        point_on_line = inside_mbr_points.points_on_line()

        # check if the point is on boundary
        if len(point_on_line[0]) != 0:
            plotter.add_point(point_on_line[0][0][0], point_on_line[0][0][1], 'boundary')
            classification.append('boundary')

        else:
            not_classified = RayCasting(point, poly)
            final_round = not_classified.rca()
            inside_poly = final_round[0]
            outside_poly = final_round[1]

            # Plot if inside or outside polygon
            if len(inside_poly) !=0:
                plotter.add_point(inside_poly[0][0], inside_poly[0][1], 'inside')
                classification.append('inside')
            else:
                plotter.add_point(outside_poly[0][0], outside_poly[0][1], 'outside')
                classification.append('outside')

    if classification[0] == 'boundary':
        print(f'Your chosen point is on the {classification[0]} of the polygon')
    else:
        print(f'Your chosen point is {classification[0]} the polygon')
    plotter.show()


if __name__ == "__main__":
    main()
