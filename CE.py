def get_current_efficiency(m_1, m_2, I, t):
    # Variables, BATH, Mass constituents in grams, Watts bath made 01.02.21
    volume = 0.4 # L
    m_fe = 0 * volume # g/L
    m_ni = 48 * volume # g/L
    m_nis = 265 * volume # g/L
    #m_water = 300
    #m_absorbic = 0.5284
    m_tot = m_fe + m_ni + m_nis# + m_water + m_absorbic

    # Constants
    I = abs(I) # A
    F = 96485 # As/mol
    Mm_fe = 270.3 # g/mol
    Mm_ni = 237.69 # g/mol
    Mm_nis = 154.76 # g/mol
    A_sample = 12.5 # cm^2, only exposed area

    # Weight fraction
    w_fe = m_fe / m_tot
    w_ni = m_ni / m_tot
    w_nis = m_nis / m_tot

    m_t = (I * t) / (F * ( (w_fe * 3 / Mm_fe) + (w_ni * 2 / Mm_ni) + (w_nis * 2 / Mm_nis) ) )
    #print(f'Theoretical = {m_t:.2f} g')

    m_a =  m_2 - m_1
    #print(f'Actual = {m_a:.2f} g')

    CE = (m_a/m_t)*100
    #print(f'CE = {CE:.2f} %')

    loading = (m_a / A_sample) * 1000 # g to mg
    #print(f'Loading = {loading:.2f} mg/cm2')

    return  m_t, m_a, CE, loading