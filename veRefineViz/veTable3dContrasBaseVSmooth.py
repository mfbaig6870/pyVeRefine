import pandas as pd
import plotly.graph_objects as go

# Read the first CSV file into a pandas DataFrame
df = pd.read_csv('../inputs/ve_table.csv')

# Reverse the order of the rows in the result dataframe
df = df[::-1]

# Create a list of the RPM values and a list of the MAP values
x = df.columns[1:]
y = df.iloc[:, 0]

# Reverse the order of the rows in the result dataframe
y = y[::-1]

# Create a 2D array of the Z values
z = df.iloc[:, 1:].values

# Define the colors for the first surface plot
colormap = ['rgb(50, 0, 75)', 'rgb(200, 0, 200)', '#c8dcc8']
colorscale = [[0, colormap[0]], [0.5, colormap[1]], [1, colormap[2]]]

# Create the first 3D surface plot with the defined colors
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, surfacecolor=z, colorscale=colorscale, opacity=0.5)])

# Add the wireframe trace
fig.add_trace(go.Scatter3d(
    x=x, y=[y[0]]*len(x), z=z[0],
    mode='lines',
    line=dict(color='black', width=1),
    showlegend=False
))
for i in range(1, len(y)):
    fig.add_trace(go.Scatter3d(
        x=x, y=[y[i]]*len(x), z=z[i],
        mode='lines',
        line=dict(color='black', width=1),
        showlegend=False
    ))
for i in range(len(x)):
    fig.add_trace(go.Scatter3d(
        x=[x[i]]*len(y), y=y, z=z[:, i],
        mode='lines',
        line=dict(color='black', width=1),
        showlegend=False
    ))

# Set the layout
fig.update_layout(
    title='3D Surface Plot with Wireframe and Colormap',
    autosize=False,
    width=800, height=800,
    scene=dict(
        xaxis_title='RPM',
        yaxis_title='MAP',
        zaxis_title='Z values',
        aspectratio=dict(x=1, y=1, z=0.5)
    )
)

# Read the second CSV file into another pandas DataFrame
df2 = pd.read_csv('../outputs/smoothedVeTable.csv')

# Reverse the order of the rows in the result dataframe
df2 = df2[::-1]

# Create a list of the RPM values and a list of the MAP values
x2 = df2.columns[1:]
y2 = df2.iloc[:, 0]

# Reverse the order of the rows in the result dataframe
y2 = y2[::-1]

# Create a 2D array of the Z values
z2 = df2.iloc[:, 1:].values

# Define the colors for the second surface plot
colormap2 = ['rgb(50, 0, 75)', 'rgb(200, 0, 200)', '#c8dcc8']
colorscale2 = [[0, colormap2[0]], [0.5, colormap2[1]], [1, colormap2[2]]]

# Create a new Surface trace for the second surface plot
surf2 = go.Surface(x=x2, y=y2, z=z2, surfacecolor=z2, colorscale=colorscale2, opacity=0.5)

# Add the new Surface trace to the existing data
fig.add_trace(surf2)

# Call the show method to display the combined plot
fig.show()
