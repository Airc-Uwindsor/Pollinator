# Step 1: Install plotly
# Run this command in your terminal:
# pip install plotly

import plotly.graph_objs as go
import plotly.io as pio

# Step 2: Read the target positions from the file
with open('targets.txt', 'r') as f:
    target_positions = f.readlines() # target: (x, y, z)\n

# Step 3: Parse the target positions
targets = []
for target_position in target_positions:
    target_position = target_position.strip() # (x, y, z)
    target_position = target_position[1:-1] # x, y, z
    x, y, z = target_position.split(', ')
    x, y, z = float(x), float(y), float(z)
    target = (x, y, z)
    targets.append(target)

# Extract x, y, z coordinates
x_coords = [target[0] for target in targets]
y_coords = [target[1] for target in targets]
z_coords = [target[2] for target in targets]

# Step 4: Create a 3D scatter plot using plotly
scatter = go.Scatter3d(
    x=x_coords,
    y=y_coords,
    z=z_coords,
    mode='markers',
    marker=dict(
        size=5,
        color='red',
        opacity=0.8
    )
)

layout = go.Layout(
    scene=dict(
        xaxis_title='X',
        yaxis_title='Y',
        zaxis_title='Z'
    )
)

fig = go.Figure(data=[scatter], layout=layout)

# Show the plot
pio.show(fig)