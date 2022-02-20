from SolutionDrawer import SolDrawer
from VRP_Model import *


class Solution:
    def __init__(self):
        self.cost = 0.0
        self.routes = []


class RelocationMove(object):
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None

        self.costChangeOriginRt = None
        self.costChangeTargetRt = None

        self.timeChangeOriginRt = None
        self.timeChangeTargetRt = None

        self.moveCost = None
        self.timeCost = None

    def Initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None

        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9
        self.timeCost = 0


class SwapMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = None
        self.timeCost = None
        self.timeChangeFirstRoute = None
        self.timeChangeSecondRoute = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.costChangeFirstRt = None
        self.costChangeSecondRt = None
        self.moveCost = 10 ** 9
        self.timeCost = 0


class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None

    def Initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9


class CustomerInsertion(object):
    def __init__(self):
        self.customer = None
        self.route = None
        self.cost = 10 ** 9
        self.timecost = 0  # add auto


class Solver:
    def __init__(self, m):
        self.allNodes = m.allNodes
        self.customers = m.customers
        self.depot = m.allNodes[0]
        self.distanceMatrix = m.matrix_distance
        self.timeMatrix = m.matrix_time
        self.capacity = m.capacity
        self.timecapacity = 0.25 * 60
        self.trucks = m.trucks
        self.sol = None
        self.bestSolution = None

    def solve(self):
        self.SetRoutedFlagToFalseForAllCustomers()
        self.ApplyNearestNeighborMethod()
        self.ReportSolution()
        self.LocalSearch(2)
        self.ReportSolution()
        self.LocalSearch(1)
        self.ReportSolution()
        self.LocalSearch(0)
        self.ReportSolution()
        self.VND()
        self.ReportSolution()
        return self.sol

    def SetRoutedFlagToFalseForAllCustomers(self):
        for i in range(0, len(self.customers)):
            self.customers[i].isRouted = False


    def ApplyNearestNeighborMethod(self):
        modelIsFeasible = True
        self.sol = Solution()
        insertions = 0

        while (insertions < len(self.customers)):
            bestInsertion = CustomerInsertion()

            min_change = 10 ** 13
            min_best_insertion_point = None

            for i in range(0, len(self.trucks)):
                candidateRoute: Route = self.trucks[i]
                if candidateRoute is not None:
                    self.IdentifyBestInsertion(bestInsertion, candidateRoute)

                    if bestInsertion.cost < min_change:
                        min_best_insertion_point = bestInsertion

            if (min_best_insertion_point.customer is not None):
                self.ApplyCustomerInsertion(min_best_insertion_point)
                insertions += 1




            else:
                # If there is an empty available route
                if candidateRoute is not None and len(
                        candidateRoute.sequenceOfNodes) == 1:
                    modelIsFeasible = False
                    break


        if (modelIsFeasible == False):
            print('FeasibilityIssue')
            # reportSolution

        SolDrawer.draw2(i, self.trucks, self.allNodes)

    def LocalSearch(self, operator):
        self.bestSolution = self.cloneSolution()
        terminationCondition = False
        localSearchIterator = 0

        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()

        while terminationCondition is False:

            self.InitializeOperators(rm, sm, top)


            # Relocations
            if operator == 0:
                self.FindBestRelocationMove(rm)
                if rm.originRoutePosition is not None:
                    if rm.moveCost < 0:

                        self.ApplyRelocationMove(rm)
                    else:
                        terminationCondition = True

            # Swaps
            elif operator == 1:
                self.FindBestSwapMove(sm)
                if sm.positionOfFirstRoute is not None:
                    if sm.moveCost < 0:
                        self.ApplySwapMove(sm)
                    else:
                        terminationCondition = True

            elif operator == 2:
                self.FindBestTwoOptMove(top)
                if top.positionOfFirstRoute is not None:
                    if top.moveCost < 0:
                        self.ApplyTwoOptMove(top)
                    else:
                        terminationCondition = True


            if (self.sol.cost < self.bestSolution.cost):
                self.bestSolution = self.cloneSolution()


            localSearchIterator = localSearchIterator + 1

        SolDrawer.draw(localSearchIterator, self.sol, self.allNodes)
        self.sol = self.bestSolution

        print('\n')
        print('Number of iterations where Local Search trapped in local minimum is: ',
              localSearchIterator)
        print('\n')

    def VND(self):
        self.bestSolution = self.cloneSolution()
        VNDIterator = 0
        kmax = 3
        rm = RelocationMove()
        sm = SwapMove()
        top = TwoOptMove()
        neighborhoodTypeDict = {self.FindBestRelocationMove: rm, self.FindBestSwapMove: sm,
                                self.FindBestTwoOptMove: top}

        k = 1
        neighborhoodTypeOrder = [self.FindBestTwoOptMove, self.FindBestSwapMove, self.FindBestRelocationMove]   #allazoume to order kai sygkrinoume apotelesmata
        # neighborhoodTypeOrder = [self.FindBestTwoOptMove, self.FindBestSwapMove, self.FindBestRelocationMove]
        # neighborhoodTypeOrder = [self.FindBestRelocationMove, self.FindBestSwapMove, self.FindBestTwoOptMove]

        while k <= kmax:
            self.InitializeOperators(rm, sm, top)

            moveTypeToApply = neighborhoodTypeOrder[k - 1]
            moveStructure = neighborhoodTypeDict[moveTypeToApply]
            bestNeighbor, moveCost = self.FindBestNeighbor(moveTypeToApply, moveStructure)
            if bestNeighbor is not None and moveCost < 0.0:
                self.ApplyMove(moveStructure)
                k = 1

                if (self.sol.cost < self.bestSolution.cost):
                    self.bestSolution = self.cloneSolution()

                VNDIterator = VNDIterator + 1
            else:
                k = k + 1

        SolDrawer.draw(VNDIterator, self.sol, self.allNodes)

    def FindBestNeighbor(self, moveTypeToApply, moveStructure):
        bestNeighbor = None

        moveTypeToApply(moveStructure)

        if isinstance(moveStructure, RelocationMove):
            bestNeighbor = moveStructure.originRoutePosition

        elif isinstance(moveStructure, SwapMove):
            bestNeighbor = moveStructure.positionOfFirstRoute

        elif isinstance(moveStructure, TwoOptMove):
            bestNeighbor = moveStructure.positionOfFirstRoute

        return bestNeighbor, moveStructure.moveCost

    def ApplyMove(self, moveStructure):

        if isinstance(moveStructure, RelocationMove):
            self.ApplyRelocationMove(moveStructure)
        elif isinstance(moveStructure, SwapMove):
            self.ApplySwapMove(moveStructure)
        elif isinstance(moveStructure, TwoOptMove):
            self.ApplyTwoOptMove(moveStructure)

    def cloneRoute(self, rt: Route):
        cloned = Route(self.depot, self.timecapacity, self.trucks)
        cloned.cost = rt.cost
        cloned.load = rt.load
        cloned.timeload = rt.timeload
        cloned.sequenceOfNodes = rt.sequenceOfNodes.copy()
        cloned.truck = rt.truck
        return cloned

    def cloneSolution(self):
        cloned = Solution()
        for i in range(0, len(self.trucks)):
            rt = self.trucks[i]
            clonedRoute = self.cloneRoute(rt)
            cloned.routes.append(clonedRoute)
        cloned.cost = self.sol.cost
        return cloned

    def FindBestRelocationMove(self, rm):
        for originRouteIndex in range(0, len(self.trucks)):
            rt1: Route = self.trucks[originRouteIndex]
            for targetRouteIndex in range(0, len(self.trucks)):
                rt2: Route = self.trucks[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    for targetNodeIndex in range(0, len(rt2.sequenceOfNodes) - 1):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        A = rt1.sequenceOfNodes[originNodeIndex - 1]
                        B = rt1.sequenceOfNodes[originNodeIndex]
                        C = rt1.sequenceOfNodes[originNodeIndex + 1]

                        F = rt2.sequenceOfNodes[targetNodeIndex]
                        G = rt2.sequenceOfNodes[targetNodeIndex + 1]

                        if rt1 != rt2:
                            timeRt1toRt2 = self.timeMatrix[F.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                           self.timeMatrix[F.ID][G.ID]
                            if rt2.load + B.demand > rt2.truck.weight or (
                                     rt2.timeload + B.service_time + timeRt1toRt2 > 210):
                                continue

                        costAdded = self.distanceMatrix[A.ID][C.ID] + self.distanceMatrix[F.ID][B.ID] + \
                                    self.distanceMatrix[B.ID][G.ID]
                        costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[B.ID][C.ID] + \
                                      self.distanceMatrix[F.ID][G.ID]

                        timeAdded = self.timeMatrix[A.ID][C.ID] + self.timeMatrix[F.ID][B.ID] + self.timeMatrix[B.ID][
                            G.ID]
                        timeRemoved = self.timeMatrix[A.ID][B.ID] + self.timeMatrix[B.ID][C.ID] + self.timeMatrix[F.ID][
                            G.ID]

                        originRtCostChange = self.distanceMatrix[A.ID][C.ID] - self.distanceMatrix[A.ID][B.ID] - \
                                             self.distanceMatrix[B.ID][C.ID]
                        targetRtCostChange = self.distanceMatrix[F.ID][B.ID] + self.distanceMatrix[B.ID][G.ID] - \
                                             self.distanceMatrix[F.ID][G.ID]

                        originRtTimeChange = self.timeMatrix[A.ID][C.ID] - self.timeMatrix[A.ID][B.ID] - \
                                             self.timeMatrix[B.ID][C.ID]
                        targetRtTimeChange = self.timeMatrix[F.ID][B.ID] + self.timeMatrix[B.ID][G.ID] - \
                                             self.timeMatrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved
                        timeCost = timeAdded - timeRemoved

                        if (moveCost < rm.moveCost) and abs(moveCost):
                            self.StoreBestRelocationMove(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                         targetNodeIndex, moveCost, timeCost, originRtCostChange,
                                                         targetRtCostChange, originRtTimeChange, targetRtTimeChange, rm)

        return rm.originRoutePosition

    def FindBestSwapMove(self, sm):
        for firstRouteIndex in range(0, len(self.trucks)):
            rt1: Route = self.trucks[firstRouteIndex]
            for secondRouteIndex in range(firstRouteIndex, len(self.trucks)):
                rt2: Route = self.trucks[secondRouteIndex]
                for firstNodeIndex in range(1, len(rt1.sequenceOfNodes) - 1):
                    if rt1 == rt2:
                        startOfSecondNodeIndex = firstNodeIndex + 1
                    else:
                        startOfSecondNodeIndex = 1
                    for secondNodeIndex in range(startOfSecondNodeIndex, len(rt2.sequenceOfNodes) - 1):

                        a1 = rt1.sequenceOfNodes[firstNodeIndex - 1]
                        b1 = rt1.sequenceOfNodes[firstNodeIndex]
                        c1 = rt1.sequenceOfNodes[firstNodeIndex + 1]

                        a2 = rt2.sequenceOfNodes[secondNodeIndex - 1]
                        b2 = rt2.sequenceOfNodes[secondNodeIndex]
                        c2 = rt2.sequenceOfNodes[secondNodeIndex + 1]

                        moveCost = None
                        costChangeFirstRoute = None
                        costChangeSecondRoute = None

                        if rt1 == rt2:
                            if firstNodeIndex == secondNodeIndex - 1:
                                timeRemoved = self.timeMatrix[a1.ID][b1.ID] + self.timeMatrix[b1.ID][b2.ID] + \
                                              self.timeMatrix[b2.ID][c2.ID]
                                timeAdded = self.timeMatrix[a1.ID][b2.ID] + self.timeMatrix[b2.ID][b1.ID] + \
                                            self.timeMatrix[b1.ID][c2.ID]
                                timeCost = timeAdded - timeRemoved

                                if (rt1.timeload + timeCost > 210) :
                                    continue

                                costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][b2.ID] + \
                                                self.distanceMatrix[b2.ID][c2.ID]
                                costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][b1.ID] + \
                                                self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded - costRemoved

                            else:
                                timeRemoved = self.timeMatrix[a1.ID][b1.ID] + self.timeMatrix[b1.ID][c1.ID] + \
                                               (self.timeMatrix[a2.ID][b2.ID] + self.timeMatrix[b2.ID][c2.ID])

                                timeAdded = self.timeMatrix[a1.ID][b2.ID] + self.timeMatrix[b2.ID][c1.ID] + \
                                               (self.timeMatrix[a2.ID][b1.ID] + self.timeMatrix[b1.ID][c2.ID])
                                timeCost = timeAdded - timeRemoved

                                if (rt1.timeload + timeCost > 210) :
                                    continue

                                costRemoved = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID] \
                                              + self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]

                                costAdded = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID] \
                                            + self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]
                                moveCost = costAdded - costRemoved

                        else:
                            timeRemoved1 = self.timeMatrix[a1.ID][b1.ID] + self.timeMatrix[b1.ID][c1.ID]
                            timeAdded1 = self.timeMatrix[a1.ID][b2.ID] + self.timeMatrix[b2.ID][c1.ID]
                            timeRemoved2 = self.timeMatrix[a2.ID][b2.ID] + self.timeMatrix[b2.ID][c2.ID]
                            timeAdded2 = self.timeMatrix[a2.ID][b1.ID] + self.timeMatrix[b1.ID][c2.ID]

                            timeCost = timeAdded1 + timeAdded2 - (timeRemoved1 + timeRemoved2)

                            if rt1.timeload + timeCost > 210 :
                                continue
                            if rt2.timeload + timeCost > 210 :
                                continue

                            if rt1.load - b1.demand + b2.demand > rt1.truck.weight:
                                continue
                            if rt2.load - b2.demand + b1.demand > rt2.truck.weight:
                                continue

                            costRemoved1 = self.distanceMatrix[a1.ID][b1.ID] + self.distanceMatrix[b1.ID][c1.ID]
                            costAdded1 = self.distanceMatrix[a1.ID][b2.ID] + self.distanceMatrix[b2.ID][c1.ID]
                            costRemoved2 = self.distanceMatrix[a2.ID][b2.ID] + self.distanceMatrix[b2.ID][c2.ID]
                            costAdded2 = self.distanceMatrix[a2.ID][b1.ID] + self.distanceMatrix[b1.ID][c2.ID]

                            costChangeFirstRoute = costAdded1 - costRemoved1
                            costChangeSecondRoute = costAdded2 - costRemoved2

                            timeChangeFirstRoute = timeAdded1 - timeRemoved1
                            timeChangeSecondRoute = timeAdded2 - timeRemoved2

                            moveCost = costAdded1 + costAdded2 - (costRemoved1 + costRemoved2)

                        if moveCost < sm.moveCost and abs(moveCost):
                            if ( rt1 == rt2):
                                self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex,
                                                       secondNodeIndex,
                                                       moveCost, timeCost, costChangeFirstRoute, costChangeSecondRoute,
                                                       timeAdded, timeRemoved,sm)
                            else:
                                self.StoreBestSwapMove(firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                                                   moveCost, timeCost, costChangeFirstRoute, costChangeSecondRoute,timeChangeFirstRoute, timeChangeSecondRoute,sm)

    def FindBestTwoOptMove(self, top):
        for rtInd1 in range(0, len(self.trucks)):
            rt1: Route = self.trucks[rtInd1]
            for rtInd2 in range(rtInd1, len(self.trucks)):
                rt2: Route = self.trucks[rtInd2]
                for nodeInd1 in range(0, len(rt1.sequenceOfNodes) - 1):
                    start2 = 0
                    if (rt1 == rt2):
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.sequenceOfNodes) - 1):
                        moveCost = 10 ** 9

                        A = rt1.sequenceOfNodes[nodeInd1]
                        B = rt1.sequenceOfNodes[nodeInd1 + 1]
                        K = rt2.sequenceOfNodes[nodeInd2]
                        L = rt2.sequenceOfNodes[nodeInd2 + 1]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.sequenceOfNodes) - 2:
                                continue
                            costAdded = self.distanceMatrix[A.ID][K.ID] + self.distanceMatrix[B.ID][L.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.sequenceOfNodes) - 1 and nodeInd2 == len(rt2.sequenceOfNodes) - 1:
                                continue

                            if self.CapacityIsViolated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            costAdded = self.distanceMatrix[A.ID][L.ID] + self.distanceMatrix[B.ID][K.ID]
                            costRemoved = self.distanceMatrix[A.ID][B.ID] + self.distanceMatrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        if moveCost < top.moveCost and abs(moveCost):
                            self.StoreBestTwoOptMove(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top)

    def ApplyRelocationMove(self, rm: RelocationMove):

        oldCost = self.CalculateTotalCost(self.sol)

        originRt = self.trucks[rm.originRoutePosition]
        targetRt = self.trucks[rm.targetRoutePosition]

        B = originRt.sequenceOfNodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            if (rm.originNodePosition < rm.targetNodePosition):
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)

            originRt.cost += rm.moveCost
            originRt.timeload += rm.timeCost
        else:
            del originRt.sequenceOfNodes[rm.originNodePosition]
            targetRt.sequenceOfNodes.insert(rm.targetNodePosition + 1, B)
            originRt.cost += rm.costChangeOriginRt
            targetRt.cost += rm.costChangeTargetRt
            originRt.load -= B.demand
            targetRt.load += B.demand

        self.sol.cost += rm.moveCost

        newCost = self.CalculateTotalCost(self.sol)
        # debuggingOnly
        if abs((newCost - oldCost) - rm.moveCost) > 100.0001:
            print('Cost Issue')

    def ApplySwapMove(self, sm):
        oldCost = self.CalculateTotalCost(self.sol)
        rt1 = self.trucks[sm.positionOfFirstRoute]
        rt2 = self.trucks[sm.positionOfSecondRoute]
        b1 = rt1.sequenceOfNodes[sm.positionOfFirstNode]
        b2 = rt2.sequenceOfNodes[sm.positionOfSecondNode]
        rt1.sequenceOfNodes[sm.positionOfFirstNode] = b2
        rt2.sequenceOfNodes[sm.positionOfSecondNode] = b1

        if (rt1 == rt2):
            rt1.cost += sm.moveCost
            rt1.timeload += sm.timeCost
        else:
            rt1.cost += sm.costChangeFirstRt
            rt2.cost += sm.costChangeSecondRt
            rt1.load = rt1.load - b1.demand + b2.demand
            rt2.load = rt2.load + b1.demand - b2.demand
            rt1.timeload += sm.timeChangeFirstRoute
            rt2.timeload += sm.timeChangeSecondRoute


        self.sol.cost += sm.moveCost

        newCost = self.CalculateTotalCost(self.sol)

    def ApplyTwoOptMove(self, top):
        rt1: Route = self.trucks[top.positionOfFirstRoute]
        rt2: Route = self.trucks[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            rt1.sequenceOfNodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment

            rt1.cost += top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            del rt1.sequenceOfNodes[top.positionOfFirstNode + 1:]
            del rt2.sequenceOfNodes[top.positionOfSecondNode + 1:]

            rt1.sequenceOfNodes.extend(relocatedSegmentOfRt2)
            rt2.sequenceOfNodes.extend(relocatedSegmentOfRt1)

            self.UpdateRouteCostAndLoad(rt1)
            self.UpdateRouteCostAndLoad(rt2)

        self.sol.cost += top.moveCost

    def ReportSolution(self):
        cost = 0
        count = 0
        for i in range(0, len(self.trucks)):
            rt = self.trucks[i]

            if rt.load > 0:
                count += 1

            print('Truckid:', rt.truck.id, end=' => ')
            print('Load:', rt.load, end=' || ')
            print('Timeload:', round(rt.timeload, 3), end=' || ')
            print('Sequence of nodes: ', end=' ')
            for j in rt.sequenceOfNodes:
                print(j.ID, end=' ')
            print("\n")

            cost += rt.cost

        print('The number of routes used is: ', count)
        print('Total cost of local optimum is: ', round(cost, 3), end = '\n')
        print('=====================================================================================================================', end = '\n')

    def IdentifyBestInsertion(self, bestInsertion, rt):
        for i in range(0, len(self.customers)):
            candidateCust: Node = self.customers[i]
            if candidateCust.isRouted is False:
                lastNodePresentInTheRoute = rt.sequenceOfNodes[-1]
                timeCheck = self.timeMatrix[lastNodePresentInTheRoute.ID][candidateCust.ID]
                if (
                        rt.load + candidateCust.demand <= rt.truck.weight and rt.timeload + candidateCust.service_time + timeCheck <= 210):  # svisame + 15 TASSOZZ

                    trialCost = self.distanceMatrix[lastNodePresentInTheRoute.ID][candidateCust.ID]

                    if trialCost < bestInsertion.cost:
                        bestInsertion.customer = candidateCust
                        bestInsertion.route = rt
                        bestInsertion.cost = trialCost

    def ApplyCustomerInsertion(self, insertion):
        insCustomer = insertion.customer
        rt = insertion.route

        # before the second depot occurrence
        insIndex = len(rt.sequenceOfNodes)
        rt.sequenceOfNodes.insert(insIndex, insCustomer)

        beforeInserted = rt.sequenceOfNodes[-2]

        costAdded = self.distanceMatrix[beforeInserted.ID][insCustomer.ID]
        timeAdded = self.timeMatrix[beforeInserted.ID][insCustomer.ID]

        rt.cost += costAdded

        self.sol.cost += costAdded

        rt.load += insCustomer.demand
        rt.timeload += insCustomer.service_time + timeAdded

        insCustomer.isRouted = True


    def StoreBestRelocationMove(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex, moveCost,
                                timeCost,
                                originRtCostChange, targetRtCostChange, originRtTimeChange, targetRtTimeChange,
                                rm: RelocationMove):
        rm.originRoutePosition = originRouteIndex
        rm.originNodePosition = originNodeIndex
        rm.targetRoutePosition = targetRouteIndex
        rm.targetNodePosition = targetNodeIndex

        rm.costChangeOriginRt = originRtCostChange
        rm.costChangeTargetRt = targetRtCostChange

        rm.timeChangeOriginRt = originRtTimeChange
        rm.timeChangeTargetRt = targetRtTimeChange

        rm.moveCost = moveCost
        rm.timeCost = timeCost

    def StoreBestSwapMove(self,firstRouteIndex, secondRouteIndex, firstNodeIndex, secondNodeIndex,
                         moveCost, timeCost, costChangeFirstRoute, costChangeSecondRoute,timeChangeFirstRoute, timeChangeSecondRoute,
                         sm):
        sm.positionOfFirstRoute = firstRouteIndex
        sm.positionOfSecondRoute = secondRouteIndex
        sm.positionOfFirstNode = firstNodeIndex
        sm.positionOfSecondNode = secondNodeIndex
        sm.costChangeFirstRt = costChangeFirstRoute
        sm.costChangeSecondRt = costChangeSecondRoute
        sm.moveCost = moveCost
        sm.timeCost = timeCost
        sm.timeChangeFirstRoute = timeChangeFirstRoute
        sm.timeChangeSecondRoute = timeChangeSecondRoute

    def StoreBestTwoOptMove(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost, top):
        top.positionOfFirstRoute = rtInd1
        top.positionOfSecondRoute = rtInd2
        top.positionOfFirstNode = nodeInd1
        top.positionOfSecondNode = nodeInd2
        top.moveCost = moveCost

    def CalculateTotalCost(self, sol):

        c = 0
        for i in range(0, len(sol.routes)):
            rt = sol.routes[i]
            for j in range(0, len(rt.sequenceOfNodes) - 1):
                a = rt.sequenceOfNodes[j]
                b = rt.sequenceOfNodes[j + 1]
                c += self.distanceMatrix[a.ID][b.ID]
        return c

    def InitializeOperators(self, rm, sm, top):
        rm.Initialize()
        sm.Initialize()
        top.Initialize()

    def CapacityIsViolated(self, rt1, nodeInd1, rt2, nodeInd2):

        rt1FirstSegmentLoad = 0
        rt1FirstSegmentTimeload = 0
        for i in range(0, nodeInd1 + 1):
            n1 = rt1.sequenceOfNodes[i]
            m1 = rt1.sequenceOfNodes[i+1]
            rt1FirstSegmentLoad += n1.demand
            if i != nodeInd1:
                rt1FirstSegmentTimeload += n1.service_time + self.timeMatrix[n1.ID][m1.ID]
            else:
                rt1FirstSegmentTimeload += n1.service_time

        rt1SecondSegmentLoad = rt1.load - rt1FirstSegmentLoad
        rt1SecondSegmentTimeload = rt1.timeload - rt1FirstSegmentTimeload

        rt2FirstSegmentLoad = 0
        rt2FirstSegmentTimeload = 0
        for i in range(0, nodeInd2 + 1):
            n2 = rt2.sequenceOfNodes[i]
            m2 = rt2.sequenceOfNodes[i+1]
            rt2FirstSegmentLoad += n2.demand
            if i == nodeInd2:
                rt2FirstSegmentTimeload += n2.service_time
            else:
                rt2FirstSegmentTimeload += n2.service_time + self.timeMatrix[n2.ID][m2.ID]

        rt2SecondSegmentLoad = rt2.load - rt2FirstSegmentLoad
        rt2SecondSegmentTimeload = rt2.timeload - rt2FirstSegmentTimeload

        A1 = rt1.sequenceOfNodes[nodeInd1]
        B1 = rt1.sequenceOfNodes[nodeInd1 + 1]
        A2 = rt2.sequenceOfNodes[nodeInd2]
        B2 = rt2.sequenceOfNodes[nodeInd2 - 1]

        if (
                rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.truck.weight or rt1FirstSegmentTimeload + rt2SecondSegmentTimeload +
                self.timeMatrix[A1.ID][A2.ID] > 210):
            return True

        if (
                rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.truck.weight or rt2FirstSegmentTimeload + rt1SecondSegmentTimeload +
                self.timeMatrix[B2.ID][B1.ID] > 210):
            return True

        return False

    def UpdateRouteCostAndLoad(self, rt: Route):
        tc = 0
        tl = 0
        total_timeload = 0

        for i in range(0, len(rt.sequenceOfNodes) - 1):
            A = rt.sequenceOfNodes[i]
            B = rt.sequenceOfNodes[i + 1]
            tc += self.distanceMatrix[A.ID][B.ID]
            tl += A.demand

            total_timeload += A.service_time + self.timeMatrix[A.ID][B.ID]

        rt.load = tl
        rt.cost = tc

        rt.timeload = total_timeload

    def TestSolution(self):
        totalSolCost = 0
        for r in range(0, len(self.trucks)):
            rt: Route = self.trucks[r]
            rtCost = 0
            rtLoad = 0
            for n in range(0, len(rt.sequenceOfNodes) - 1):
                A = rt.sequenceOfNodes[n]
                B = rt.sequenceOfNodes[n + 1]
                rtCost += self.distanceMatrix[A.ID][B.ID]
                rtLoad += A.demand
            if abs(rtCost - rt.cost) > 0.0001:
                print('Route Cost problem')
            if rtLoad != rt.load:
                print('Route Load problem')

            totalSolCost += rt.cost

        if abs(totalSolCost - self.sol.cost) > 0.0001:
            print('Solution Cost problem')

