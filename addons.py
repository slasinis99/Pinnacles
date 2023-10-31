import os
import main as pin

#############
# DISCOVERY #
#############

# def point_gen(n):
#     if (os.path.exists(f'points-{n}.pts')):
#         with open(f'points-{n}.pts', 'rb') as fp:
#             return pickle.load(fp)
#     points = []
#     base = distinct_graph_labelings(create_graph(n, 'cycle'), [3,5,7,n])[0]
#     for k in range(7, n):
#         #base = distinct_graph_labelings(create_graph(n, 'cycle'), [3,5,k,n])[0]
#         for j in range(5, k):
#             for i in range(3, j):
#                 p_set = [n, k, j, i]
#                 print(f'p_set = {p_set}')
#                 e = distinct_graph_labelings(create_graph(n, 'cycle'), [n, k, j, i])[0]
#                 points.append(((i, j, k), int(e / base)))
#     pickle.dump(points, open(f'points-{n}.pts', 'wb'))
#     return points

# def table_gen():
#     points = point_gen(10)
#     # Unpack the points and values
#     x, y, z = zip(*[point[0] for point in points])
#     values = [point[1] for point in points]

#     # Create a 3D scatter plot
#     fig = plt.figure()
#     ax = fig.add_subplot(111, projection='3d')
#     scatter = ax.scatter(x, y, z, c=values, cmap='viridis', marker='o')

#     # Add labels (optional)
#     ax.set_xlabel('i')
#     ax.set_ylabel('j')
#     ax.set_zlabel('k')

#     # Add hover text
#     annotations = [f'Value: {v}' for v in values]
#     mplcursors.cursor(hover=True).connect("add", lambda sel: sel.annotation.set_text(annotations[sel.index]))

#     # Add colorbar
#     fig.colorbar(scatter)

#     # Show the plot
#     plt.show()