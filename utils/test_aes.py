import pyaes
cod1 = pyaes.new('1' * 16, pyaes.MODE_ECB)
strc = 'asdnlasbkdjabkdbasduaskjduiqci uyeique uqwcelk jasdc idasjdia' * 64

try:
    from Crypto.Cipher import AES
    cod2 = AES.new('1' * 16, AES.MODE_ECB)
except:
    pass

def test1():
    cod1.encrypt(strc)

def test2():
    cod2.encrypt(strc)

if __name__ == '__main__':
    from timeit import Timer
    t1 = Timer("test1()", "from __main__ import test1")
    print t1.repeat(3, 1000)
    t2 = Timer("test2()", "from __main__ import test2")
    print t2.repeat(3, 1000)
