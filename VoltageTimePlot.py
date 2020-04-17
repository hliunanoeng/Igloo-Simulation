from os.path import join
import numpy as np
from matplotlib import style
import matplotlib.pyplot as plt

style.use('ggplot')

tvec=np.load('Example/results/axon_tvec.npy')

'''
V_Uncovered=np.load('Uncovered/Uncovered_results/Voltage000.npy')*1000

V_S2=np.load('Example/results/Voltage000.npy')*1000

V_S4=np.load('S4/S4_results/Voltage000.npy')*1000

V_S6=np.load('S6/S6_results/Voltage000.npy')*1000

fig=plt.figure()
ax1=fig.add_subplot(111)
ax2=fig.add_axes([0.78,0.16,0.11,0.1])
ax1.plot(tvec,V_Uncovered,label='Uncovered',linestyle='--',c='r')
ax1.plot(tvec,V_S2,label='2 Openings')
ax1.plot(tvec,V_S4,label='4 Openings')
ax1.plot(tvec,V_S6,label='6 Openings')
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Voltage ($\mu$V)')
ax1.set_title('Signal Amplitude Decreases with the Number of Openings (Diameter 300$\mu$m, Width 5$\mu$m, Height 3$\mu$m)')
ax1.legend(loc='best')
ax2.plot(tvec,V_Uncovered,label='Uncovered',linestyle='--',c='r')
ax2.legend(loc=1,prop={'size':5})
plt.show()

'''

'''
S2_D45=np.load('Example/results/Voltage000D45.npy')*1000
S2_D60=np.load('Example/results/Voltage000D60.npy')*1000
S2_D90=np.load('Example/results/Voltage000D90.npy')*1000
S2_D150=np.load('Example/results/Voltage000D150.npy')*1000
S2_D200=np.load('Example/results/Voltage000D200.npy')*1000
S2_D300=np.load('Example/results/Voltage000D300.npy')*1000


fig=plt.figure()
ax1=fig.add_subplot(111)
ax1.plot(tvec,S2_D45,label='Diameter 45$\mu$m')
ax1.plot(tvec,S2_D60,label='Diameter 60$\mu$m')
ax1.plot(tvec,S2_D90,label='Diameter 90$\mu$m')
ax1.plot(tvec,S2_D150,label='Diameter 150$\mu$m')
ax1.plot(tvec,S2_D200,label='Diameter 200$\mu$m')
ax1.plot(tvec,S2_D300,label='Diameter 300$\mu$m')
ax1.set_xlabel('Time (ms)')
ax1.set_ylabel('Voltage ($\mu$V)')
ax1.set_title('Signal Amplitude Increases with the Igloo Diameter (2 Openings, Width 5$\mu$m, Height 3$\mu$m)')
ax1.legend(loc='best')
source_pos = np.load(join('Example/results', "source_pos.npy"))
plt.show()
'''