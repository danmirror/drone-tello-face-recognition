
import numpy as np
import matplotlib.pyplot as plt

# Create a Matplotlib plot
fig, ax = plt.subplots()
line, = ax.plot([], [])

# Generate some new data
x = np.linspace(0, 10, 100)
y = np.exp(-x/2) * np.cos(2*np.pi*x)

# Update the plot with the new data
line.set_data(x, y)

# Display the plot
plt.show()