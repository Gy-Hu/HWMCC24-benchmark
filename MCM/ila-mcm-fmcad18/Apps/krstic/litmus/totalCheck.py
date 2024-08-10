# total check 
def check(edgeList):
    # build in degree and out degree
    if len(edgeList) == 1 and edgeList[0][0] == edgeList[0][1]:
        gid = edgeList[0][0]
        return set([gid]), [gid]
        
    indegree = {}
    outdegree = {}
    nodeSet  = set([])
    for id1,id2 in edgeList:
        outdegree[id1] = outdegree.get(id1,0) + 1
        indegree[id2]  = indegree.get(id2,0) + 1
        nodeSet.add(id1)
        nodeSet.add(id2)

    #print indegree
    #print outdegree
    #print nodeSet
    for node in nodeSet:
        indegree[node] = indegree.get(node,0)
        outdegree[node] = outdegree.get(node,0)

    # pop untill empty
    # make sure only one is possible
    orderList = []
    allNode   = set([])
    while allNode != nodeSet:
        # find in degree = 0
        targetID = None
        for nodeId, deg in indegree.items():
            if deg == 0:
                if targetID is None:
                    targetID = nodeId
                else: # make sure only one is total
                    print '<E> po relation is not total!'
                    assert False
        if targetID is None:
            print '<E> cyclic po relation!'
            assert False
        # remove all related edges
        for id1,id2 in edgeList:
            if id1 == targetID:
                assert indegree[id2] > 0
                indegree[id2] -= 1
        del indegree[targetID]

        allNode.add(targetID)
        orderList.append(targetID)

    return allNode,orderList


if __name__ == '__main__':
    print check([(1,2),(2,3),(2,4),(3,4)])
