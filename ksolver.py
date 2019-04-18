import networkx as nx

def algorithm(client, G, bots, home):
    T = nx.minimum_spanning_tree(G)
    bfs_T = nx.bfs_tree(T, home)
    nodes = [home] + [v for u,v in bfs_T.edges()]
    for v in reversed(nodes):
        try:
            parent, _ = list(bfs_T.in_edges(v)).pop()
            if v in bots:
                # print("remote(%d, %d)"%(v, parent))
                bots.remove(v)
                bots.append(parent)
                client.remote(v, parent)
                print("time: {}".format(client.time))
                print("bot_count: {}".format(client.bot_locations))
        except IndexError:
            pass

def solve(client):
    client.end()
    client.start()

    all_students = list(range(1, client.students + 1))
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    # bot_locs = non_home
    bot_locs = [47, 97, 74, 92, 75]
    algorithm(client, client.G, bot_locs, client.h)
    client.end()


def test_nx():
    g = nx.Graph()
    g.add_weighted_edges_from([(1,2,1), (2,3,1), (3,4,1), (4,5,100), (2,5,100), (3,5,1)])
    algorithm(None, g, [3,5, 4], 1)

if __name__ == '__main__':
    test_nx()