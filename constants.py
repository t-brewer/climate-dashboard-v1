def file_reader(path):
    with open(path) as f:
        s = f.read()
    return s

# Labels / Marks for RangeSliders
co2_marks = {str(x): {"label": str(x)} for x in [1750, 2022]}
temp_anomaly_marks = {str(x) : {"label": str(x)} for x in [1850, 2022]}
sea_level_marks = { str(x) : {"label": str(x)} for x in [1880, 2020]}

data_dir = "./assets/data"

# Dicitionary of figure choices specific to the chosen data.
axis_labels = {
    "co2":{
        "data": data_dir + "/annual-co2-emissions-per-country.csv",
        "title": "Carbon Emissions",
        "axis": "CO2 emissions (tonnes)",
        "marks": co2_marks,
        "min_year": 1850,
        "max_year": 2022,
        "dropdown": "Global CO2 Emissions",
        "info": file_reader("./assets/data/opening_text.txt"),
        "graph_type": "line",
        "first_prompt": "In 100 words, tell me something about carbon emission and how data "
                        "can be useful in the context of climate change.",
        "something_else_prompt": "Tell me something else about CO2 emissions.",
        "prompt_display": "Tell me about climate change and data.",
        "source": "https://ourworldindata.org/co2-dataset-sources"
    },
    "anomaly":{
        "data": data_dir + "/global-land-ocean-average-temperature-anomaly.csv",
        "title": "Global Land and Ocean December Average Temperature Anomalies",
        "axis": "\u0394 T (C)",
        "marks": temp_anomaly_marks,
        "min_year": 1850,
        "max_year": 2023,
        "dropdown": "GLO Temperature Anomaly",
        "info": file_reader("./assets/data/opening_text.txt"),
        "graph_type": "bar",
        "color_flag": lambda x: x > 0,
        "first_prompt": "In 100 words, tell me something about rising average global temperature "
                        "and how data can be useful in mitigating this aspect of climate change.",
        "prompt_display": "Tell me about climate change and data",
        "source": "https://ourworldindata.org/grapher/temperature-anomaly"
    },
    "sea_level":{
        "data": data_dir + "/sea-level.csv",
        "title": "Global Average Seal Rise",
        "axis" : "\u0394 H (meters)",
        "marks": sea_level_marks,
        "min_year": 1880,
        "max_year": 2020,
        "dropdown": "Global Sea Level",
        "info": file_reader("./assets/data/opening_text.txt"),
        "graph_type": "bar",
        "first_prompt": "In 100 words, tell me something about rising sea levels and "
                        "how data can be useful in mitigating this aspect of climate change.",
        "prompt_display": "Tell me about climate change and data.",
        "source": "https://ourworldindata.org/grapher/sea-level"
    }
}

