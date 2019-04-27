import networkx as nx
from algorithm import AmroshAlg

def solve(client):
    client.end()
    client.start()

    # instance_name = 'toronto_29_1'
    # arg_file = instance_name.rsplit('_', 1)[0] + '.json'
    # with open('test_graphs/{}'.format(arg_file), 'r') as f:
    #     graph_data = json.load(f)
    # instance = dict()
    # for _instance in graph_data['instances']:
    #     if _instance['instanceName'].lower() == instance_name.lower():
    #         instance = _instance
    #         break

    alg = AmroshAlg(client)
    alg.run()

    client.end()

def test_nx():
    g = nx.Graph()
    g.add_weighted_edges_from([(1,2,1), (2,3,1), (3,4,1), (4,5,100), (2,5,100), (3,5,1)])

if __name__ == '__main__':
    test_nx()
