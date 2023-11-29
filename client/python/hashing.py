from bcrypt import checkpw, hashpw, gensalt
import copy
salt=gensalt()
salt1=gensalt()
x="123"
hx=hashpw(x.encode('utf-8'),salt)
print(hx)
dhx=hx.decode('utf-8')
print(x.encode('utf-8'),dhx.encode('utf-8'),"\n\n\n")

print(checkpw(x.encode('utf-8'),dhx.encode('utf-8')))