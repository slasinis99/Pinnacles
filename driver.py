import main as m

def showState(state: int, graph_family: int = 0, node_count: int = 5, alt_node_count: int = 0, pinnacle_set: list = []):
    graph_family_name = ''
    if graph_family == m.GraphType.COMPLETE: graph_family_name = 'Complete'
    elif graph_family == m.GraphType.BIPARTITE: graph_family_name = 'Complete Bipartite'
    elif graph_family == m.GraphType.STAR: graph_family_name = 'Star'
    elif graph_family == m.GraphType.CYCLE: graph_family_name = 'Cycle'
    elif graph_family == m.GraphType.WHEEL: graph_family_name = 'Wheel'
    else: graph_family_name = 'None Selected'

    alt_node_desc = ''
    if graph_family == m.GraphType.BIPARTITE: alt_node_desc = ', Nodes on Left Split: '+str(alt_node_count)
    if graph_family == m.GraphType.STAR: alt_node_desc = ', Number of Stars: '+str(alt_node_count)

    if state == 0: #Main Menu
        print("-----------------------")
        print("Graph Pinnacle Labeling")
        print("-----------------------")
        print(f"Options (Graph Family: {graph_family_name}, Node Count = {node_count}{alt_node_desc}, Pinnacle Set = {pinnacle_set})")
        print("-----------------------")
        print('1 - Create a Graph')
        print('2 - Modify Pinnacle Set')
        print('3 - Run Calculator')
        print('4 - Exit')
        print('-------------------------')
        return m.get_digits(input("Please enter selection: ")), graph_family, node_count, alt_node_count, pinnacle_set
    elif state == 1: #Choose Graph Family
        print('--------------------')
        print('Graph Family Options')
        print('--------------------')
        print('1 - Complete')
        print('2 - Complete Bipartite')
        print('3 - Star')
        print('4 - Cycle')
        print('5 - Wheel')
        print('--------------------')
        print('6 - Go Back')
        print('7 - Exit')
        print('--------------------')
        choice = m.get_digits(input("Please enter selection: "))
        if choice == 1:
            return 11, graph_family, node_count, alt_node_count, pinnacle_set
        elif choice == 2:
            return 12, graph_family, node_count, alt_node_count, pinnacle_set
        elif choice == 3:
            return 13, graph_family, node_count, alt_node_count, pinnacle_set
        elif choice == 4:
            return 14, graph_family, node_count, alt_node_count, pinnacle_set
        elif choice == 5:
            return 15, graph_family, node_count, alt_node_count, pinnacle_set
        elif choice == 6:
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        else:
            exit()
    elif state == 11 or state == 14 or state == 15: #Graph not requiring more than the node count
        print("---------------------------------")
        print("How many vertices would you like?")
        print('---------------------------------')
        node_count = m.get_digits(input("Please enter choice: "))
        pinnacle_set = [node_count]
        if state == 11:
            return 0, m.GraphType.COMPLETE, node_count, alt_node_count, pinnacle_set
        if state == 14:
            return 0, m.GraphType.CYCLE, node_count, alt_node_count, pinnacle_set
        if state == 15:
            return 0, m.GraphType.WHEEL, node_count, alt_node_count, pinnacle_set
    elif state == 12: #Complete Bipartite node count selection
        print("---------------------------------")
        print("How many vertices would you like?")
        print('---------------------------------')
        value = m.get_digits(input("Please enter choice: "))
        if value >= 1:
            node_count = value
        pinnacle_set = [node_count]
        return 120, m.GraphType.BIPARTITE, node_count, alt_node_count, pinnacle_set
    elif state == 13: #Star node count selection
        print("---------------------------------")
        print("How many vertices would you like?")
        print('---------------------------------')
        value = m.get_digits(input("Please enter choice: "))
        if value >= 1:
            node_count = value
        pinnacle_set = [node_count]
        return 130, m.GraphType.STAR, node_count, alt_node_count, pinnacle_set
    elif state == 120: #Complete Bipartite node count for left half
        print('----------------------------------------')
        print('How many vertices on left side of graph?')
        print('----------------------------------------')
        value = m.get_digits(input("Please enter choice: "))
        if value >= 1:
            node_count = value
        return 0, graph_family, node_count, alt_node_count, pinnacle_set
    elif state == 130: #Stars inside graph count
        print('----------------------------------------')
        print('How many stars inside graph?')
        print('----------------------------------------')
        alt_node_count = m.get_digits(input('Please enter choice: '))
        return 0, graph_family, node_count, alt_node_count, pinnacle_set
    elif state == 2: #Menu for modifying the pinnacle set
        print('---------------------------')
        print('Modify Pinnacle Set Options')
        print('---------------------------')
        print('1 - Add Pinnacle')
        print('2 - Remove Pinnacle')
        print('3 - Reset Pinnacle Set')
        print('4 - Go Back')
        print('5 - Exit')
        print('---------------------------')
        choice = m.get_digits(input('Please enter selection: '))
        if choice in [1, 2, 3]:
            return 20+choice, graph_family, node_count, alt_node_count, pinnacle_set
        elif choice == 4:
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        else:
            exit()
    elif state == 21: #Adding a value to the pinnacle set
        print('---------------------------------------------------------------------------')
        print(f'Add Value to Pinnacle Set: {pinnacle_set}')
        print(f'Note: Each number in the pinnacle set must be distinct and must contain {node_count}')
        print('---------------------------------------------------------------------------')
        value = m.get_digits(input(f"Please enter a value in [1, {node_count-1}]: "))
        if value >= 1 and value <= node_count and not value in pinnacle_set:
            pinnacle_set.append(value)
            pinnacle_set = sorted(pinnacle_set, reverse=True)
        return 2, graph_family, node_count, alt_node_count, pinnacle_set
    elif state == 22: #Removing a value from the pinnacle set
        print(f'--------------------------------------'+(len(pinnacle_set)+2)*'-')
        print(f'Remove a value from the Pinnacle Set: {pinnacle_set}')
        print(f'--------------------------------------'+(len(pinnacle_set)+2)*'-')
        value = m.get_digits(input(f'Please enter a value in the pinnacle set less than {node_count}: '))
        if value < node_count and value in pinnacle_set:
            pinnacle_set.remove(value)
        return 2, graph_family, node_count, alt_node_count, pinnacle_set
    elif state == 23: #Resetting the pinnacle set
        print(f'-------------------------')
        print(f'Resetting Pinnacle Set...')
        print(f'-------------------------')
        pinnacle_set = [node_count]
        print(f'Pinnacle Set has been Reset: {pinnacle_set}')
        return 2, graph_family, node_count, alt_node_count, pinnacle_set
    elif state == 3: #Calculate the number of labelings
        s = ''
        if not graph_family in [m.GraphType.BIPARTITE, m.GraphType.COMPLETE, m.GraphType.CYCLE, m.GraphType.STAR, m.GraphType.WHEEL]:
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        if graph_family == m.GraphType.COMPLETE:
            g = m.create_graph(node_count, 'complete')
            t = m.distinct_graph_labelings(g, pinnacle_set)[0]
            print('--------------------------------------')
            print('Graph Family: Complete')
            print(f'Vertex Count: {node_count}')
            print(f'Pinnacle Set: {pinnacle_set}')
            print('--------------------------------------')
            print(f'Number of Distinct Labelings: {t}')
            print(f'-------------------------------------')
            input(f'Press Enter to Continue')
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        elif graph_family == m.GraphType.BIPARTITE:
            g = m.create_graph(node_count, 'bipartite'+str(alt_node_count))
            t = m.distinct_graph_labelings(g, pinnacle_set)[0]
            print('--------------------------------------')
            print('Graph Family: Complete Bipartite')
            print(f'Vertex Count: {node_count}')
            print(f'Vertices in left half: {alt_node_count}')
            print(f'Pinnacle Set: {pinnacle_set}')
            print('--------------------------------------')
            print(f'Number of Distinct Labelings: {t}')
            print(f'-------------------------------------')
            input(f'Press Enter to Continue')
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        elif graph_family == m.GraphType.CYCLE:
            g = m.create_graph(node_count, 'cycle')
            t = m.distinct_graph_labelings(g, pinnacle_set)[0]
            print('--------------------------------------')
            print('Graph Family: Cycle')
            print(f'Vertex Count: {node_count}')
            print(f'Pinnacle Set: {pinnacle_set}')
            print('--------------------------------------')
            print(f'Number of Distinct Labelings: {t}')
            print(f'-------------------------------------')
            input(f'Press Enter to Continue')
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        elif graph_family == m.GraphType.STAR:
            g = m.create_graph(node_count, 'star'+str(alt_node_count))
            t = m.distinct_graph_labelings(g, pinnacle_set)[0]
            print('--------------------------------------')
            print('Graph Family: Star')
            print(f'Vertex Count: {node_count}')
            print(f'Vertices Star Center: {alt_node_count}')
            print(f'Pinnacle Set: {pinnacle_set}')
            print('--------------------------------------')
            print(f'Number of Distinct Labelings: {t}')
            print(f'-------------------------------------')
            input(f'Press Enter to Continue')
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
        elif graph_family == m.GraphType.WHEEL:
            g = m.create_graph(node_count, 'wheel')
            t = m.distinct_graph_labelings(g, pinnacle_set)[0]
            print('--------------------------------------')
            print('Graph Family: Wheel')
            print(f'Vertex Count: {node_count}')
            print(f'Pinnacle Set: {pinnacle_set}')
            print('--------------------------------------')
            print(f'Number of Distinct Labelings: {t}')
            print(f'-------------------------------------')
            input(f'Press Enter to Continue')
            return 0, graph_family, node_count, alt_node_count, pinnacle_set
    else: #When all else fails, exit the program
        exit()


def main():
    state = 0
    graph_family = 0
    node_count = 0
    alt_node_count = 0
    pinnacle_set = []
    while state >= 0:
        state, graph_family, node_count, alt_node_count, pinnacle_set = showState(state, graph_family, node_count, alt_node_count, pinnacle_set)

if __name__ == "__main__":
    main()