from src.modules import *
from src.models import *
import random
import time
import plotly.express as px
import pandas as pd


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


def make_rcurves(__amount):
    print(Log("Generating %i random curves" % __amount))
    return [Curve.make_random(n) for n in range(1, __amount + 1)]


def invoke_curves(*args):
    N = args[0]
    frm = FileReaderManager()
    frm.include_fimport("curves.csv", Curve.from_string)
    __curves = frm.fgather()
    print(Log("Trying to load curves"))
    if __curves == None:
        print(Log("Unable to load curves, file does not exist or is empty" % N))
        __curves = make_rcurves(N)
        fwm = FileWriterManager()
        fwm.include_fexport("curves.csv", __curves)
        fwm.fflush()
    elif len(__curves) != N:
        print(Log("Loaded %i curves from files, but required %i" %
              (len(__curves, N))))
        if len(__curves) > N:
            print(Log("Sliced %i curves from array" % (len(__curves) - N)))
            __curves = __curves[:N]
        if len(__curves) < N:
            __curves = __curves + make_rcurves(N - len(__curves))
        fwm = FileWriterManager()
        fwm.include_fexport("curves.csv", __curves)
        fwm.fflush()
    else:
        print(Log("Loaded %i curves successfully from file" % N))
    return __curves


def generate_tsimilarities(solution):
    similarities = []
    for __idx in range(len(solution)):
        __pointer_x = solution[__idx]
        similarities += __pointer_x.get_similarity_table()
        for __idy in range(__idx + 1, len(solution)):
            __pointer_y = solution[__idy]
            similarities += __pointer_x.get_similarity_table(__pointer_y)
    return similarities


def call_algorithm(*args):
    if len(args) == 1:
        args = args[0]
    __curves, func_algth = args

    __clusters = [Cluster(__curves[__idcurve], __idcurve)
                  for __idcurve in range(len(__curves))]

    start_time = time.time()
    solution = func_algth(__clusters)
    exec_time = time.time() - start_time
    print(Log("total execution time: %.5f seconds" % (exec_time)))
    print(Log("total clusters: %i" % len(solution)))

    similarities = generate_tsimilarities(solution)

    similar = list(filter(lambda x: float(
        x.split(",")[2]) >= similarity_requiered, similarities))

    unsimilar = list(filter(lambda x: float(
        x.split(",")[2]) < similarity_requiered, similarities))

    fwm = FileWriterManager()
    fwm.include_fexport("similar.csv", similar)
    fwm.include_fexport("unsimilar.csv", unsimilar)
    fwm.fflush()

    print(Log("total similarities: %i" % len(similar)))
    print(Log("total unsimilarities: %i" % len(unsimilar)))
    print(Log("total output: %i" % len(similarities)))

    return exec_time


def change_parameters(*args):
    pass


def stress_algorithm(*args):
    data = []
    start, end, steps, times = args[0]

    for __amount in range(start, end + steps, steps):
        __times = []
        for _r in range(times):
            __curves = make_rcurves(__amount)
            __args = ((__curves, sort_curves),)
            __times.append(call_algorithm(__curves, sort_curves))
        __avg_time = reduce(lambda x, y: x+y, __times) / len(__times)
        data.append([__amount, __avg_time])
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns=['Number of curves', 'Execution time'])
    fig = px.line(df, x="Number of curves", y="Execution time")
    print(df)
    fig.show()


def close(*args):
    sys.exit(0)


if __name__ == "__main__":
    N = 200
    similarity_requiered = 70
    Cluster.acceptance = 70

    __curves = invoke_curves(N)

    assert similarity_requiered <= Cluster.acceptance
    main_menu = Menu(self_call=True,
                     linejump_before=1,
                     ask_option_str="Select an option")

    main_menu.add_option("Call algorithm", call_algorithm,
                         __curves, sort_curves)
    main_menu.add_option("Stress algorithm",
                         stress_algorithm, 10, 5000, 10, 5)
    main_menu.add_option("Make new curves", invoke_curves, N)
    main_menu.add_option("Change parameters", change_parameters)
    main_menu.add_option("Close program", close)

    main_menu.launch()
