class articulo:
    nombre = ""
    cantidad = 0
    unidad = ""
    registro = False

    def __init__(self):
        self.nombre = ""
        self.cantidad = 0
        self.unidad = ""
        self.registro = True

    def __init__(self, registro):
        self.nombre = ""
        self.cantidad = 0
        self.unidad = ""
        self.registro = registro

    def __str__(self):
        return self.nombre + " " + str(self.precio)

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_unidad(self):
        return self.unidad

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_unidad(self, unidad):
        self.unidad = unidad

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_registro(self, registro):
        self.registro = registro

    def get_registro(self):
        return self.registro

    def is_registro(self):
        return self.registro

    def empezar_registro(self):
        self.registro = True

    def finalizar_registro(self):
        self.registro = False

    def is_nombre_empty(self):
        return self.nombre == ""

    def is_cantidad_empty(self):
        return self.cantidad == 0

    def is_unidad_empty(self):
        return self.unidad == ""

    def get_lista(self):
        return "comprar {} {} de {}\n".format(self.cantidad, self.unidad, self.nombre)
