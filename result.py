f = open('result_new.txt')
n = 1
a1 = []
a2 = []
a3 = []
a4 = []
for line in f:
    if line != '\n':
        if n == 1:
            a1.append(float(line))
            n += 1
        elif n == 2:
            a2.append(float(line))
            n += 1
        elif n == 3:
            a3.append(float(line))
            n += 1
        else:
            a4.append(float(line))
            n = 1
print(a1)
print(a2)
print(a3)
print(a4)
print('E')
print(sum(a1)/len(a1))
print(sum(a2)/len(a2))
print(sum(a3)/len(a3))
print(sum(a4)/len(a4))
print('min')
print(min(a1))
print(min(a2))
print(min(a3))
print(min(a4))
print('max')
print(max(a1))
print(max(a2))
print(max(a3))
print(max(a4))
print('D')
print((sum([x*x for x in a1])/len(a1))-(sum(a1)/len(a1))*(sum(a1)/len(a1)))
print((sum([x*x for x in a2])/len(a2))-(sum(a2)/len(a2))*(sum(a2)/len(a2)))
print((sum([x*x for x in a3])/len(a3))-(sum(a3)/len(a3))*(sum(a3)/len(a3)))
print((sum([x*x for x in a4])/len(a4))-(sum(a4)/len(a4))*(sum(a4)/len(a4)))
