import pandas as pd
import plotly.express as px

# read csv file into pandas dataframe
df = pd.read_csv('../outputs/veTableRefPct.csv')

# set the first column as the index
df.set_index(df.columns[0], inplace=True)

# Reverse the order of the rows in the result dataframe
df = df[::-1]

# create the heatmap
fig = px.imshow(df, x=df.columns, y=df.index, text_auto=True)

# Set heatmap color scale
fig.update_layout(
    title={
        'text': 'VE Table Refinement %',
        'font': {'size': 12, 'color': 'grey', 'family': 'Arial'},
        # 'x': 0.5,
        # 'y': 0.95,
        'xanchor': 'left',
        'yanchor': 'top'
    },
    xaxis=dict(title={
            'text': 'RPM',
            'font': {'size': 10, 'color': 'grey', 'family': 'Arial'}
        },
        tickfont=dict(color='grey', size=10, family='Arial')),
    yaxis=dict(title={
            'text': 'Manifold Pressure',
            'font': {'size': 10, 'color': 'grey', 'family': 'Arial'}
        },
        tickfont=dict(color='grey', size=10, family='Arial')),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='grey'),
    margin=dict(l=50, r=50, t=50, b=50),
    hovermode='closest',
    coloraxis_colorbar=dict(
        title={
            'text': 'Variance %',
            'font': {'size': 10, 'color': 'Grey', 'family': 'Arial'}
        },
        x=1,
        xpad=0,
        len=0.4,
        y=0.5,
        ypad=0,
        thickness=15,
        tickfont=dict(color='grey', size=10, family='Arial')
    ),
    coloraxis=dict(
        colorscale='Viridis',
        showscale=True,
        colorbar_thickness=25,
        colorbar_ticklen=3,
        colorbar_tickfont=dict(color='grey', size=10, family='Arial'),
        colorbar_title_side='right',
        colorbar_title_font=dict(color='grey', size=10, family='Arial')
    )
)

# show the plot
fig.show()
