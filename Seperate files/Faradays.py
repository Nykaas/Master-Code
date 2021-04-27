### This code executes Faraday's laws of electrolysis to calculate the theoretical loading and plating rate ###

Ni = 0.66
Fe = 0.06
P = 0.28
current_density = 5 # mA/cm2
minutes = 60

### Alloy element information ###
Mm_Ni = 58.69 # g/mol
z_Ni = 2
sum_Ni = (Ni*z_Ni) / Mm_Ni

Mm_Fe = 55.85 # g/mol
z_Fe = 2
sum_Fe = (Fe*z_Fe) / Mm_Fe

Mm_P = 30.97 # g/mol
z_P = 3
sum_P = (P*z_P) / Mm_P

### Calculation ###
loading = ((current_density/1000) * (minutes*60)) / (96485 * (sum_Ni + sum_Fe + sum_P))
rate = loading / (minutes/60)

print(f'Theoretical plated loading is {loading*1000:.2f} mg/cm\N{SUPERSCRIPT TWO}, while the plating rate is {rate*1000:.2f} mg/cm\N{SUPERSCRIPT TWO}h.')
