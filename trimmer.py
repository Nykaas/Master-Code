
new_file = open(r'C:\Users\Ruben\Documents\In_situ\Pt-Ir\Durability_trimmed.txt', 'w')

with open(r'C:\Users\Ruben\Documents\In_situ\Pt-Ir\Durability.txt') as f:
    for i, line in enumerate(f):
        if i % 5000 == 0:
            new_file.write(line)
            print(i)

new_file.close()
f.close()


