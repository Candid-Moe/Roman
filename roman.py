from __future__ import division
from functools import reduce

expansion = dict(M="DD", D="C" * 5, C="LL", L="X" * 5, X="VV", V="I" * 5, I="I")
compresion = (("I" * 5, "V"), ("VV", "X"), ("X" * 5, "L"), ("LL", "C"), ("C" * 5, "D"), ("DD", "M"))
tablaI = dict(M="M", D="D", C="C", L="L", X="X", V="V", I="I")
tablaV = dict(M="M" * 5, D="MMM", C="C" * 5, L="CCL", X="L", V="XXV", I="V")
tablaX = dict(M="M" * 10, D="MMMMM", C="M", L="D", X="C", V="L", I="X")
tablaL = dict(M="M" * 50, D="M" * 25, C="M" * 5, L="MMD", X="D", V="CCL", I="L")
tablaC = dict(M="M" * 100, D="M" * 50, C="M" * 10, L="M" * 5, X="M", V="C" * 5, I="C")
tablaD = dict(M="M" * 500, D="M" * 250, C="M" * 50, L="M" * 25, X="M" * 5, V="MMD", I="D")
tablaM = dict(M="M" * 1000, D="M" * 500, C="M" * 100, L="M" * 5, X="M" * 10, V="M" * 5, I="M")

tabla_mult = dict(I=tablaI, V=tablaV, X=tablaX, L=tablaL, C=tablaC, D=tablaD, M=tablaM)
factores = dict(M=1000, D=500, C=100, L=50, X=10, V=5, I=1)

class Roman:
    def __init__(self, value):

        if isinstance(value, int) and value > 0:
            value = Roman._int2roman(value)

        if not isinstance(value, str):
            raise ValueError("Not a roman numeral")

        dic = dict(M="", D="", C="", L="", X="", V="", I="")
        for letra in value.upper():
            dic[letra] += letra
        valor = "".join(dic.values())
        self.value = reduce(lambda a, b: a.replace(*b), compresion, valor)

    @classmethod
    def _coerce(cls, other):
        if isinstance(other, str) or isinstance(other, int):
            other = Roman(other)
        elif not isinstance(other, Roman):
            raise ValueError("Not a roman numeral:", other)
        return other

    @classmethod
    def _int2roman(cls, other):
        roman = ""
        for letra, factor in factores.items():
            num = other // factor
            if num:
                roman += letra * num
                other %= factor
        return roman

    def __add__(self, other):
        other = Roman._coerce(other)
        return Roman(self.value + other.value)

    def __radd__(self, other):
        return self + other

    def __iadd__(self, other):
        return self + other

    def __sub__(self, other):
        def last(valor):
            return "IVXLCDM".find(valor[-1])

        def roma_expand(valor):
            letra = valor[-1]
            return valor[:-1] + expansion[letra]

        other = Roman._coerce(other)
        valor1 = self.value
        valor2 = other.value

        while valor1 and valor2:
            while valor1[-1] != valor2[-1]:
                if last(valor1) > last(valor2):
                    valor1 = roma_expand(valor1)
                else:
                    valor2 = roma_expand(valor2)

            valor1 = valor1[:-1]
            valor2 = valor2[:-1]

        if valor2:
            raise ValueError("Negative result")

        return Roman(valor1)

    def __rsub__(self, other):
        other = Roman._coerce(other)
        return other - self

    def __isub__(self, other):
        return self - other

    def __mul__(self, other):
        other = Roman._coerce(other)
        producto = [tabla_mult[letra][val] for letra in other.value for val in self.value]
        return Roman("".join(producto))

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        return self * other

    def __div__(self, other):
        other = Roman._coerce(other)
        dividendo = self
        divisor = other

        tabla_multiplos = []
        multiplo = Roman("I")
        val = divisor
        ''' Construir tabla (divisor * n, n) para todos los 
            valores menores a este
        '''
        while dividendo >= val:
            tabla_multiplos.append((val, multiplo))
            val += val
            multiplo *= Roman("II")

        ''' Ir restando multiplos del divisor mientras se pueda.
            La cuenta de las resta es el cuociente. 
        '''
        cuociente = None
        while dividendo >= divisor:
            ''' Para no recalcular, usamos la tabla.
                Primero, eliminamos las entradas mayores al dividendo
            '''
            while dividendo < tabla_multiplos[-1][0]:
                tabla_multiplos.pop()

            dividendo -= tabla_multiplos[-1][0]
            if cuociente:
                cuociente += tabla_multiplos[-1][1]
            else:
                cuociente = tabla_multiplos[-1][1]
            ''' La entrada ya ha sido usada, descartarla de inmediato'''
            tabla_multiplos.pop()

        return cuociente, dividendo

    def __rdiv__(self, other):
        other = Roman._coerce(other)
        return other.__div__(self)

    def __idiv__(self, other):
        return self.__div__(other)

    def __truediv__(self, other):
        return self.__div__(other)

    def __rtruediv__(self, other):
        other = Roman._coerce(other)
        return other.__div__(self)

    def __itruediv__(self, other):
        return self.__div__(other)

    def __floordiv__(self, other):
        return self.__div__(other)

    def __rfloordiv__(self, other):
        other = Roman._coerce(other)
        return other.__div__(self)

    def __ifloordiv__(self, other):
        return self.__div__(other)

    def __mod__(self, other):
        cuociente, resto = self.__div__(other)
        return resto

    def __imod__(self, other):
        return self.__mod__(other)

    def __pow__(self, power, modulo=None):
        valor = self
        while power > "I":
            valor *= self
            power -= "I"
        return valor

    def __rpow__(self, other):
        other = Roman._coerce(other)
        return other.__pow__(self)

    def __ipow__(self, other):
        return self.__pow__(other)

    def __cmp__(self, other):
        other = Roman._coerce(other)
        ''' Caso iguales '''
        if self.value.__hash__() == other.value.__hash__():
            return 0
        ''' Caso distintos '''
        last = min(len(self.value), len(other.value))
        for index in range(last):
            idx1 = "IVXLCDM".index(self.value[index])
            idx2 = "IVXLCDM".index(other.value[index])
            if idx1 < idx2:
                return -1
            elif idx1 > idx2:
                return 1
        if len(self.value) == last:
            return -1
        elif len(other.value) == last:
            return 1
        return 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __gt__(self, other):
        return self.__cmp__(other) > 0

    def __ge__(self, other):
        return self.__cmp__(other) >= 0

    def __le__(self, other):
        return self.__cmp__(other) <= 1

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __format__(self, format_spec):
        def gen(result, cuenta):
            if cuenta > 4:
                result.append("(%d)" % cuenta)
            elif cuenta > 0:
                result[-1] = result[-1] * cuenta
            return result

        result = ['']
        if format_spec == "r":
            cuenta = 0
            for letra in self.value:
                if letra == result[-1]:
                    cuenta += 1
                else:
                    result = gen(result, cuenta)
                    result.append(letra)
                    cuenta = 1

            return "".join(gen(result, cuenta))
        else:
            return self.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __int__(self):
        valor = 0
        for letra in self.value:
            valor += factores[letra]
        return valor

    def __float__(self):
        return float(self.__int__())

    def __hash__(self):
        return self.value.__hash__()

    def __index__(self):
        return self.__int__()

    def __iter__(self):
        """Retorna cada una de las letras
        """
        return self.value.__iter__()