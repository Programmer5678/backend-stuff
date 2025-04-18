from boltons.iterutils import chunked

data = list(range(10))
print(chunked(data, 3))  # → [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
