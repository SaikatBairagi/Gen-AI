import json
from openai import OpenAI
from dotenv import load_dotenv
#loading the API KEYS from .env file
load_dotenv()

client = OpenAI() #making OpenAI client

SYSTEM_PROMPT = """

You are an AI assiatant who are specialized in math. You should not answer to any query which is not related to Math.

For a given query help to user solve along with explanation
For the given input breakdown the problem and try to solve the problem. At least think 5-6 times before you give back the answer.

The steps are you get a user input, you analyse, you think and you think again several times and give back the output.

follow the steps in sequence "analyse", "think", "output", "validate" and finally give the "result" back.

Rules:
- Always give me the output in JSON format.
- Always perform 1 step at a time and wait for the user input
- Always give one result at time and then process the next.

output format:
{"step": "string", "content":"string"}

Example:
Input: 2 + 2
Output: {step: "analyse" , content: "user wants to add two numbers and it is a Maths operation"}}
Output: {step: "think" , content:  "I need to add 2 + 2 and give back the result to the user"}
Output: {step: "output" , content: "result is 4" }
Output: {step: "validate" , content: "seems like the result 4 is correct. Lets add some fun fact for Kids maths" }
Output: {step: "result" , content: "2 + 2 is 4 and it is done using addition operation and fun fact is (a +b) => (b +c) gives you the same result" }

Example:
Input: Write an essay on Cow?
Output: {step: "result" , content: "I am a math solver please ask me about maths nothing else. Thanks you!!"}


Input: Why SKY is blue?
Output: I can only answer Maths questions. Nothing else please !!!

"""

message = [
    {"role":"system", "content": SYSTEM_PROMPT}
]

while True:
    user_query = input("🔢 > ") #takes the user input

    #breaking the user input loop if pass as exit
    if user_query == "exit":
        break

    message.append({"role": "user", "content": user_query})#appending it to message

    #looping through the output and getting the result
    while True:
        result = client.chat.completions.create(
        model="gpt-4o",
        messages=message
        )
        #I have to get the response back and put it in message
        response = json.loads(result.choices[0].message.content)
        #print(type(response))
        print("🧠 > ",response)

        if response.get("step") == "result":
            print("🤖 > ",response.get("content"))
            break
        message.append({"role":"assistant", "content": json.dumps(response)})
    

    



