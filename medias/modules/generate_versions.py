import random
P = "Python {}.{}"
p = "python {}.{}"
j = "Java {}"

ps = []
Ps = []

for major in [1, 2, 3]:
    for minor in range(20):
        ps.append(p.format(major, minor))
        Ps.append(P.format(major, minor))

js = []
for major in [4, 5, 6, 7, 8, 9]:
    js.append(j.format(major))

tmp = ps * 10 + Ps * 15 + js * 20
random.shuffle(tmp)
open("./versions.txt", "w").write("\n".join(tmp[:150]))
