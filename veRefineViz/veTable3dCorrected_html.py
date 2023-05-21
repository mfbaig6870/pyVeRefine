import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

# Specify the absolute path to the CSV file
csv_path = 'C:/Users/mfbai/PycharmProjects/pyVeRefine/outputs/correctedVeTable.csv'

# Load the CSV file into a pandas dataframe
df = pd.read_csv(filepath_or_buffer=csv_path)

# Read the CSV file into a pandas DataFrame
# df = pd.read_csv('../outputs/correctedVeTable.csv')

# Reverse the order of the rows in the result dataframe
df = df[::-1]

# Create a list of the RPM values and a list of the MAP values
x = df.columns[1:]
y = df.iloc[:, 0]

# Reverse the order of the rows in the result dataframe
y = y[::-1]

# Create a 2D array of the Z values
z = df.iloc[:, 1:].values

# Define the colors for the surface plot
colormap = ['rgb(50, 0, 75)', 'rgb(200, 0, 200)', '#c8dcc8']
colorscale = [[0, colormap[0]], [0.5, colormap[1]], [1, colormap[2]]]

# Create the 3D surface plot with the defined colors
fig = go.Figure(data=[go.Surface(x=x, y=y, z=z, surfacecolor=z, colorscale=colorscale)])

# Add the wireframe trace
fig.add_trace(go.Scatter3d(
    x=x, y=[y[0]] * len(x), z=z[0],
    mode='lines',
    line=dict(color='black', width=1),
    showlegend=False
))
for i in range(1, len(y)):
    fig.add_trace(go.Scatter3d(
        x=x, y=[y[i]] * len(x), z=z[i],
        mode='lines',
        line=dict(color='black', width=1),
        showlegend=False
    ))
for i in range(len(x)):
    fig.add_trace(go.Scatter3d(
        x=[x[i]] * len(y), y=y, z=z[:, i],
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

# define the CSS style to apply
css_style = """
    body {
    font-family: Arial, sans-serif;
    background-color: white;
    margin: 0;
    padding: 0;
}

.header-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: left;
    text-align: left;
}

h1 {
    font-size: 6em;
    margin: 0;
}

h2 {
    font-size: 3em;
    margin: 0;
}

h3 {
    font-size: 2em;
    margin: 0;
}

p {
    font-size: 1em;
    margin: 0;
}

section {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

footer {
    background-color: #333;
    color: white;
    padding: 20px;
    text-align: left;
}
"""

# write the HTML file with the CSS style applied
pio.write_html(fig, file='veTable3dCorrected.html', config={
    'modeBarButtonsToRemove': ['toggleSpikelines'],
    'displayModeBar': True,
    'staticPlot': False,
    'editable': False,
    'style': {'type': 'text/css', 'props': {'children': css_style}}
})
