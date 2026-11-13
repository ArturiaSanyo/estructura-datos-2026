def multiplicar(n, z):
    if n == 0:
        return 0
    else:
        return z + multiplicar(n - 1, z)

print(multiplicar(3, 2))  # Output: 6