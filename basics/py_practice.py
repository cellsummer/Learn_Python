# 15. reverse the words
def reverse(sentence):
    words = sentence.split()
    rev_sentence = " ".join(reversed(words))
    return rev_sentence


sentence = "welcome to the jungle"
print(reverse(sentence))

# 3. list less than 10

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]

print([num for num in a if num < 10])

# 5. list the overlap

a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

print(list(set(a).intersection(set(b))))


# 13. Fibonacci
def fibonacci(num):
    if num == 0:
        x = []
    if num == 1:
        x = [1]
    if num == 2:
        x = [1, 1]
    if num > 2:
        i = 0
        x = [1, 1]
        while i < num - 2:
            x.append(x[i] + x[i + 1])
            i += 1
    return x


print(fibonacci(10))
