import networkx as nx
import matplotlib.pyplot as plt

def plot_example(seed, number_of_students, project_supervisors, student_preferences):
    """_summary_

    Args:
        seed (_type_): _description_
        number_of_students (_type_): _description_
        project_supervisors (_type_): _description_
        student_preferences (_type_): _description_
    """
    # Create a bipartite graph
    G = nx.Graph()

    # Add nodes with the node attribute 'bipartite'
    list_of_projects = sorted(project_supervisors.keys())
    G.add_nodes_from(range(1, number_of_students+1), bipartite=0)  # Set bipartite=0 for the first set of nodes
    G.add_nodes_from(list_of_projects, bipartite=1)  # Set bipartite=1 for the second set of nodes

    # Add edges between the two sets of nodes
    applications = []
    for stud in student_preferences:
        selected_projs = student_preferences[stud]
        for proj in selected_projs:
            applications.append((stud, proj))
    G.add_edges_from(applications)

    # Get bipartite layout
    pos = nx.bipartite_layout(G, nodes=range(1, number_of_students+1), scale=5)

    fig, ax = plt.subplots(figsize=(6, 30))

    # Draw the bipartite graph
    nx.draw(G, 
            pos = pos, 
            with_labels =True, 
            font_weight = 'bold', 
            font_size = 4,
            node_color = ['skyblue']*number_of_students + ['lightcoral']*len(list_of_projects), 
            node_size = 50,
            ax = ax)

    plt.title(f'Stable matching example (generated by seed={seed})')
    plt.savefig("tests/results/plots/example.png", dpi=100)
    plt.clf()


def plot_results(number_of_students, project_supervisors, student_preferences, matching):
    """_summary_

    Args:
        number_of_students (_type_): _description_
        project_supervisors (_type_): _description_
        student_preferences (_type_): _description_
        matching (_type_): _description_
    """
    # Create a bipartite graph
    G = nx.Graph()

    # Add nodes with the node attribute 'bipartite'
    list_of_projects = sorted(project_supervisors.keys())
    G.add_nodes_from(range(1, number_of_students+1), bipartite=0)  # Set bipartite=0 for the first set of nodes
    G.add_nodes_from(list_of_projects, bipartite=1)  # Set bipartite=1 for the second set of nodes

    # Add edges between the two sets of nodes
    applications = []
    for stud in student_preferences:
        selected_projs = student_preferences[stud]
        for proj in selected_projs:
            applications.append((stud, proj))
    G.add_edges_from(applications)

    # Get bipartite layout
    pos = nx.bipartite_layout(G, 
                            nodes=range(1, number_of_students+1),
                            scale=5)

    fig, ax = plt.subplots(figsize=(6, 30))

    # Color the matching results
    matching_edges = [(f'{stud}', f'{proj}') for proj, students_matched in matching.items() for stud in students_matched]

    # Draw the bipartite graph
    nx.draw(G, 
            pos = pos, 
            with_labels =True, 
            font_weight = 'bold', 
            font_size = 4,
            node_color = ['skyblue']*number_of_students + ['lightcoral']*len(list_of_projects), 
            node_size = 50,
            edge_color = ['red' if (f'{edge[0]}', f'{edge[1]}') in matching_edges else 'black' for edge in G.edges()],
            ax = ax)

    plt.title(f'Stable matching solution')
    plt.savefig("tests/results/plots/solution.png", dpi=100)
    plt.clf()