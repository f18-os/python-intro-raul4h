import sys

input = open(sys.argv[1],"r")
text = input.read()
count = {}

for x in '.,:;''"""':
    text=text.replace(x,'')

for x in '-\n':
    text=text.replace(x,' ')

text = text.lower()
text = text.split()

for word in text:
    if word not in count:
        count[word] = 1
    else:
        count[word] += 1

input.close()
output = open(sys.argv[2], "w")

sortedkeys = sorted(count.keys())

for item in sortedkeys: output.write(item + " " + str(count[item]) + "\n")

output.close()

print("Done")