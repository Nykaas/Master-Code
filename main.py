import matplotlib.pyplot as plt
import numpy as np

# Starting values
r = 0.04
T_s = 22.8
T_0 = 90
y = T_0

# Time interval 
a = 0
b = 50
#dt = float(input('Please enter a value for time step: '))
dt = 0.1
n = int((b-a)/dt)
time_rng = np.arange(a,b,dt)

# Arrays for solutions
def arrays(n):
    global analytical_sol, euler_sol, experimental
    analytical_sol = np.zeros(n)
    euler_sol = np.zeros(n)
    experimental = np.array([[0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,12.0,13.0,14.0,15.0],
                            [83.0,77.7,75.1,73.0,71.1,69.4,67.8,66.4,64.7,63.4,62.1,61.0,59.9,58.7,57.8,56.6]])

# Functions
def analytical(T_s,T_0,r,t): # Analytical solution
    return T_s + (T_0 - T_s)*np.exp(-r*t) 

def euler(dt,r,x,T_s):       # Euler's method
    return x + dt*(-r*(x-T_s))   

def solutions(y):            # Updating arrays with respective T(t)
    for i, t in enumerate(time_rng):
        analytical_sol[i] = analytical(T_s,T_0,r,t) 
        y = euler(dt,r,y,T_s) 
        euler_sol[i] = y
    return analytical_sol, euler_sol

def table(y2,y3,time):
    # Table header
    print('\n',' '*5,'\033[1m' + 'Iterations cream in coffee','\033[0m')
    print('-'*52)
    print('Time [min] | Cream at start [\N{DEGREE SIGN}C] | Cream at end [\N{DEGREE SIGN}C]')
    for i in range(0,len(y2)):
            print('%.2f'%time[i],'      |','%.2f'%y2[i],'\t             |','%.2f'%y3[i])
    return

# Simulating adding cream at 90 or 70 degrees
def cream():
    y2 = []
    y3 = []
    time = []
    y2.append(T_0 - 5) #85
    y3.append(T_0)     #90
    time.append(0)
    i = 0
    while y2[i] >= 65 and y3[i] >= 70: #Final temperature
        y2.append(euler(dt,r,y2[i],T_s)) # add cream at 90 degrees Celsius
        y3.append(euler(dt,r,y3[i],T_s)) # add cream at 70 degrees Celsius
        #time += dt
        time.append(time[i]+dt)
        i += 1
    y3[-1] -= 5
    print('\033[1m' + 'Coffee cup problem','\033[0m','\nAnswer to question iiv)')
    print('Final temperatures:\nCream at start:','%.2f'%y2[-1],'\N{DEGREE SIGN}C.\nCream at end:','%.2f'%(y3[-1]),'\N{DEGREE SIGN}C.')
    print('Final temperature of 65\N{DEGREE SIGN}C is fastest achieved when cream is added at 70\N{DEGREE SIGN}C at time','%.2f'%time[-1],'minutes.')
    if input('Show iterations? [yes/no] \n') == 'yes':
        table(y2,y3,time)
    return

# Plotting
def plots():
    plt.plot(time_rng, analytical_sol, 'b-', label = 'Analytical solution')
    plt.plot(time_rng, euler_sol, 'r-', label = "Euler's method")
    plt.plot(experimental[0], experimental[1], 'g-', label = 'Experimental')
    plt.xlabel('Time [min]')
    plt.ylabel('Temperature [\N{DEGREE SIGN}C]')
    plt.legend()
    #plt.xlim(0,15) ## Uncomment to scale graphs for experimental data
    plt.title('Coffe cup problem')
    plt.show()
    return

# Data for Excel
def save_data():
    np.savetxt('Experimental_data.txt', experimental, delimiter = ';', fmt='%1.1f')
    np.savetxt('Analytical_sol_data.txt', analytical_sol, delimiter = ';', fmt='%1.1f')
    return

# Main runnning function for code
def main(n,y):
    arrays(n)
    #solutions(y)
    cream()
    plots()
    #save_data() ## Uncomment to save experimental and analytical data
    return

main(n,y)