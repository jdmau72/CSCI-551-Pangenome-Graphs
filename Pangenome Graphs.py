import networkx as nx
import matplotlib.pyplot as plt
import Sequence
from string import digits

# takes in a prealigned list of sequences and builds a variation graph
def buildVariationGraph(sequenceList):
    G = nx.DiGraph()

    longest = len(max(sequenceList, key = len))

    # initialize empty character array of length of the longest sequence
    characters = []
    for i in range(longest):
        characters.append([])

    # for each index i, gets a set of unique characters in s[i] for all s
    for i in range(longest):
        for s in sequenceList:
            if ((s[i] in characters[i]) == False):    # if character not already added
                characters[i].append(s[i])
    print(characters)

    
    # compresses singletons
    print("Compressing characters...")
    compressed_characters = []
    for i in range(longest - 1):
        if ((len(characters[i]) == 1) and (len(characters[i+1]) == 1)): # both are singletons
            print(f"{characters[i][0]} + {characters[i+1][0]} = {characters[i][0] + characters[i+1][0]}")
            characters[i + 1] = [characters[i][0] + characters[i+1][0]]
        else:
            compressed_characters.append(characters[i])
    compressed_characters.append(characters[longest-1])
    print(compressed_characters)

    # adds those compressed characters to the graph as nodes
    labels = {}
    for i, compress in enumerate(compressed_characters):
        for c in compress:
            if (c != "-"):  # now that skip edges are accounted for, don't need these blank nodes
                G.add_node((c + str(i)), layer=i)
                labels[(c+str(i))] = c  # adds the label to the dictionary, so there can be multiple nodes with the same label

    print()

    # adding edges (with skips?)
    skipEdges = []
    for s in sequenceList:
        print(f"\nSequence {s}")
        current = 0
        substring_A = ""
        substring_B = ""
        for i in range(len(compressed_characters) - 1):        
            if (substring_B != "-"):
                substring_A = s[current: current + len(compressed_characters[i][0])]
                node_A = substring_A + str(i)

                current = current + len(compressed_characters[i][0])   # moves current to end of currnet substring
                substring_B = s[current: current + len(compressed_characters[i+1][0])]
                node_B = substring_B + str(i+1)
                print(f"A: {substring_A}        B: {substring_B}        compressed_characters: {compressed_characters[i]}       nodeA: {node_A}     nodeB: {node_B}")

                if(substring_B in compressed_characters[i+1] and substring_B != "-"):
                    # checks if edge already exists
                    if not node_B in G[node_A]:
                        G.add_edge(node_A, node_B)

            else: # so if the previous one was a "-"
                # will only update B and current
                current = current + len(compressed_characters[i][0])   # moves current to end of currnet substring
                substring_B = s[current: current + len(compressed_characters[i+1][0])]
                node_B = substring_B + str(i+1)
                print(f"A: {substring_A}        B: {substring_B}        compressed_characters: {compressed_characters[i]}       nodeA: {node_A}     nodeB: {node_B}")
                if (substring_B in compressed_characters[i+1] and substring_B != "-"):
                    if not node_B in G[node_A]:
                        # instead of adding the edge, since it needs to curve to be seen, adds it to a list that will get added to the graph later
                        skipEdges.append((node_A, node_B))


    # draw the G
    plt.figure()
    pos = nx.multipartite_layout(G, subset_key="layer")
    nx.draw(G, pos, labels= labels, arrows= True, with_labels = True)

    # # makes the edges that would overlap curve
    for edge in skipEdges:
        nx.draw_networkx_edges(G, pos, edgelist=[edge], edge_color='black', connectionstyle='arc3,rad=0.3')
    #plt.show()
    plt.title("Variation Graph")

    return G


    

# builds a pangenome graph by splitting them into k-sized blocks
def buildBlockGraph(sequenceList, k):
    G = nx.DiGraph()

    longest = len(max(sequenceList, key = len))
    if (longest % k == 0):
        numBlocks = int(longest / k)
    else:
        numBlocks = int(longest / k) + 1

    for i in range(numBlocks):
        blockList.append([])

    for s in sequenceList:
        for i in range(numBlocks):
            blockList[i].append(s[k * (i) : k * (i+1)])
            print(blockList[i])

    # get layers for displaying nicely
    layers = []
    for i, block in enumerate(blockList):
        layers.append(list(dict.fromkeys(block)))
        # print(list(dict.fromkeys(block)))
        G.add_nodes_from(list(dict.fromkeys(block)), layer = i)
        print(f"block: {block}")

    for iseq, s in enumerate(sequenceList):
        for iblock in range(numBlocks - 1): # -1 since last block wont have any outgoing edges
                #print(blockList[iblock][iseq], end="")
                if(blockList[iblock + 1][iseq] != ''):
                    G.add_edge(blockList[iblock][iseq], (blockList[iblock + 1][iseq]), )
                    print(f"Edge: {(blockList[iblock][iseq], (blockList[iblock + 1][iseq]))}")

    plt.figure()
    pos = nx.multipartite_layout(G, subset_key="layer")
    nx.draw(G, pos, arrows=True, with_labels = True)
    plt.title("Block Graph")
    # plt.show()

    return G




# MAIN -------------------------------------------------
BLOCK_SIZE = 6
blockList = []

sequenceList = Sequence.readFASTA("default.fasta", names = False)
# sequenceList = Sequence.readFASTA("multiFASTA.fasta", names = False)
# sequenceList = Sequence.readFASTA("test2.fasta", names = False)

blockGraph = buildBlockGraph(sequenceList, k= BLOCK_SIZE)

# variationGraph = buildVariationGraph(sequenceList)

sequenceList_variation = Sequence.readFASTA("prealigned.fasta", names = False)
variationGraph = buildVariationGraph(sequenceList_variation)

plt.show()