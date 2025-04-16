from openai import OpenAI
from dotenv import load_dotenv
import json
import subprocess
import os
import shutil

load_dotenv()

model = OpenAI()

#functions goes here
def create_react_project(project_name):
    try:
        # Remove if already exists (optional cleanup)
        if os.path.exists(project_name):
            print(f"Cleaning up existing directory '{project_name}'...")
            shutil.rmtree(project_name)

        # Run the create-react-app command
        print(f"Creating React app '{project_name}'...")
        result = subprocess.run(
            ['npx', 'create-react-app', project_name],
            check=True,
            text=True,
            capture_output=True
        )

        # Validate success by checking folder and key files
        expected_files = ['package.json', 'src', 'public']
        project_path = os.path.join(os.getcwd(), project_name)
        is_valid = all(os.path.exists(os.path.join(project_path, f)) for f in expected_files)

        if is_valid:
            print(f"✅ React app '{project_name}' created successfully.")
            return "Project created Successful"
        else:
            print(f"⚠️ React app '{project_name}' creation might be incomplete.")
            return "Failed to create"

    except subprocess.CalledProcessError as e:
        print("❌ Error while creating React app:")
        print(e.stderr)
        return "Failed to create"
    except Exception as ex:
        print(f"❌ Unexpected error: {ex}")
        return "Failed to create"

def start_react_app(app_name):
    try:
        app_path = os.path.abspath(app_name)

        if not os.path.isdir(app_path):
            print(f"❌ Directory '{app_name}' does not exist.")
            return False

        # Change working directory to the app folder
        os.chdir(app_path)
        print(f"📂 Changed directory to: {app_path}")

        print("🚀 Starting the React app (npm start)...")

        # Start the React app using subprocess and stream output
        process = subprocess.Popen(
            ['npm', 'start'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Print logs as the server runs
        for line in process.stdout:
            print(line, end='')  # line already includes newline

        process.wait()
        print(f"✅ React app '{app_name}' exited with code {process.returncode}")
        return process.returncode == 0

    except Exception as e:
        print(f"❌ Error starting React app: {e}")
        return False 

#setting up available tools
available_tools = {
    "create_react_project":{
        "fn": create_react_project,
        "description": "this is a function that creates a react project by taking one parameter as project name"
    },
    "start_react_app":{
        "fn": start_react_app,
        "description": "this is a function that takes a command and runs that in operating system"
    }
}


#system prompt goes here
SYSTEM_PROMPT = '''
You are an Helpful AI ssistant to create a React project template with files in it.
Always ask user to provide the Project name they want to create and invoke the function.

follow the steps in sequence "start", "plan", "think", "action", "observation" and finally give the "output" back.

Rules:
- Always give the output in JSON format.
- Always perform 1 step at a time and wait for the user input.
- Always try to understant the user query from all the perspective and resolve them. If needed you can ask more question.

Tools:
- create_react_project : this will take a project name as input and create the react app
- start_react_app :  this is a function that takes a command and runs that in operating system

Example:

Input: Can you please create a react app.
Output: {"step": "think" , "content": "ok I can create it. Use my-react-app as project name if no name provided"}
Output: {"step": "think" , "content": "If you ask for the project and user did not give any input you be creative and you can choose the project name but all in lower case and think user has concent on that"}
Output: {"step": "plan" , "content": "I need to crate the app and install the dependency too to create the project I need to call
create_react_project from the tools"}
Output: {"step": "action" , "function": create_react_project, "input": "my-react-app"}
Output: {"step": "observe" , "content": "Project created Successful"}
Output: {"step": "plan" , "content": "if Project is crated Successfully in observe stage then call the start_react_app function to start the project else go to output state for failure"}
Output: {"step": "action" , "function": start_react_app, "input": "my-react-app"}
Output: {"step": "output" , "content": "project is started succesfully"}


'''

#OpenAI code goes here

message = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

while True:
    user_ip = input("> ")
    if(user_ip == "exit"):
        break
    message.append({"role":"user", "content":user_ip})

    while True:
        response = model.chat.completions.create(
            model="gpt-4o",
            messages= message
        )

        print(f"🧠 {response.choices[0].message.content}")

        response_dict = json.loads(response.choices[0].message.content)

        if(response_dict.get("step") == "action"):
            func = response_dict.get("function")
            param = response_dict.get("input")

            if available_tools.get(func):
                output = available_tools[func].get("fn")(param)
                print("🛠️ >", output)
                print("I put back the message -->",json.dumps({"step": "observation" , "content": output}))
                message.append({"role":"assistant", "content": json.dumps({"step": "observation" , "content": output})})

        if(response_dict.get("step") == "output"):
            print(f"🤖 {response_dict.get('content')}")
            break
        message.append({"role":"assistant", "content": json.dumps(response_dict)})

