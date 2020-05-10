from variables import P1, P2


def init_sigma(node):
    sigma = {}

    def dfs(node):
        sigma[node.inf_set] = {action: 1/len(node.actions) for action in node.actions}
        for child_node in node.children.values():
            dfs(child_node)

    dfs(node)
    return sigma


def init_cumulative_vector(node):
    cumulative_vector = {}

    def dfs(node):
        cumulative_vector[node.inf_set] = {action: 0 for action in node.actions}
        for child_node in node.children.values():
            dfs(child_node)

    dfs(node)
    return cumulative_vector


def update_reaching_I_probs(node, sigma):
    reaching_probs = {}

    def dfs(node, probs, sigma):
        
        for player, prob in probs.items():
            if node.inf_set not in reaching_probs.keys():
                reaching_probs[node.inf_set] = {P1: 0, P2: 0}
            reaching_probs[node.inf_set][player] += prob

        for action in node.actions:
            child_probs = probs.copy()
            if node.state in [P1, P2]:
                child_probs[node.state] *= sigma[node.inf_set][action]
            child_node = node.children[action]
            dfs(child_node, child_probs, sigma)

    probs = {P1: 1, P2: 1}
    dfs(node, probs, sigma)
    return reaching_probs


def update_reaching_h_probs(node, probs, sigma):

    node.reaching_h_probs = probs
    for action in node.actions:
        child_probs = probs.copy()
        if node.state in [P1, P2]:
            child_probs[node.state] *= sigma[node.inf_set][action]
        child_node = node.children[action]
        update_reaching_h_probs(child_node, child_probs, sigma)
