import dash
from dash import dcc, ctx
from dash import html
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
from data_processing import get_data, get_delta
from constants import axis_labels
from components import *
from openai import OpenAI
from prompt_builder import get_prompt, promptGPT
from numpy import random
import time

useGPT = True

# -----Preamble / Starting Values ------
external_stylesheets = [dbc.themes.BOOTSTRAP]
data = get_data()  # Can merge other data that is classified by year.
fig = px.line(
    data,
    x="year",
    y=["co2"]
)
graph_object.figure = fig
#deltay_val = get_delta(data, "co2", axis_labels["co2"]["min_year"],
#                      axis_labels["co2"]["max_year"])
#deltay_header.children = "\u0394 M_CO2 = {}".format(deltay_val)
# todo how to make super/subscripts in display text.

with open("assets/data/opening_text.txt", "r") as f:
    default_message = f.read()


# ChatGPT, only do CO2 to minimize prompting
# with open(".env/open-ai-key") as f:
#     api_key = f.read()

if useGPT:
    gpt_client = OpenAI()
    completion = promptGPT(gpt_client, axis_labels["co2"]["first_prompt"])
    message = completion.choices[0].message.content
else:
    message = default_message

axis_labels["co2"]["message"] = message

info_header.children=message



# Start the App
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "climate-dashboard"
server = app.server

# App Layout
app.layout = html.Div(
    id="app",
    children=[
        dbc.Row(
            [
                dbc.Col(
                    dbc.Stack(
                        [
                            html.Div(graph_object, id="graph-container"),
                            *[html.Div(sliders[k], id="{}-slider-container".format(k)) for k in axis_labels.keys()]
                        ],
                        id="first-column-stack",
                        gap=0),
                    id="first-column",
                ),
                dbc.Col(
                    dbc.Stack(
                        [
                            html.Div(graph_dropdown, id="dropdown-container"),
                            *[prompt_containers[k] for k in axis_labels.keys()],
                            info_header,
                            dbc.Button("Tell me more", id="tmm-btn", n_clicks=0, className="me-1"),
                            dbc.Button("Tell me something else", id="tmse-btn", n_clicks=0, className="me-1") # dn_clicks is what triggers
                        ],
                        id="second-column-stack",
                        gap=1
                    ),
                    id="second-column"
                )
            ],
            id="first-row"
        ),
        dbc.Row(
            [
                dbc.Col([source_containers[k] for k in axis_labels.keys()]),
                dbc.Col(
                    html.Div(portfolio_link), style={"text-align": "right",
                                                     "margin-right": "5px"}),
                    html.Div(portfolio_image, style={"width": "50px", "margin-right": "10px"})
            ],
            id="third-row",
            style={
                "margin-top": "20px"
            }
        )
    ]
)


@app.callback(
    output=[
        Output('tmm-btn', "disabled", allow_duplicate=True),
        Output("tmse-btn", "disabled", allow_duplicate=True)
    ],
    inputs=[
        Input("tmm-btn", "n_clicks"),
        Input("tmse-btn", "n_clicks"),
    ],
    prevent_initial_call=True
)
def disable_buttons(*args):  # Disables the buttons on click to make sure we don't query GPT multiple times.
    '''
    Disables the buttons on click to make sure we don't query GPT multiple times, they re-enabled by the
    querying function.
    '''
    return True, True


# First Dropdown Change OR Button Click --> Update info-header text
@app.callback(
    output=[
        Output("info-header","children"),
        Output("tmm-btn", "disabled"),
        Output("tmse-btn", "disabled"),
        *[Output("{}-prompt-text".format(k), "children") for k in axis_labels.keys()]
    ],
    inputs=[
        State("graph-dropdown", "value"),
        State("info-header", "children"),
        Input("tmm-btn", "n_clicks"),
        Input("tmse-btn", "n_clicks"),
    ],
    prevent_initial_call=True
)
def update_text(yaxis, current_text, *args):
    triggered_id = ctx.triggered_id
    print("triggered_id", triggered_id)

    if useGPT:
        if triggered_id == "tmm-btn":
            prompt = "In 100 words, tell me more about: {}".format(current_text)
            prompt_display = "Prompt: Tell me more!"

        else:
            prompt = get_prompt(yaxis)
            prompt_display = prompt
        message = promptGPT(gpt_client, prompt)
        message = message.choices[0].message.content

    else:
        time.sleep(0.1)
        message = "ChatGPT is turned off. Here is a random number to show change: {}".format(random.randint(1000))
        prompt = "Prompt: ChatGPT is turned off."
        prompt_display = prompt

    print(prompt)

    axis_labels[yaxis]["prompt"] = prompt
    axis_labels[yaxis]["prompt_display"] = prompt_display
    axis_labels[yaxis]["message"] = message

    return message, False, False, *[axis_labels[k]["prompt_display"] for k in axis_labels.keys()]

@app.callback(  # Dropdown OR Slider Change
    output=[Output("graph-object", "figure")],
            #Output(deltay_header.id, "children")],
    inputs=[
        Input("graph-dropdown", "value"),
        Input(sliders["co2"], "value"),
        Input(sliders["anomaly"], "value"),
        Input(sliders["sea_level"], "value"),
    ]
)
def update_chart(*args):
    #  Dropdown change => Reset Graph
    yaxis = args[0]
    slider_values = {
        "co2": args[1],
        "anomaly": args[2],
        "sea_level": args[3]
    }

    start_year, end_year = slider_values[yaxis]
    filtered_data = data.loc[(data.year >= start_year) & (data.year <= end_year)]
    x = "year"
    y = [yaxis]

    if "color_flag" in axis_labels[yaxis].keys():
        color_mapper = axis_labels[yaxis]["color_flag"]
    else:
        color_mapper = None

    # Create a plotly plot for use by dcc.Graph().
    if axis_labels[yaxis]["graph_type"] == "line":
        fig = px.line(
            filtered_data,
            x=x,
            y=y
        )
    else:
        if color_mapper is not None:
            fig = px.bar(
                filtered_data,
                x=x,
                y=y,
                color=filtered_data[yaxis].apply(color_mapper).values
            )
        else:
            fig = px.bar(
                filtered_data,
                x=x,
                y=y
            )
    fig.update_layout(
        template="plotly_white",
        #title=yaxis if yaxis not in axis_labels.keys() else axis_labels[yaxis]["title"],
        xaxis_title="Year",
        yaxis_title=yaxis if yaxis not in axis_labels.keys() else axis_labels[yaxis]["axis"],
        showlegend=False,
        font=dict(
            family="Verdana, sans-serif",
            size=18,
            color="black"
        )
    )

    # Get Delta Y
    # year_min, year_max = slider_values[yaxis]
    # dy = round(get_delta(data, yaxis, year_min, year_max))
    # print("year min", year_min, "year_max", year_max, "dy", dy)
    #
    # display = "\u0394 {} = {} {}".format(yaxis, dy, "unit")
    # print("display", display)



    return [fig]#, display



@app.callback(
    output=[
        *[Output("{}-slider-container".format(k), "style") for k in axis_labels.keys()],
        *[Output("{}-source-container".format(k), "style") for k in axis_labels.keys()],
        *[Output("{}-prompt-container".format(k), "style") for k in axis_labels.keys()]
    ],
    inputs=[Input(component_id='graph-dropdown', component_property='value')]
)
def show_hide_element(yaxis):
    outputs = []
    for o in dash.callback_context.outputs_list:
        key = o["id"].split('-')[0]
        value = {"display": 'block' if yaxis == key else "none"}
        outputs.append(value)

    return outputs



if __name__ == "__main__":
    app.run_server(dev_tools_props_check=False)
