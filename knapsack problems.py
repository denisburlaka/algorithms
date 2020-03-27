import random

# Количество особей в популяции
n = 300
# Количество популяций
m = 50
# Вместимость рюкзака
capacity = 200

r = random.Random()
r.seed(1)  # Чтобы сгенерированные "вещи" были постоянными

# Количество различных вещей
count_items = 50

items = [i for i in range(count_items)]
items_prices = [r.randint(1, 100) for _ in range(count_items)]
items_weights = [r.randint(1, 100) for _ in range(count_items)]


def calculate_weight(x):
    weight = 0
    for i in range(count_items):
        if x[i] == 1:
            weight += items_weights[i]
    return weight


def init():
    p = []
    for _ in range(n):
        x = [random.randint(0, 1) for _ in range(count_items)]
        p.append(x)
    return p


def f(x):
    if calculate_weight(x) > capacity:
        return 0
    f = 0
    for i in range(count_items):
        if x[i] == 1:
            f += items_prices[i]
    return f


def selection(p):
    p.sort(key=lambda x: (-f(x), calculate_weight(x)))
    return p[:int(n * 0.5)]


def recombination(p):
    new_p = []
    new_p.extend(p)
    while len(new_p) < n:
        x = p[random.randint(0, len(p) - 1)]
        y = p[random.randint(0, len(p) - 1)]
        d = random.randint(0, count_items - 1)
        new_p.append(x[:d] + y[d:])
    return new_p


def mutation(p):
    mut = 0.4
    for _ in range(int(len(p) * mut)):
        a = p[random.randint(0, len(p) - 1)]
        for _ in range(1):
            x = random.randint(0, count_items - 1)
            a[x] = abs(a[x] - 1)


p = init()
for _ in range(m):
    p = recombination(p)
    mutation(p)
    p = selection(p)
    print(p[0], calculate_weight(p[0]), f(p[0]))

'''
# Проверка решения генетического алгоритма, с помощью точного подсчета
def dynamic():
    result = [[0 for _ in range(capacity)] for _ in range(len(items))]
    for i in range(len(items)):
        for j in range(1, capacity + 1):
            x = items_prices[i] if items_weights[i] <= j else 0
            if j - items_weights[i] > 0 and i >= 1:
                x += result[i - 1][j - items_weights[i] - 1]
            result[i][j - 1] = max(x, result[i - 1][j - 1] if i - 1 >= 0 else 0)
    print(result[-1][-1])

dynamic()
'''
