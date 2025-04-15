import json

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


system_prompt = """

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


Input: Why SKY is blue?
Output: I can only answer Maths questions. Nothing else please !!!

"""

result = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content":system_prompt},
        {"role": "user", "content": " What is 2 +2 * 0?"},
        {"role": "assistant", "content": json.dumps({"step": "analyse", "content": "user requests for the evaluation of an expression with addition and multiplication operations."})},
        {"role": "assistant", "content": json.dumps({"step": "think", "content": "The expression follows the order of operations, commonly known as BIDMAS/BODMAS (Brackets, Orders, Division and Multiplication, Addition and Subtraction)."})},
        {"role": "assistant", "content": json.dumps({"step": "output", "content": "According to the order of operations, we first perform the multiplication: 2 * 0 = 0."})},
        {"role": "assistant", "content": json.dumps({"step": "validate" , "content": "The multiplication 2 * 0 results in 0. Now we need to continue by adding 2 + 0."})}
    ]
)

print(f"🤖 {result.choices[0].message.content}")