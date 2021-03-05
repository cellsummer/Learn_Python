# list
lst_a = [1, 3, 5, 7, 9]
lst_b = [2, 4, 6, 8, 10]

# list computation
result = [a * b * b for a, b in zip(lst_a, lst_b)]
print(result)

# tuples
tup_a = (1, 2)
tup_b = (3, 4)

print([tup_a, tup_b])
print(list(tup_a))

# sets
set_a = {1, 3, 4, 5, 8}
set_b = {2, 4, 5, 7, 8}

print(set_a.intersection(set_b))
print(list(set_a))

# convert list to set
print(set(lst_b))

# generator: it can use both list and sets
demo_generator = (arg * arg for arg in lst_a)
gen_b = (arg * arg for arg in set_a)

print(next(gen_b))
print(next(gen_b))
print(next(demo_generator))
print(next(demo_generator))
print(next(demo_generator))

# dictionary
dict_a = {"key1": 1, "key2": 4, "key3": 9, "key4": 16}

print(dict_a["key1"])
item1, item2, item3, _ = dict_a
print([item1, item2, item3])
print([*dict_a])

# convert dictionary into list of tuples
lst_a_from_dict_a = [(key, value) for key, value in dict_a.items()]
print(lst_a_from_dict_a)
