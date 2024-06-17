from constants import axis_labels
from numpy import random
from openai import OpenAI


roles = {
    "academic": "You are an optimistic academic who knows a lot about climate change."
}


# Some structures to use.
base = "In 50 words:"
objects = {
    "co2": "co2 emissions",
    "anomaly": "rising average global land and sea temperature",
    "sea_level": "rising sea levels"
}
subjects = ["the natural world", "our daily lives", "the economy", "politics"]

prompts = {}
for k in objects.keys():
    prompts[k] = []
    for s in subjects:
        prompts[k].append(base + "Tell me about the impacts of {} on {}". format(objects[k], s))

# Handwritten prompts :
prompts["co2"].extend([
    base + "ways to reduce our CO2 emissions in our daily lives.",
    base + "the complexities of the climate crisis.",
    base + "ways policy can affect our carbon footprint.",
    base + "the history of carbon emissions."
])

prompts["anomaly"].extend([
    base + "the correlation between rising global temperatures and extreme weather events.",
    base + "the correlation between rising global temperatures and rising sea levels.",
    base + "how we could adapt to more frequent extreme weather events."
])

prompts["sea_level"].extend([
    base + "the relation between the oceans El Nino and climate predictions.",
    base + "what the thermohaline circulation is, its importance, and how it is affected by climate change."
])

def get_prompt(key): # do it as a function here to not have it be loaded all the time,
    # Look up which state we are in (co2/temp/sea_level)
    # construct the list of prompts
    # choose one at random.
    return random.choice(prompts[key])


def promptGPT(client, prompt,system_content="default", model="gpt-3.5-turbo"):
    default = "You are an optimistic teacher capable of explaining the facts of climate change while inspiring hope."
    roles = {
        "peasant": "You are a medieval peasant who does not know anything about climate change.",
        "hunter-gatherer": "You are a hunter gatherer from present day Africa.",
        "business" : "You are a skilled small business owner asking what they can do."
    }
    system = default if system_content=="default" else system_content
    system = roles["business"]
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system",
             "content": system},
            {"role": "user", "content": prompt}
        ]
    )
    return completion

def tell_me_more(client, message):
    _prompt = "In 100 words, tell me more about: {}".format(message)
    completion = promptGPT(client, _prompt)
    return completion





