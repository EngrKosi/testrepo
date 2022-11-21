import math
import random
import numpy as np
import matplotlib.pyplot as plt

def handle_close(evt):
    global fig
    fig = None # Closed Figure!

fig, ax = plt.subplots()
fig.canvas.mpl_connect('close_event', handle_close)

# Specify coordinates of the outline of the container
boundary_x = [-0.1,-0.1,-1,-1, 1, 1, 0.1, 0.1]
boundary_y = [ 1.2,   1, 1,-1,-1, 1, 1,   1.2]

# Plot the outline as a solid red line, and hold the figure
plt.plot(boundary_x, boundary_y, 'r-')
plt.xlim(-1.2, 1.2)
plt.ylim(-1.2, 1.2)

# Specify the initial position of the particle
x = np.asarray([0,1.2])

ParticleInNeck = True
ParticleInMain = False

# Specify the initial velocity of the particle
v = np.asarray([2,-1])

# Plot the particle in its initial position as a blue circle
# assign the plot handle to the variable 'b' so we can update later
b, = plt.plot(x, 'bo')

# Specify initial time and time-step
t = 0.0
dt = 0.01

clock_x = -1.1
clock_y =  1.1
th, = plt.plot([clock_x,clock_x], [clock_y,clock_y+0.05], 'k-')
tm, = plt.plot([clock_x,clock_x], [clock_y,clock_y+0.10], 'b-')
ts, = plt.plot([clock_x,clock_x], [clock_y,clock_y+0.10], 'r:')

plt.show(block=False)

while True:
    plt.pause(dt)

    # ==== * * * Section B * * * ====
    # Specify acceleration of the particle
    a = np.asarray([0,0]) # i.e., no acceleration

    # Update the velocity and position of the particle
    v = v + a * dt
    x = x + v * dt
    
    # Assume for the moment that the particle is outside the boundaries
    ParticleOutsideBoundaries = True

    # If the particle is outside the boundaries, then we have a record of
    # where it was previously, i.e., in the neck or in the main container.
    while ParticleOutsideBoundaries:
        # Check boundaries
        if (x[0] > 1.2) or (x[0] < -1.2) or (x[1] > 1.2) or (x[1] < -1.2):
            # particle lost for good; restart
            x[0] = random.uniform(-0.1, 0.1)
            x[1] = 1.2
            v[1] = random.uniform(-1, -0.25)
            v[0] = math.sqrt(1 - v[1]**2)
    
        # If the particle is in the neck, record this fact.
        if (x[0] >= -0.1) and (x[0] <= 0.1) and (x[1] > 1):
            ParticleInNeck = True
            ParticleInMain = False

            # Particle inside boundaries, no need to worry
            ParticleOutsideBoundaries = False
            break
    
        # If the particle is in the main container, record this fact.
        if (x[0] >= -1) and (x[0] <= 1) and (x[1] >= -1) and (x[1] <= 1):
            ParticleInMain = True
            ParticleInNeck = False

            # Particle inside boundaries, no need to worry
            ParticleOutsideBoundaries = False
            break
        
        if ParticleInMain:
            # ==== * * * Section A * * * ====
            # Add code here to bounce off walls in main container,
            # i.e., the particle has travelled outside the walls and
            # so the position needs to be reflected inside and the
            # component of velocity normal to the wall reversed.
            break # (delete this line)
        elif ParticleInNeck:
            if x[0] < -0.1:
                x[0] = -0.2 - x[0]
                v[0] = -v[0]
            elif x[0] > 0.1:
                x[0] = 0.2 - x[0]
                v[0] = -v[0]
    
    # Update the x- and y-coordinates associated with the plot
    b.set_xdata([x[0]])
    b.set_ydata([x[1]])
    
    # Update the clock
    t = t + dt
    if t > 43200:
        t = t - 43200 # 12 hour day

    count_hour = math.floor(t / 3600)
    count_mins = math.floor((t - 3600 * count_hour) / 60)
    count_secs = t - 3600 * count_hour - 60 * count_mins
    angle_hour = 2 * math.pi * (count_hour / 12)
    angle_mins = 2 * math.pi * (count_mins / 60)
    angle_secs = 2 * math.pi * (count_secs / 60)
    th.set_xdata([clock_x, clock_x + 0.05 * math.sin(angle_hour)])
    th.set_ydata([clock_y, clock_y + 0.05 * math.cos(angle_hour)])
    tm.set_xdata([clock_x, clock_x + 0.10 * math.sin(angle_mins)])
    tm.set_ydata([clock_y, clock_y + 0.10 * math.cos(angle_mins)])
    ts.set_xdata([clock_x, clock_x + 0.10 * math.sin(angle_secs)])
    ts.set_ydata([clock_y, clock_y + 0.10 * math.cos(angle_secs)])

    if fig is None:
        break
    plt.draw()
