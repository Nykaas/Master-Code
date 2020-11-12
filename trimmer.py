
new_file = open(r'C:\Users\Ruben\Documents\In_situ\Pt-NiF\Durability_trimmed_2.txt', 'w')

with open(r'C:\Users\Ruben\Documents\In_situ\Pt-NiF\Durability_trimmed.txt') as f:
    for i, line in enumerate(f):
        if i % 5 == 0:
            new_file.write(line)
            print(i)


