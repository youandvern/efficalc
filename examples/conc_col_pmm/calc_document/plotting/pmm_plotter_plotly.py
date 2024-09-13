import plotly.graph_objects as go
import numpy as np
from .pmm_mesh import get_mesh


def plot(col, intervals, load_spaces, load_cases):
    # This function plots the factored load capacity diagram for the column
    # col. "intervals" is the number of spaces in the angle of eccentricity,
    # "load_spaces" is the number of vertical spaces in the PMM diagram

    x, y, z, quarter_mesh = get_mesh(col, intervals, load_spaces)
    X = np.array(x)
    Y = np.array(y)
    Z = np.array(z)

    axis_colors = {"x": "#FF0000", "y": "#00CC00", "z": "#0000FF"}
    ax_labels = {"x": "${\phi}M_{nx}$", "y": "${\phi}M_{ny}$", "z": "${\phi}P_n$"}
    z_factor = 0.12
    xy_factor = 1.05

    data = {}
    # list for min, then max, then difference
    min_max = []
    for dir in (X, Y, Z):
        min_max.append([dir.min(), dir.max()])
    for i in range(3):
        min_max[i].append(min_max[i][1] - min_max[i][0])
    min1, max1 = min_max[2][:2]
    range1 = min_max[2][2]
    data["z"] = {}
    data["z"]["range"] = range1 * (1 + 2 * z_factor)
    data["z"]["min"] = min1 - range1 * z_factor
    data["z"]["max"] = max1 + range1 * z_factor

    min_aspect = 2
    max_xy = max(min_max[0][2], min_max[1][2])
    for i, dir in enumerate(("x", "y")):
        data[dir] = {}
        length = min(xy_factor * max_xy, min_aspect * min_max[i][2])
        data[dir]["range"] = length
        data[dir]["min"] = -length / 2
        data[dir]["max"] = length / 2

    def get_arrow(axisname="x"):
        ax_color = axis_colors[axisname]
        scale = [[0, ax_color], [1, ax_color]]
        # Create arrow body
        body = go.Scatter3d(
            marker=dict(size=1, color=ax_color),
            line=dict(color=ax_color, width=5),
            showlegend=False,  # hide the legend
            hoverinfo="skip",
        )

        head = go.Cone(
            sizemode="raw",
            sizeref=1,
            autocolorscale=None,
            colorscale=scale,
            showscale=False,  # disable additional colorscale for arrowheads
            hoverinfo="skip",
        )
        for ax, direction in zip(("x", "y", "z"), ("u", "v", "w")):
            if ax == axisname:
                body[ax] = data[ax]["min"], data[ax]["max"]
                head[ax] = [data[ax]["max"]]
                head[direction] = [0.05 * data[axisname]["range"]]
            else:
                body[ax] = 0, 0
                head[ax] = [0]
                head[direction] = [0]

        return [body, head]

    def add_axis_arrows(fig):
        for ax in ("x", "y", "z"):
            for item in get_arrow(ax):
                fig.add_trace(item)

    def get_annotation_for_ax(ax):
        d = dict(
            showarrow=False,
            text=ax_labels[ax],
            xanchor="left",
            font=dict(color="#1f1f1f", size=18),
        )
        for ax_ in ("x", "y", "z"):
            if ax_ == ax:
                d[ax_] = data[ax]["max"] - data[ax]["range"] * 0.025
            else:
                d[ax_] = 0

        if ax in {"x", "y"}:
            d["xshift"] = 12
        else:
            d["xshift"] = 2

        return d

    def get_axis_names():
        return [get_annotation_for_ax(ax) for ax in ("x", "y", "z")]

    def get_scene_axis():
        return dict(
            title="",  # remove axis label (x,y,z)
            showbackground=False,
            visible=False,
            showticklabels=False,  # hide numeric values of axes
            showgrid=False,  # Show box around plot
        )

    fig = go.Figure(
        layout=dict(
            title={
                "text": "PMM Diagram",
                "x": 0.5,
                "y": 0.98,
                "xanchor": "center",
                "yanchor": "top",
                "font": {"color": "#1f1f1f", "size": 18},
            },
            autosize=True,
            width=550,
            height=550,
            margin=dict(l=5, r=5, b=5, t=5),
            scene=dict(
                xaxis=get_scene_axis(),
                yaxis=get_scene_axis(),
                zaxis=get_scene_axis(),
                annotations=get_axis_names(),
                aspectmode="cube",
            ),
        ),
    )

    add_axis_arrows(fig)

    load_data = np.array(load_cases)

    """
    fig.add_trace(
        go.Scatter3d(
            showlegend=False,  # hide the legend
            x=load_data[:, 0],
            y=load_data[:, 1],
            z=load_data[:, 2],
            color="#001ccf",
            symbol="species",
        )
    )
    """

    surface_col = "#ffcc4c"
    surface_scale = [[0, surface_col], [1, surface_col]]
    fig.add_trace(
        go.Surface(
            z=Z,
            x=X,
            y=Y,
            opacity=0.9,
            colorscale=surface_scale,
            showscale=False,  # Set to True to show colorscale
            name="",
        )
    )

    line_color = "#f7f7f7"
    line_size = 1.5
    for i in range(X.shape[0]):
        fig.add_trace(
            go.Scatter3d(
                mode="lines",
                line=dict(color=line_color, width=line_size),
                showlegend=False,  # hide the legend
                x=X[i, :],
                y=Y[i, :],
                z=Z[i, :],
            )
        )
    for i in range(X.shape[1]):
        fig.add_trace(
            go.Scatter3d(
                mode="lines",
                line=dict(color=line_color, width=line_size),
                showlegend=False,  # hide the legend
                x=X[:-1, i],
                y=Y[:-1, i],
                z=Z[:-1, i],
            )
        )
    fig.update_yaxes(
        scaleanchor="x",
        scaleratio=1,
    )

    return quarter_mesh, fig
