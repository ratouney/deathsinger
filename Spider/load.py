f = open('champIds', 'r')

lines = f.readlines()

for l in lines:
    s = l.split(':')
    s[1] = s[1].rstrip()[1:]
    print(s)