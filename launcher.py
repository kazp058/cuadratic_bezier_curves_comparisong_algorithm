from src.models import *
import random


def pop_takerandom(clusters):
    idx = random.randint(0, len(clusters) - 1)
    return clusters.pop(idx)


def trymerge(merged, cluster):
    __mcounter = 0
    __selected_merged = False
    while __mcounter < len(merged) and not __selected_merged:
        __m = merged[__mcounter]
        if __m.stable_cluster(cluster):
            __m.add_cluster(cluster)
            __selected_merged = True
        __mcounter += 1
    if not __selected_merged:
        merged.append(cluster)


def merge_clusters(__clusters):
    merged = []
    while len(__clusters) > 0:
        if len(merged) == 0:
            selected = pop_takerandom(__clusters)
            merged.append(selected)
        else:
            selected = pop_takerandom(__clusters)
            trymerge(merged, selected)

    return merged


def sort_curves(clusters):
    if len(clusters) <= 1:
        return clusters

    mid = len(clusters) // 2
    left = clusters[: mid]
    right = clusters[mid:]

    sorted_left = sort_curves(left)
    sorted_right = sort_curves(right)

    return merge_clusters(sorted_left + sorted_right)


def make_curves(__amount):
    return [Curve.make_random(n) for n in range(1, __amount + 1)]


N = 200

similarity_requiered = 70
Cluster.acceptance = 75
assert similarity_requiered <= Cluster.acceptance

__curves: [Curve] = make_curves(N)
__clusters = [Cluster(__curves[__idcurve], __idcurve)
              for __idcurve in range(len(__curves))]

solution = sort_curves(__clusters)
similarities = []
for __idx in range(len(solution)):
    __pointer_x = solution[__idx]
    similarities += __pointer_x.get_similarity_table()
    for __idy in range(__idx + 1, len(solution)):
        __pointer_y = solution[__idy]
        similarities += __pointer_x.get_similarity_table(__pointer_y)
print("\ntotal clusters:      ", len(solution))

similar = list(filter(lambda x: float(
    x.split(",")[2]) >= similarity_requiered, similarities))
unsimilar = list(filter(lambda x: float(
    x.split(",")[2]) < similarity_requiered, similarities))

print("amount of curves:     ", N)
print("total similarities:   ", len(similar))
print("total unsimilarities: ", len(unsimilar))
print("_______________________")
expected = 0
for n in range(1, N):
    expected = expected + n

print("total output:          %i/%i" % (len(similarities), expected))
