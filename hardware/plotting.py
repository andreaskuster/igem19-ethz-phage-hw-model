import numpy as np
import matplotlib.pyplot as plt

fig = plt.figure(figsize=(15,10))

data = np.genfromtxt('pre_processed_sensor_data.csv', delimiter=',')
data = [1/x for x in data]
#np.savetxt("test.csv", [x[0] for x in data])

x = np.linspace(0, len(data)-1, len(data))

plt.ylabel('Sensor Value [Units]')
plt.xlabel('Time [13s]')
plt.plot(x, data)
plt.title('Raw OD Sensor Data')
plt.legend()
plt.savefig("raw_sensor.png")
plt.show()


