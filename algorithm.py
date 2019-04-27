from typing import List, Tuple
import networkx as nx
import numpy as np
from client import Client

class AmroshAlg:

    def __init__(self, client: Client) -> None:
        self.client: Client = client
        self.graph: nx.Graph = client.G
        self.n_nodes: int = self.graph.number_of_nodes()
        self.home: int = client.home
        self.bots: int = client.bots
        self.non_home: List[int] = list(range(1, client.home)) + \
                                   list(range(client.home + 1, client.v + 1))
        self.students: int = client.students

        self.bfs_T: nx.DiGraph = self._get_bfs_tree()

    def _get_bfs_tree(self) -> nx.DiGraph:
        """
        Finds the BFS tree starting from home on the MST of the graph
        """
        tree = nx.minimum_spanning_tree(self.graph)
        return nx.bfs_tree(tree, self.home)

    def get_info(self) -> Tuple[List[int], int]:
        """
        Get the bot locations by running the optimal sequence of scouts and remotes
        Greedily on the MST run remote on the nodes with largest number of yeses
        This will help us either find the lies or bots
        At the same time update the number of lies each person is telling
        Do this until someone exhausts all the lies he/she could tell
        Each person can lie for at most number of yeses + number of bots or half of the number of
        nodes, which ever is less.

        :returns
        List[int]: bot locations
        int: number of remotes used to narrow down bot locations
        """
        student_ans = {}
        for v in self.graph:
            if v is self.home:
                continue
            student_ans[v] = self.client.scout(v, list(range(1, self.students+1)))

        std_ans_arr = np.array([list(x.values()) for x in list(student_ans.values())])
        n_true = np.sum(std_ans_arr, axis=0)
        max_n_lies = np.minimum(n_true + self.bots, self.n_nodes//2)
        node_value = np.sum(std_ans_arr, axis=1)
        node_dict = dict(zip(self.non_home, node_value))
        std_lies_arr = np.array([0]*self.students)

        sorted_nodes = sorted(self.non_home, key=lambda x: node_dict[x],
                              reverse=True)

        marked = {}
        n_remote = 0
        for v in sorted_nodes:
            parent, _ = list(self.bfs_T.in_edges(v)).pop()
            n_remoted_bots = self.client.remote(v, parent)
            n_remote += 1
            marked[v] = True
            if n_remoted_bots != 0:
                # there was a bot in v
                std_lies_arr[std_ans_arr[v] == False] += 1
            else:
                # there was no bot in v
                std_lies_arr[std_ans_arr[v] == True] += 1

            honest_stds = np.where(std_lies_arr >= max_n_lies)[0]
            if len(honest_stds) != 0:
                honest_std = honest_stds[0]
                undiscovered_bot_locations = []
                for i, i_ans in enumerate(std_ans_arr[:, honest_std]):
                    if marked[i]:
                        continue
                    elif i_ans:
                        undiscovered_bot_locations.append(i)

                return undiscovered_bot_locations + self.client.bot_locations, n_remote

            if len(self.client.bot_locations) == self.bots:
                return self.client.bot_locations, n_remote

    def bring_home(self, bot_locations: List[int]) -> int:
        """
        On the MST of the graph find the bfs from home and move backwards on the tree
        call remote only on the nodes with bot in them
        :param
        bot_locations: list of bot locations
        :return:
        int: number of remote calls for bringing bots home
        """

        nodes = [self.home] + [v for u,v in self.bfs_T.edges()]
        n_remotes = 0
        bot_set = set(bot_locations)
        for v in reversed(nodes):
            try:
                if v in bot_set:
                    parent, _ = list(self.bfs_T.in_edges(v)).pop()
                    self.client.remote(v, parent)
                    bot_set.remove(v)
                    bot_set.add(parent)
                    if len(self.client.bot_locations) == self.bots:
                        bot_set = set(self.client.bot_locations)
                    n_remotes += 1
                    print("time: {}".format(self.client.time))
                    print("bot_count: {}".format(self.client.bot_locations))
            except IndexError:
                pass
        return n_remotes

    def run(self):
        bot_locs, n_discover_remotes = self.get_info()
        discover_time = self.client.time
        n_resque_remotes = self.bring_home(bot_locs)
        print(dict(n_scout_remotes=n_discover_remotes, n_extra_remotes=n_resque_remotes,
                   n_remotes=n_discover_remotes + n_resque_remotes,
                   discover_time=discover_time, total_time=self.client.time))
