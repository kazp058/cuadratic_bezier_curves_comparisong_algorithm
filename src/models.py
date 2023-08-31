from functools import reduce
import math
import random


class Point:

    def __init__(self, x: float = None, y: float = None) -> None:
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return "(%f,%f)" % (float(self.x), float(self.y))

    def make_random(point: object = None) -> object:
        __y = None
        __x = None

        if point == None:
            __x = random.randrange(-100, 100)
            __y = random.randrange(-100, 100)
            return Point(__x, __y)

        __x = random.randrange(point.x, 100)

        if __x == point.x:
            while __y == None or __y == point.y:
                __y = random.randrange(-100, 100)
        else:
            __y = random.randrange(-100, 100)

        return Point(__x, __y)

    def from_string(__str: str) -> object:
        __cache = __str.strip().replace(")", "").replace("(", "").split(",")
        return Point(float(__cache[0]), float(__cache[1]))

    def get_distance_points(point_a, point_b) -> float:
        return math.sqrt(
            pow(point_b.x - point_a.x, 2)
            +
            pow(point_b.y - point_a.y, 2)
        )

    def get_midpoint(point_a, point_b):
        return Point((point_a.x + point_b.x) / 2, (point_a.y + point_b.y) / 2)


class Curve:

    def __init__(self, id: int = None,
                 point_a: Point = None,
                 point_b: Point = None,
                 point_c: Point = None,
                 t: float = None) -> None:
        self.id = id
        self.point_a = point_a
        self.point_b = point_b
        self.point_c = point_c
        self.t = t

    def __str__(self) -> str:
        return "%i>%s;%s;%s;%f" % (int(self.id),
                                   str(self.point_a),
                                   str(self.point_b),
                                   str(self.point_c),
                                   float(self.t))

    def copy(curve):
        __curve = Curve()
        __curve.id = curve.id
        __curve.point_a = curve.point_a
        __curve.point_b = curve.point_b
        __curve.point_c = curve.point_c
        __curve.t = curve.t
        return __curve

    def make_random(__id: int, __target_curve=None) -> object:
        __curve = Curve()
        __curve.id = __id
        if __target_curve == None:
            __curve.point_a = Point.make_random()
            __curve.point_b = Point.make_random(__curve.point_a)
            __curve.point_c = Point.make_random(__curve.point_b)
        else:
            __curve.point_a = Point.make_random(__target_curve.point_a)
            __curve.point_b = Point.make_random(__target_curve.point_b)
            __curve.point_c = Point.make_random(__target_curve.point_c)
        __curve.t = random.random()
        return __curve

    def from_string(__str: str) -> object:
        __curve = Curve()
        __id, __str = __str.strip().split(">")
        __curve.id = int(__id)

        __point_a, __point_b, __point_c, __t = __str.split(";")
        __curve.point_a = Point.from_string(__point_a)
        __curve.point_b = Point.from_string(__point_b)
        __curve.point_c = Point.from_string(__point_c)
        __curve.t = float(__t)

        return __curve

    def modify_avg(self, curve_b):
        self.point_a = Point.get_midpoint(self.point_a, curve_b.point_a)
        self.point_b = Point.get_midpoint(self.point_b, curve_b.point_b)
        self.point_c = Point.get_midpoint(self.point_c, curve_b.point_c)
        self.t = (self.t + curve_b.t) / 2

        return self

    def similarity(self, curve_b, scalingVector=(Point(-100, -100), Point(100, 100))) -> float:
        distances = [self.point_a.get_distance_points(curve_b.point_a),
                     self.point_b.get_distance_points(curve_b.point_b),
                     self.point_c.get_distance_points(curve_b.point_c)]
        normalized_distances = list(map(
            lambda x: x / scalingVector[0].get_distance_points(scalingVector[1]), distances))

        return 100 * (1 -
                      reduce(lambda x, y: x + y, normalized_distances) /
                      (len(distances) + 1)
                      - abs(self.t - curve_b.t) /
                      (len(distances) + 1)
                      )


class Cluster:

    acceptance = 60

    def __init__(self, curve: Curve, id: int = 0) -> None:
        self.centroid = Curve.copy(curve)
        self.id = id
        self.curves = [curve]

    def add_cluster(self, __cluster: any):
        self.centroid.modify_avg(__cluster.centroid)
        self.curves = self.curves + __cluster.curves

    def get_similarity_table(self, cluster_b: any = None):
        sim_table = []
        if cluster_b != None:
            __sim = self.centroid.similarity(cluster_b.centroid)
            for __cidx in range(len(self.curves)):
                __cx = self.curves[__cidx]
                for __cidy in range(len(cluster_b.curves)):
                    __cy = cluster_b.curves[__cidy]
                    sim_table.append("%i,%i,%.4f" % (__cx.id, __cy.id, __sim))
        else:
            avg = self.avg_similarity()
            for __cidx in range(len(self.curves)):
                __cx = self.curves[__cidx]
                for __cidy in range(__cidx + 1, len(self.curves)):
                    __cy = self.curves[__cidy]
                    sim_table.append("%i,%i,%.4f" % (__cx.id, __cy.id, avg))

        return sim_table

    def avg_similarity(self):
        return reduce(
            lambda y, z: y + z,
            map(lambda x: self.centroid.similarity(x), self.curves)
        ) / len(self.curves)

    def copy(self):
        __cluster = Cluster(self.centroid)
        __cluster.id = self.id
        __cluster.curves = self.curves.copy()
        return __cluster

    def stable_cluster(self, cluster: any = None):
        __tcluster = self
        if cluster != None:
            __tcluster = self.copy()
            __tcluster.add_cluster(cluster)

        __sims = list(
            map(lambda curve: __tcluster.centroid.similarity(curve) >= Cluster.acceptance,
                __tcluster.curves))
        return reduce(lambda x, y: x and y, __sims)

    def __str__(self) -> str:
        return ("id: %i > clustere: [%s] \ncurvas: \n(\n\t") % (self.id, self.centroid) + ",\n\t".join(list(map(lambda x: str(x), self.curves))) + "\n)"
