import js2py
import pandas as pd

df = pd.read_excel('copycorrelationtest.xlsx')
df['new'] = list(zip(df['H. tmp Lat'], df['H. tmp Lng']))

js1 = '''pairCoordinates = function(lat, lng) {
  return lat * 10000000 << 16 & 0xffff0000 | lng * 10000000 & 0x0000ffff;
}

'''

def fun(x, y):
    return js2py.eval_js(js1)(x, y)

#print(js2py.eval_js(js1)(1, 1))

coordinates = [fun(x, y) for x, y in df['new']]

#df['H. tmp coordinates'] = coordinates

print(coordinates)

df.to_excel('copycorrelationtest.xlsx')



#df['new'] = [res1(lat, long) for lat, long in ]

