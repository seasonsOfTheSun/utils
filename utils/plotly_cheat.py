import plotly.graph_objects
import numppy as np


def three_d_scatter(x,y,z,labels,colormap=None,
                          xaxis_title='xaxis_title',
                          yaxis_title='yaxis_title',
                          zaxis_title='zaxis_title',
                          legend_title='legend_title',
                          font_family='Arial',
                          font_size=10,
                          plot_title='plot_title'):

    fig = plotly.graph_objects.Figure()

    if colormap == None:
        colormap = {}
        for i in np.unique(labels):
            colormap[i] = np.random.rand(size=(3,))



    for label, color in colormap.items():
      # split color class by color class because the legend won't be created correctly otherwise
      fig.add_trace(plotly.graph_objects.Scatter3d(x=x[labels==label],y=y[labels==label],z=z[labels==label],
                                                mode='markers',
                                                  marker=dict(
                                                      size=16,
                                                      line = {"color": "#000000", "width":10},
                                                      color=color
                                                  ),
                                                   name=label))


    fig.update_layout(
        title=plot_title,
        # axis titles areset through the scene object for 3d plots
        scene = dict(
                        xaxis_title=xaxis_title,
                        yaxis_title=yaxis_title,
                        zaxis_title=zaxis_title),
        legend_title=legend_title,
        font=dict(
            family=font_family,
            size=font_size
        ))


