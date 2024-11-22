from roman import Roman

def test2():
    a = Roman("XII")
    print(a + 3)
    print(3 + a)
    print(a + "III")
    print("III" + a)

    b = Roman("VIII")
    b += 2
    b += "X"
    print(b)
    print(int(b))
    print(float(b))

    c = "abcdefghijklmnopqrstuvwxyz"
    print(c[Roman("I"):Roman("III")])

    print(f"Romano({a})")
    print("Romano(%r)" % a)
    print("Romano({})".format(a))


    print(a < 12)
    print(a <= 12)
    print(a > 12)
    print(a >= 12)
    print(12 > a)
    print(12 < a)

def test():
    print(Roman("IIIIII"))
    a = Roman("III")
    b = Roman("III")
    c = a + b
    print(c)
    c = c - Roman("V")
    print(c)
    c = Roman("XXV") * Roman("LV")
    print(c)
    c = "vv" + Roman("XXV") + "L"
    print(c)
    c += "MI"
    print(c)
    c = Roman("I" * 99)
    print(c)
    c += 10
    print(c)
    c = Roman("MML")
    d = Roman("MXXIIII")
    if c > d:
        print("Mayor")
    c = Roman("MMMMMMMMMM") / "II"
    print(c)
    c = Roman("XXV") / Roman("V")
    print(c)
    c = Roman("XXVIII") / Roman("IIII")
    print(c)
    c = Roman("MMMDCXXXXI") / Roman("XX")
    print(c)
    print("Pow")
    c = Roman("II")**Roman("XVI")
    print(c)
    print("Formato {0:r}".format(c))
#    for i in range(1, 1000, 1):
#        print(i, Roman(i))

def test3():
    c = Roman(2145);
    print(c)
    for x in c:
        print(x, end= " ")

if __name__ == '__main__':
    test3()
