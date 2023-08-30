```
def trymerge(merged, cluster):
    counter = 0
    target_merged = False
    while counter < merged.size and not target_merged:
        if merged[counter] is stable_cluster(cluster):
            merged[counter].add_cluster(cluster)
            target_merged = True
        increase counter by 1
    if target_merged is false:
        merged.append(cluster)


def merge_clusters(clusters):
    merged = []
    while clusters.size greater than 0:
        if merged.size is 0:
            selected = pop_takerandom(clusters) #pop a cluster from clusters
            merged.append(selected)
        else:
            selected = pop_takerandom(clusters) #pop a cluster from clusters
            trymerge(merged, selected)

    return merged

def sort_curves(clusters):
    if clusters.size less or equal than 1:
        return clusters

    mid = clusters.size // 2
    left = clusters[: mid]
    right = clusters[mid + 1:]

    sorted_left = sort_curves(left)
    sorted_right = sort_curves(right)

    return merge_clusters(sorted_left + sorted_right)

```
