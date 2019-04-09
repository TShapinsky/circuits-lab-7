import smu
import numpy as np

s = smu.smu()

v = np.linspace(-.4,.4,1000)

measuring = "I1"

f = open("data/T1.{!s}.csv".format(measuring),'w')
f.write("Vdm, {!s}\n".format(measuring))

s.set_voltage(1,-.2)
s.autorange(1)
s.set_voltage(2,5)
s.autorange(2)

for val in v:
    s.set_voltage(1,val)
    s.autorange(1)
    s.set_voltage(2,5)
    s.autorange(2)
    f.write('{!s},{!s}\n'.format(val,s.get_current(2)))

s.set_current(1,0)
f.close()
