#import necessary library
from queue import LifoQueue
import pydot
import numpy as np
import pydot
#initial state decleration where M=3,C=3, side=0(left)
initial_state= [3,3,0]	

#class to compute the node validity, its depth and graph using pydot
class Node:
    goal_state=[0,0,1]
    num_of_instances=0
    def __init__(self,state,parent,action,depth):
        self.parent=parent
        self.state=state
        self.action=action
        self.depth=depth
        if self.is_killed():
            color="red"
        elif self.goal_test():
            color="green"
        else:
            color="white"
        self.graph_node = pydot.Node(str(self), style="filled", fillcolor=color)
        Node.num_of_instances+=1

    def __str__(self):
        return str(self.state)

    def goal_test(self):
        if self.state == self.goal_state:
            return True
        return False

    def is_valid(self):
        missionaries = self.state[0]
        cannibals = self.state[1]
        boat = self.state[2]
        if missionaries < 0 or missionaries > 3:
            return False
        if cannibals < 0 or cannibals > 3:
            return False
        if boat > 1 or boat < 0:
            return False
        return True

    def is_killed(self):
        missionaries = self.state[0]
        cannibals = self.state[1]
        if missionaries < cannibals and missionaries > 0:
            return True
        if missionaries > cannibals and missionaries < 3 :
            return True

    def generate_child(self):
        children=[]
        depth = self.depth + 1
        op = 1  
        if self.state[2] == 1:
            op = -1  

        for x in range(3):
            for y in range(3):
                new_state=self.state.copy()
                new_state[0],new_state[1],new_state[2]=new_state[0]- op * x, new_state[1]- op * y, new_state[2] + op * 1
                action=[x,y,op]
                new_node=Node(new_state, self, action, depth)
                if x + y >= 1 and x + y <= 2 :
                    children.append(new_node)
        return children  

    def find_solution(self):
        solution = []
        solution.append(self.action)
        path = self
        while path.parent != None:
            path = path.parent
            solution.append(path.action)
        solution = solution[:-1]
        solution.reverse()
        return solution

#the dfs implementation of the missionary and cannibals problems
def dfs(initial_state):
    graph = pydot.Dot(graph_type='digraph',label=" DFS implementation \n State Space tree where white is active node \n red is dead node  \n green is goal node\nSubmitted by: Aayush Dip Giri\nRoll no 16",fontsize="24", color="black",
                                                    fontcolor="black",  style="filled", fillcolor="black")
    start_node = Node(initial_state, None, None,0)      
    if start_node.goal_test():
        return start_node.find_solution()
    stack = LifoQueue()
    stack.put(start_node)
    explored=[]
    killed=[]
    print("\n\nDFS implementation\n")
    print(" Start node "+ str(start_node.state)+"  level=%d"%start_node.depth)
    while not(stack.empty()):
        node=stack.get()
        print("\nNode to be expanded  "+str(node.state))  
        explored.append(node.state)
        graph.add_node(node.graph_node)
        if node.parent:
            diffrence=np.subtract(node.parent.state,node.state)
            if node.parent.state[2]==1:             
                diffrence[0],diffrence[1]=-diffrence[0],-diffrence[1]       
            graph.add_edge(pydot.Edge(node.parent.graph_node, node.graph_node,label=str(diffrence)))
        children=node.generate_child()
        if not node.is_killed():
            print(" Child nodes \n",end="")
            for child in children:
                if child.state not in explored:
                    print(str(child.state)+"\tlevel=%d" % child.depth)
                    if child.goal_test():
                        print(" goal state since final output is [0,0,1]\n")
                        graph.add_node(child.graph_node)
                        diffrence = np.subtract(node.parent.state, node.state)
                        if node.parent.state[2] == 1:              
                            diffrence[0], diffrence[1] = -diffrence[0], -diffrence[1]     

                        graph.add_edge(pydot.Edge(child.parent.graph_node, child.graph_node,label=str(diffrence)))

                        # colour all leaves blue
                        leafs = {n.get_name(): True for n in graph.get_nodes()}
                        for e in graph.get_edge_list():
                            leafs[e.get_source()] = False
                        for leaf in leafs:
                            if leafs[leaf] and str(leaf) not in killed and str(leaf)!="\"[0, 0, 1]\"":          #[0,0,1]
                                node = pydot.Node(leaf, style="filled", fillcolor="blue")
                                graph.add_node(node)

                        graph.write_png('final.png')

                        return child.find_solution()
                    if child.is_valid():
                        stack.put(child)
                        explored.append(child.state)

        else:
            print("This node is killed")
            killed.append("\""+str(node.state)+"\"")

    return

if __name__ == "__main__":
    solution=dfs(initial_state)
    print('Our solution nodal path is :', solution)