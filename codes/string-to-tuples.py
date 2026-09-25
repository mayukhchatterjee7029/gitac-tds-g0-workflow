
# Paste your mapping rows inside the triple quotes.
DATA = """
0 	0 	2 	1
0 	1 	1 	1
0 	2 	4 	1
0 	3 	0 	3
0 	4 	0 	1
1 	0 	1 	4
1 	1 	2 	0
1 	2 	2 	4
1 	3 	4 	2
1 	4 	2 	2
2 	0 	0 	0
2 	1 	3 	2
2 	2 	4 	3
2 	3 	3 	0
2 	4 	3 	4
3 	0 	1 	0
3 	1 	2 	3
3 	2 	3 	3
3 	3 	4 	4
3 	4 	0 	2
4 	0 	3 	1
4 	1 	1 	2
4 	2 	1 	3
4 	3 	0 	4
4 	4 	4 	0
"""

# Parse each non-empty line into a tuple of four integers.
tuples = []

for line in DATA.strip().splitlines():
    numbers = tuple(map(int, line.split()))

    if len(numbers) != 4:
        raise ValueError(f"Expected four numbers, got: {line}")

    tuples.append(numbers)

# Print the result in the requested format.
print(", ".join(map(str, tuples)))