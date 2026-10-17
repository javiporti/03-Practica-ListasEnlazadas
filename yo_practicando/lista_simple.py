# lista_simple.py
# La lista SIMPLEMENTE enlazada del repaso (bloque 2): version para completar.
#
# Solo tiene puntero al SIGUIENTE. Por eso todo lo que necesita "mirar hacia
# atras" obliga a recorrer desde la cabeza:
#   delete_last  -> O(n): hay que encontrar el penultimo
#   delete_node  -> O(n): hay que encontrar el anterior del nodo
#   recorrer hacia atras -> no hay forma directa
#
# Completa cada metodo marcado con TODO. Lo demas ya esta hecho.
# Orden recomendado: insert_first -> insert_last -> __iter__ -> buscar
#                    -> delete_first -> __getitem__ -> delete_last -> delete_node
#
# INVARIANTE (debe ser cierto al terminar CADA operacion):
#   - tamano == 0  <=>  cabeza is None  <=>  cola is None
#   - si no esta vacia: cola.siguiente is None
#   - de cabeza a cola, siguiendo "siguiente", hay exactamente "tamano" nodos


class Nodo:
    __slots__ = ("dato", "siguiente")

    def __init__(self, dato):
        self.dato = dato
        self.siguiente = None


class ListaSimple:
    def __init__(self, iterable=None):
        self.cabeza = None
        self.cola = None          # con puntero a cola, insert_last es O(1)
        self.tamano = 0
        if iterable is not None:
            for dato in iterable:
                self.insert_last(dato)

    def __len__(self):
        return self.tamano

    def __iter__(self):
        """Genera los datos de cabeza a cola (usa yield). Coste: O(n)."""
        actual = self.cabeza
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __getitem__(self, pos):
        """Devuelve el dato en la posicion pos. Coste: O(n).
        Si pos esta fuera de [0, tamano) lanza IndexError."""
        # TODO
        if pos < 0 or pos >= self.tamano: raise IndexError
        actual = self.cabeza
        for _ in range(pos):
            actual = actual.siguiente
        return actual.dato

    def buscar(self, dato):
        """Devuelve el PRIMER NODO cuyo dato es 'dato', o None si no esta.
        Coste: O(n)."""
        actual = self.cabeza
        for _ in range(self.tamano):
            if actual.dato == dato:
                return actual
            actual = actual.siguiente
        return 

    def insert_first(self, dato):                       # O(1)
        """Inserta al principio y devuelve el nodo nuevo.
        Cuidado: lista vacia (la cola tambien cambia)."""
        nuevo = Nodo(dato)
        #Consideramos según el tamaño de la lista (si es 0 entonces tanto la cola como la cabeza son `nuevo`):
        if self.tamano == 0:
            self.cabeza = self.cola = nuevo
            
        else:   #la lista tiene cabeza:
            nuevo.siguiente = self.cabeza   
            self.cabeza = nuevo
            
        #actualizamos el tamaño de la lista y devolvemos el dato:
        self.tamano += 1
        return nuevo
        

    def insert_last(self, dato):                        # O(1) gracias a cola
        """Inserta al final y devuelve el nodo nuevo.
        Cuidado: lista vacia."""
        nuevo = Nodo(dato)
        #Consideramos según el tamaño de la lista (si es 0 entonces tanto la cola como la cabeza son `nuevo`):
        if self.tamano == 0:
            self.cabeza = self.cola = nuevo
            
        else: #Revisamos el final:
            self.cola.siguiente = nuevo
            self.cola = nuevo
        
        #actualizamos el tamaño de la lista y devolvemos el dato:
        self.tamano += 1
        return nuevo

    def delete_first(self):                             # O(1)
        """Borra el primero y devuelve su dato.
        Lista vacia -> IndexError. Cuidado: si solo habia un elemento."""
        #consideramos si la lista está vacía:
        if self.cabeza is None:
            raise IndexError("delete_first la lista esta vacia")
        
        #Hay mal menos 1 elemento:
        x = self.cabeza       
        self.cabeza = self.cabeza.siguiente
        
        #comprobamos si ahora la lista quedaría vacía -> la cola a NONE!!!
        if self.cabeza is None:
            self.cola = None
        
        #actualizamos el tamaño de la lista y devolvemos el dato:
        self.tamano -= 1
        return x.dato

    def delete_last(self):                              # O(n)
        """Borra el ultimo y devuelve su dato.
        Lista vacia -> IndexError. Cuidado: si solo habia un elemento.
        Pista: hay que encontrar el PENULTIMO recorriendo desde la cabeza."""
        if self.tamano == 0:
            raise IndexError("delete_first: la lista esta vacia")  
        if self.tamano == 1:
            y = self.cabeza
            self.cabeza = self.cola = None #!
            self.tamano -= 1
            return y.dato
        #Hay más de un elemento:
        actual = self.cabeza  
        x = self.cola   
        for _ in range(self.tamano - 2):    
            actual = actual.siguiente
            
        #`actual` ahora es el penultimo:
        actual.siguiente = None
        self.cola = actual
        
        #comprobamos si ahora la lista quedaría vacía -> la cabeza a NONE!!!
        if self.cola is None:
            self.cabeza = None
                    
        #actualizamos el tamaño de la lista y devolvemos el dato:
        self.tamano -= 1
        return x.dato

    def delete_node(self, nodo:Nodo):                        # O(n)
        """Borra 'nodo' (que pertenece a la lista) y devuelve su dato.
        Casos: es la cabeza / es la cola / esta en medio.
        Pista: hay que encontrar el ANTERIOR a 'nodo' recorriendo."""
        #1. Comprobaciones de tamaño:
        if self.tamano == 0:
            raise TypeError("delete_first: la lista esta vacia") 

        #2. La lista tiene al menos 1 elemento:
            #--> comprobamos si se trata del ultimo (para evitar recorrerla entera) o el primero (no se encontraría):
        if self.cabeza == nodo:
            self.delete_first()
            return nodo.dato
        if self.cola == nodo:
            self.delete_last()
            return nodo.dato
        
        #3. Está en el medio:
        actual = self.cabeza
        while actual.siguiente is not None:
            if actual.siguiente == nodo:  #encontrado!
                actual.siguiente = nodo.siguiente
                nodo.siguiente = None
                self.tamano -= 1
                return nodo.dato
            actual = actual.siguiente
        #si se ejecuta esta parte del código quiere decir que el nodo no pertence a la lista:
        raise ValueError
        
     
# ---------------------------------------------------------------------------
# Autocomprobacion: ejecuta  python lista_simple.py
# ---------------------------------------------------------------------------
def _invariante_ok(l):
    if l.tamano == 0:
        return l.cabeza is None and l.cola is None
    if l.cola.siguiente is not None:
        return False
    n, actual = 0, l.cabeza
    while actual is not None:
        n += 1
        actual = actual.siguiente
    return n == l.tamano


def _prueba(nombre, f):
    try:
        f()
        print(f"OK       {nombre}")
    except NotImplementedError:
        print(f"PENDIENTE {nombre}")
    except Exception as e:  # noqa: BLE001
        print(f"FALLA    {nombre}: {type(e).__name__} {e}")


def _t_insert_first():
    l = ListaSimple()
    l.insert_first(1)
    l.insert_first(2)
    assert list(l) == [2, 1] and len(l) == 2 and _invariante_ok(l)


def _t_insert_last():
    l = ListaSimple()
    l.insert_last(1)
    l.insert_last(2)
    assert list(l) == [1, 2] and len(l) == 2 and _invariante_ok(l)


def _t_getitem():
    l = ListaSimple([5, 6, 7])
    assert l[0] == 5 and l[2] == 7
    try:
        l[3]
        assert False, "debia lanzar IndexError"
    except IndexError:
        pass


def _t_buscar():
    l = ListaSimple([1, 2, 3])
    assert l.buscar(2).dato == 2 and l.buscar(9) is None


def _t_delete_first():
    l = ListaSimple([1, 2])
    assert l.delete_first() == 1 and _invariante_ok(l)
    assert l.delete_first() == 2 and _invariante_ok(l) and len(l) == 0
    try:
        l.delete_first()
        assert False, "debia lanzar IndexError"
    except IndexError:
        pass


def _t_delete_last():
    l = ListaSimple([1, 2, 3])
    assert l.delete_last() == 3 and list(l) == [1, 2] and _invariante_ok(l)
    assert l.delete_last() == 2 and l.delete_last() == 1
    assert len(l) == 0 and _invariante_ok(l)
    l.insert_last(9)                       # sigue funcionando tras vaciarse
    assert list(l) == [9] and _invariante_ok(l)


def _t_delete_node():
    l = ListaSimple([1, 2, 3, 4])
    assert l.delete_node(l.buscar(2)) == 2 and list(l) == [1, 3, 4]
    assert l.delete_node(l.buscar(4)) == 4 and list(l) == [1, 3]   # la cola
    assert l.delete_node(l.buscar(1)) == 1 and list(l) == [3]      # la cabeza
    assert _invariante_ok(l)
    l.insert_last(8)
    assert list(l) == [3, 8] and _invariante_ok(l)


def _t_contra_list():
    import random
    random.seed(1)
    l, ref = ListaSimple(), []
    for _ in range(2000):
        op = random.choice(["fi", "la", "df", "dl", "dn"])
        if op == "fi":
            x = random.randint(0, 9)
            l.insert_first(x)
            ref.insert(0, x)
        elif op == "la":
            x = random.randint(0, 9)
            l.insert_last(x)
            ref.append(x)
        elif op == "df" and ref:
            assert l.delete_first() == ref.pop(0)
        elif op == "dl" and ref:
            assert l.delete_last() == ref.pop()
        elif op == "dn" and ref:
            i = random.randrange(len(ref))
            nodo = l.cabeza
            for _ in range(i):
                nodo = nodo.siguiente
            assert l.delete_node(nodo) == ref.pop(i)
        assert list(l) == ref and _invariante_ok(l)


if __name__ == "__main__":
    _prueba("insert_first", _t_insert_first)
    _prueba("insert_last", _t_insert_last)
    _prueba("__getitem__", _t_getitem)
    _prueba("buscar", _t_buscar)
    _prueba("delete_first", _t_delete_first)
    _prueba("delete_last", _t_delete_last)
    _prueba("delete_node", _t_delete_node)
    _prueba("contra list (2000 ops)", _t_contra_list)