import statistics

uncertainty = {
    'NF_Overpotential': [381, 393, 387], # Ex_Reference
    'NF_ECSA': [440.61, 316.73, 376.97], # Ex_Reference
    'NF_bzt': [21.86, 27.3, 24.57], # Ex_Reference
    'ED_loading': [1.98, 1.66, 1.22],
    'ED_Overpotential': [308, 305, 331], # Ex_Uncertainty
    'ED_ECSA': [460.15, 715.91, 370.61], # Ex_Uncertainty
    'ED_bzt': [14.72, 16.27, 17.41] # Ex_Uncertainty
}

for key in uncertainty:
    sd = statistics.stdev(uncertainty[key])
    mean = sum(uncertainty[key])/len(uncertainty[key])
    sd_percent = sd/mean * 100
    print(f'SD {key} = {round(sd, 2)} or {round(sd_percent, 2)} %')


    