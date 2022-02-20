import matplotlib.pyplot as plt

class SolDrawer:
    @staticmethod
    def get_cmap(n, name='hsv'):
        return plt.cm.get_cmap(name, n)

    @staticmethod
    def draw(itr, sol, nodes):
        plt.clf()
        plt.style.use('ggplot')
        SolDrawer.drawPoints(nodes)
        SolDrawer.drawRoutes(sol)
        plt.savefig(str(itr))

    @staticmethod
    def drawPoints(nodes:list):
        x = []
        y = []
        for i in range(len(nodes)):
            n = nodes[i]
            x.append(n.xx)
            y.append(n.yy)
        plt.scatter(x, y, c="blue")

    @staticmethod
    def drawRoutes(sol):
        cmap = SolDrawer.get_cmap(len(sol.routes))
        plt.title('VND')
        if sol is not None:
            for r in range(0, len(sol.routes)):
                rt = sol.routes[r]
                for i in range(0, len(rt.sequenceOfNodes) - 1):
                    c0 = rt.sequenceOfNodes[i]
                    c1 = rt.sequenceOfNodes[i + 1]
                    plt.plot([c0.xx, c1.xx], [c0.yy, c1.yy], c=cmap(r))

    def draw2(itr, sol, nodes):
        plt.clf()
        plt.style.use('ggplot')
        SolDrawer.drawPoints(nodes)
        SolDrawer.drawRoutes2(sol)
        plt.savefig(str(itr))

    def drawRoutes2(sol):
        cmap = SolDrawer.get_cmap(len(sol))
        plt.title('Nearest Neighbor')
        if sol is not None:
            for r in range(0, len(sol)):
                rt = sol[r]
                for i in range(0, len(rt.sequenceOfNodes) - 1):
                    c0 = rt.sequenceOfNodes[i]
                    c1 = rt.sequenceOfNodes[i + 1]
                    plt.plot([c0.xx, c1.xx], [c0.yy, c1.yy], c=cmap(r))

