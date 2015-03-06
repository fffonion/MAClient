# MAClient 韩服扩展(已失效)
## 概述
不适用于当前的韩服；外面还套了一层位加密

KISA SEED CBC，参见(http://en.wikipedia.org/wiki/SEED)[维基百科]

代码中NIST -> KISA, TOWFISH -> SEED

别问我密钥是啥，都开源了www

## 编译
Windows
```
set name=maclient_crypt_ext
cd /d %~dp0
gcc.exe -mdll -g -O0 -Wall -ID:\Dev\Python\Python27\include -ID:\Dev\Python\Python27\PC -c %name%.c -o %name%.o
python test.py
pause
```

*nix
```
GCC="x86_64-linux-gnu-gcc"
STRIP="x86_64-linux-gnu-strip"
MODULE="maclient_crypt_ext"
$GCC -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I/usr/include/python2.7 -c $MODULE.c -o /tmp/$MODULE.o
$GCC -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -D_FORTIFY_SOURCE=2 -g -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security /tmp/$MODULE.o -o ./$MODULE.so
$STRIP ./$MODULE.so
```

# MAClient Koren Server Cryptography Extension(Legacy)

## Summary
Not compatible with present KR server

KISA SEED CBC，refer to (http://en.wikipedia.org/wiki/SEED)[Wikipedia]

Replace NIST -> KISA, TOWFISH -> SEED

Keys are all shown in the code.

## Compile
Windows
```
set name=maclient_crypt_ext
cd /d %~dp0
gcc.exe -mdll -g -O0 -Wall -ID:\Dev\Python\Python27\include -ID:\Dev\Python\Python27\PC -c %name%.c -o %name%.o
python test.py
pause
```

*nix
```
GCC="x86_64-linux-gnu-gcc"
STRIP="x86_64-linux-gnu-strip"
MODULE="maclient_crypt_ext"
$GCC -pthread -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -fPIC -I/usr/include/python2.7 -c $MODULE.c -o /tmp/$MODULE.o
$GCC -pthread -shared -Wl,-O1 -Wl,-Bsymbolic-functions -Wl,-Bsymbolic-functions -Wl,-z,relro -fno-strict-aliasing -DNDEBUG -g -fwrapv -O2 -Wall -Wstrict-prototypes -D_FORTIFY_SOURCE=2 -g -fstack-protector --param=ssp-buffer-size=4 -Wformat -Werror=format-security /tmp/$MODULE.o -o ./$MODULE.so
$STRIP ./$MODULE.so
```