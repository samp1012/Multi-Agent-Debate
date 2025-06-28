import networkx as nx
import matplotlib.pyplot as plt

def create_dag():
    G = nx.DiGraph()

    G.add_node("UserInputNode")
    G.add_node("AgentNode")
    G.add_node("Memory")
    G.add_node("JudgeNode")

    G.add_edge("UserInputNode", "AgentNode")
    G.add_edge("AgentNode", "Memory")
    G.add_edge("Memory", "AgentNode")
    G.add_edge("Memory", "JudgeNode")

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", arrowsize=20, font_size=10)
    plt.title("Multi-Agent Debate DAG")
    plt.savefig("dag_diagram.png")
    plt.show()

if __name__ == "__main__":
    create_dag()