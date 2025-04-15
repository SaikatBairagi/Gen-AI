from openai import OpenAI
from dotenv import load_dotenv
import json
import requests
import os
import fnmatch

load_dotenv()

client = OpenAI()

def findFiles(command: str):
    print("🧰 ", command)
    matches = []
    for root, dirs, files in os.walk("."):
        for filename in files:
            if fnmatch.fnmatch(filename, "*Weather*"):
                matches.append(os.path.join(root, filename))
    return matches

def runCommands(command: str):
    print("🛠️ > ", command)
    result = os.system(command=command)
    print(f"result--> {result}")
    return result

def getWeatherInfoByCity( city: str):
    print(f"🛠️ calling with {city}")
    url = f"http://wttr.in/{city}?format=%C+%t"
    response = requests.get(url)
    
    if response.status_code == 200:
        return f"The weather of {city} is {response.text}"
    

available_tools = {
    "getWeatherInfoByCity":{
        "fn": getWeatherInfoByCity,
        "description": "this is a function that returns trmparature of a city"
    },
    "runCommands":{
        "fn": runCommands,
        "description": "this is a function that takes a command and runs that in operating system"
    },
    "findFiles":{
        "fn": findFiles,
        "description": "this is a function that takes a command and find the files that matches the name in this machine"
    }
}

SYSTEM_PROMPT = '''

You are an usuful AI agent who helps customer to resolve there queries.

For the given input try to breakdown the problem and try to resolve it.
The steps you will get a user input, you analyse, you think and you think again several times and give back the output. Based on the user input you will plan the next action and based on the action you call a function from tools and wait for the Observation. Based on the observation you return the output to the user

follow the steps in sequence "start", "plan", "think", "action", "observation" and finally give the "output" back.

Rules:
- Always give the output in JSON format.
- Always perform 1 step at a time and wait for the user input.
- Always try to understant the user query from all the perspective and resolve them.

available_tools:
- getWeatherInfoByCity : That takes a City as input and returns temperature of the place.
- runCommands : this is a function that takes a command and runs that in operating system.
- findFiles : this is a function that takes a command and find the files that matches the name in this machine.

output format:
{"step": "string", "content":"string", "function":"the name of the function if the step is function", "input":"the input param of the function"}

Example:
Input: What is the weather of Paris?
Output: {"step": "plan" , "content": "user wants to get the temparature of a city"}
Output: {"step": "think" , "content":  "To get that I need to first find out if the user provide me the City or I need to ask for it"}
Output: {"step": "plan" , "content": "from the available tools I need to call getWeatherInfoByCity function"}
Output: {"step": "action" , "function": getWeatherInfoByCity, "input": "Paris"}
Output: {"step": "observation" , "content": "the temperature is 12"}
Output: {"step": "output" , "content": "the temperature of Paris is 12"}



'''

message = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_input = input("> ")
    if user_input == "exit":
        break
    message.append({"role": "user", "content": user_input})

    while True:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages= message
        )

        response_message = json.loads(response.choices[0].message.content)
        print("🧠 ",response_message)

        # initiate the tool calling by looking up the available_tools dict
        if(response_message.get("step") == "action"):
            tool = response_message.get("function")
            city = response_message.get("input")

            if available_tools.get(tool):
                output = available_tools[tool].get("fn")(city)
                print("🛠️ >", output)
                message.append({"role":"assistant", "content": json.dumps({"step": "observation" , "content": output})})

        #printing the output of the final result
        if(response_message.get("step") == "output"):
            print("🤖 ",response_message.get("content"))
            break
        message.append({"role": "assistant", "content": json.dumps(response_message)})


