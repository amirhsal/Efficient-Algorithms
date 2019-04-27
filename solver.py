import networkx as nx
from algorithm import AmroshAlg
import json

def solve(client):
    args = [{}, {'is_bot_loc_known':True}, {'assume_bot_everywhere':True}]
    results = []
    for arg in args:
        client.start()

        instance_name = 'singapore_0_2'
        arg_file = instance_name.rsplit('_', 1)[0] + '.json'
        with open('test_graphs/{}'.format(arg_file), 'r') as f:
            graph_data = json.load(f)
        instance = dict()
        for _instance in graph_data['instances']:
            if _instance['instanceName'].lower() == instance_name.lower():
                instance = _instance
                break

        alg = AmroshAlg(client, bot_loc=instance['bots'])
        result = alg.run(**arg)
        # print(result)
        results.append(result)

        client.end()
    print(results)

def test_nx():
    g = nx.Graph()
    g.add_weighted_edges_from([(1,2,1), (2,3,1), (3,4,1), (4,5,100), (2,5,100), (3,5,1)])

if __name__ == '__main__':
    test_nx()
