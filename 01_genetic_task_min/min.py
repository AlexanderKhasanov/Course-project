import random

BEG = -10
END = 100


def replace_at_index(tup, ix, val):

    lst = list(tup)
    lst[ix] = val
    return tuple(lst)


def sort(fun, coordinate):

    srt = sorted(zip(fun, coordinate), key=lambda x: x[1])
    return zip(*srt)


def mutation(exemplar):

    index_change = random.randrange(0, len(exemplar))
    x = exemplar[index_change] + random.uniform(0, 10) - 5
    if x < BEG:
        x = BEG
    if x > END:
        x = END

    new_exemplar = replace_at_index(exemplar, index_change, x)
    return new_exemplar


def evolution(parents, best_parents, best_mutation, good_parents, good_mutation):

    new_generation = []
    for p in parents:
        new_generation.append(p)

    for p in new_generation[:best_parents]:
        for _ in range(best_mutation):
            new_generation.append(mutation(p))

    for p in new_generation[best_mutation:(best_parents + good_parents)]:
        for _ in range(good_mutation):
            new_generation.append(mutation(p))
    return new_generation


def init_generation(count, fn, number_var):

    generation = []
    fun = []
    for i in range(count):
        coordinates = ()
        for j in range(number_var):
            coordinates += (random.uniform(BEG, END),)
        generation.append(coordinates)
        fun.append(fn(coordinates))

    return fun, generation


def genetic(fn, number_var=2, first_generation=20,
            max_iteration=200, best_parents=5, best_mutation=2, good_parents=5, good_mutation=1,
            eps=None, best_iteration=10,
            verbose=False):
    """

    :param fn: минимизируемая функция
    :param number_var: количество переменных в функции fn. надо избавиться от этой переменной
    :param first_generation: количество экземпляров в первой итерации
    :param max_iteration: максимальное количествао итераций
    :param best_parents: количество лучших предков
    :param best_mutation: количество мутанков лучших предков
    :param good_parents: количество хороших предков
    :param good_mutation: количество мутанков хороших предков
    :param best_iteration: количество итераций, необходимое чтобы завершился алгоритм, если ошибка меньше eps
    :param eps: приемлемая ошибка
    :param verbose: логгирование
    :return: возвращает найденный минимум, координаты минимума, количество пройденных итераций
    """

    values, generation = init_generation(count=first_generation, fn=fn, number_var=number_var)
    values, generation = sort(values, generation)

    glob_min = values[0]
    dot_min = generation[0]

    count_less_esp = 0
    for iteration in range(max_iteration):
        generation = evolution(generation, best_parents, best_mutation, good_parents, good_mutation)
        values = [fn(gen) for gen in generation]
        values, generation = sort(values, generation)

        if eps and abs(glob_min - values[0]) < eps:
            glob_min = values[0]
            dot_min = generation[0]
            count_less_esp += 1
        else:
            count_less_esp = 0

        if count_less_esp > best_iteration:
            break

        if values[0] < glob_min:
            glob_min = values[0]
            dot_min = generation[0]

        if verbose:
            print(glob_min, dot_min)

    return glob_min, dot_min, iteration + 1


if __name__ == "__main__":
    def target(x):
        return x[0] + x[1]

    print(genetic(fn=target, verbose=True, eps=None, first_generation=10, best_iteration=10))
