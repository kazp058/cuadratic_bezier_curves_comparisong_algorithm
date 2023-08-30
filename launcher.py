from src.models import *
import random


def pop_takerandom(left, right):
    joint = left + right
    selected = random.choice(joint)
    idx = joint.index(selected)

    if idx < len(left):
        left.pop(idx)
    else:
        idx = idx - len(left)
        right.pop(idx)
    return selected


def trymerge(merged, centroid):
    __mcounter = 0
    __selected_merged = False
    while __mcounter < len(merged) and not __selected_merged:
        __m = merged[__mcounter]
        if __m.stable_centroid(centroid):
            __m.add_centroid(centroid)
            __selected_merged = True
        __mcounter += 1
    if not __selected_merged:
        merged.append(centroid)


def merge_centroids(__left, __right):
    merged = []
    while len(__left) > 0 and len(__right) > 0:
        if len(merged) == 0:
            selected = pop_takerandom(__left, __right)
            merged.append(selected)
        else:
            selected = pop_takerandom(__left, __right)
            trymerge(merged, selected)
    while len(__left) > 0:
        selected = __left.pop(0)
        trymerge(merged, selected)

    while len(__right) > 0:
        selected = __right.pop(0)
        trymerge(merged, selected)

    return merged


def sort_curves(centroids):
    if len(centroids) <= 1:
        return centroids

    mid = len(centroids) // 2
    left = centroids[: mid]
    right = centroids[mid:]
    sorted_left = sort_curves(left)
    sorted_right = sort_curves(right)

    return merge_centroids(sorted_left, sorted_right)


def make_curves(__amount):
    return [Curve.make_random(n) for n in range(1, __amount + 1)]


N = 4

acceptance = 60
Centroid.acceptance = 70

__curves: [Curve] = make_curves(N)
__centroids = [Centroid(__curves[__idcurve], __idcurve)
               for __idcurve in range(len(__curves))]

solution = sort_curves(__centroids)
similarities = []
for __idx in range(len(solution)):
    __pointer_x = solution[__idx]
    similarities += __pointer_x.get_similarity_table()
    for __idy in range(__idx + 1, len(solution)):
        __pointer_y = solution[__idy]
        similarities += __pointer_x.get_similarity_table(__pointer_y)
print("total centroids:      ", len(solution))

similar = list(filter(lambda x: float(
    x.split(",")[2]) >= acceptance, similarities))
unsimilar = list(filter(lambda x: float(
    x.split(",")[2]) < acceptance, similarities))

print("amount of curves:     ", N)
print("total similarities:   ", len(similar))
print("total unsimilarities: ", len(unsimilar))
print("_________________________________________")
expected = 0
for n in range(1, N):
    expected = expected + n

print("total output:          %i/%i" % (len(similarities), expected))
