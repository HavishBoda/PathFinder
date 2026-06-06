from groq import Groq
from dotenv import load_dotenv
import os
from tools import TOOL_DEFINITIONS, get_available_courses, get_completed_courses, get_graduation_requirements
import json
from db.sqlite import init_db, get_user, save_user, get_recent_sessions, save_session

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tool_map = {
    "get_completed_courses": get_completed_courses,
    "get_graduation_requirements": get_graduation_requirements,
    "get_available_courses": get_available_courses,
}

def run_agent(message, user_profile, user_id):
    init_db()
    user = get_user(user_id)
    if user is None:
        save_user(user_id, user_profile)
    
    system_prompt = f"""You are an academic advising agent helping a University of Michigan student plan their courses.

Student profile:
- Major: {user_profile['major']}
- Catalog year: {user_profile['catalog_year']}
- Target graduation: {user_profile['target_graduation']}
- Completed courses: {user_profile['completed_courses']}

Your job is to help them figure out what to take next, check graduation requirements, and make a realistic multi-semester plan. Always use your tools to look up real data before making recommendations."""
    
    user_dict = get_user(user_id)
    session_history = get_recent_sessions(user_id, 3)
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message},
    ]

    messages.append(session_history)

    while True:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages = messages,
            tools = TOOL_DEFINITIONS
        )
        if response.choices[0].finish_reason == "tool_calls":
            func = response.choices[0].message.tool_calls[0].function.name
            args = response.choices[0].message.tool_calls[0].function.arguments
            args = json.loads(args)
            if func == "get_available_courses":
                args["user_id"] = "default"
            result = tool_map[func](**args)
            print(f"\n🔧 Calling tool: {func}")
            print(f"   Args: {args}")
            print(f"   Result: {result}\n")
            messages.append(response.choices[0].message)
            messages.append({
                "role": "tool",
                "tool_call_id": response.choices[0].message.tool_calls[0].id,
                "content": json.dumps(result)
            })
        elif response.choices[0].finish_reason == "stop":
            print("\n💬 Final answer:")
            print(response.choices[0].message.content)
            return response.choices[0].message
            
if __name__ == "__main__":
    test_profile = {
        "major": "Computer Science",
        "catalog_year": "2023",
        "target_graduation": "Winter 2027",
        "completed_courses": [
            {"code": "EECS 280", "name": "Programming and Data Structures", "credits": 4},
            {"code": "MATH 214", "name": "Linear Algebra", "credits": 4},
        ]
    }
    result = run_agent(
        "What courses should I take in Fall 2026?",
        test_profile,
        "havish_001"
    )
    print(result)