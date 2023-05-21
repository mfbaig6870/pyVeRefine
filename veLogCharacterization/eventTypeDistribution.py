import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html

# Read the CSV file into a DataFrame
df = pd.read_csv('../outputs/logCharacterization.csv')

# Fill null values in event_type column with a specific value (e.g., "Unknown")
df['event_type'].fillna('Unknown', inplace=True)

# Calculate the event_type counts
event_counts = df['event_type'].value_counts()

# Create the Plotly donut chart
fig = go.Figure(data=[go.Pie(labels=event_counts.index, values=event_counts.values, hole=0.5)])

# Define the chart properties
fig.update_layout(
    title='Event Type Counts',
    showlegend=True,
    legend=dict(
        title='Event Type',
        yanchor='bottom',
        y=0.1,
        xanchor='right',
        x=0.1,
    ),
    width=700,
    height=500,
)

# Create the Dash app
app = Dash(__name__)

# Define the layout
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
