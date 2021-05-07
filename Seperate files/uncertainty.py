import statistics
uncertainty = {
    'NF_Overpotential': [381, 393, 387],
    'NF_ECSA': [609.85, 515.91, 617.88],
    #'NF_bzt': [],
    'ED_loading': [1.98, 1.66, 1.22],
    'ED_Overpotential': [308, 305, 331],
    'ED_ECSA': [3756.97, 1219.24, 609.7],
    #'ED_bzt': []
}

for key in uncertainty:
    sd = statistics.stdev(uncertainty[key])
    mean = sum(uncertainty[key])/len(uncertainty[key])
    sd_percent = sd/(mean) * 100
    print(f'SD {key} = {round(sd, 2)} or {round(sd_percent, 2)} %')


    