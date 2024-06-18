from dash import dcc, get_asset_url
from dash import html
from constants import axis_labels
import dash_bootstrap_components as dbc
import openai

default_key = list(axis_labels.keys())[0]

graph_dropdown = dcc.Dropdown(
    id="graph-dropdown",
    className="dropdown",
    clearable=False,
    value=default_key,
    options=[{"label": axis_labels[k]["dropdown"], "value": k} for k in axis_labels.keys()],
    style={
        "width": "90%",
        "margin-top": "0px"
        #"box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 5px"
    }
)

graph_object = dcc.Graph(
            id="graph-object",
            config={"displayModeBar": False},
            style={
                "box-shadow": "rgba(0, 0, 0, 0.35) 0px 5px 15px",
                "width": "700px",
            }
)

deltay_header = html.H1(  # dynamic
    id="deltay-header"
)

info_header = html.P(  # dynamic
    id="info-header",
    children=axis_labels[default_key]["info"]
)

sliders = {}
for k in axis_labels.keys():
    sliders[k] = dcc.RangeSlider(
        id="{}-slider".format(k),
        step=10,
        allowCross=False,
        marks=None,
        min=axis_labels[k]["min_year"],
        max=axis_labels[k]["max_year"],
        value=[axis_labels[k]["min_year"], axis_labels[k]["max_year"]],
        tooltip={
            "placement": "top",
            "always_visible": True,
            "border_color": "#FFFFFF",
            "style": {
                "color": "white",
                "background_color": "#FFFFFF",
                "fontSize": "15px"
            }
        }
    )


datasource_links = {
    c: dcc.Link(axis_labels[c]["source"], href=axis_labels[c]["source"], id="{}-data-link".format(c)) for c in axis_labels.keys()
}

source_containers = {}
for k in axis_labels.keys():
    source_containers[k] = html.P(
            id="{}-source-container".format(k),
            children=["Source: ", datasource_links[k]],
            style={
                "font-size": "5px"
            }
        )
print(source_containers)

prompt_containers ={}
for k in axis_labels.keys():
    prompt_containers[k] = html.Div(
        html.P("Prompt: {}".format(k), id="{}-prompt-text".format(k)),
        id="{}-prompt-container".format(k)
    )

portfolio_link = dcc.Link("https://www.thomasbrewerprojects.com/", href="thomasbrewerprojects.com",id="portfolio-link")
portfolio_image = html.Img(src='assets/favicon.ico', id="logo-img", style={"width": "25px"})


