# Parameters
I = abs(-0.5) # A
t = 1800 # s
F = 96485 # As/mol

# Mass constituents in grams
new_bath = True
old_bath = False
if new_bath:
    m_fe = 33.8
    m_ni = 112
    m_nis = 71.6
    m_water = 2500
    m_absorbic = 4.4
    m_tot = m_fe + m_ni + m_nis + m_water + m_absorbic

# Molar mass in g/mol
Mm_fe = 270.3
Mm_ni = 237.69
Mm_nis = 154.76

# Weight fraction
w_fe = m_fe / m_tot
w_ni = m_ni / m_tot
w_nis = m_nis / m_tot

m_t = (I * t) / (F * ( (w_fe * 3 / Mm_fe) + (w_ni * 2 / Mm_ni) + (w_nis * 2 / Mm_nis) ) )
print(f'Theoretical electrodeposition mass is {m_t:.2f} g.')

m_a = 0.0938 #g
print(f'You deposited {m_a:.2f} g.')

CE = (m_a/m_t)*100
print(f'Current efficiency of {CE:.2f} %.')
