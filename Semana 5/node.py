class Nodo:
    def _init_(self, dato):
        self.dato = dato
        self.siguiente = None

a = Nodo(5)
b = Nodo(10)

print("Referencia del objeto a:", a)
print("Referencia del objeto b:", b)

a.siguiente = b

c = Nodo(15)
d = Nodo(20)
b.siguiente = c
c.siguiente = d