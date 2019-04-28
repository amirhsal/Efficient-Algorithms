import networkx as nx
from algorithm import AmroshAlg

def solve(client):
    client.start()

    alg = AmroshAlg(client)
    result = alg.run()
    print(result)

    client.end()

def test_nx():
    g = nx.Graph()
    g.add_weighted_edges_from([(1,2,1), (2,3,1), (3,4,1), (4,5,100), (2,5,100), (3,5,1)])

if __name__ == '__main__':
    test_nx()
