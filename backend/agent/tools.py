TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "get_completed_courses",
            "description": "Get the list of courses a student has already completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "The student's unique ID"
                    }
                },
                "required": ["user_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_graduation_requirements",
            "description": "Get the courses a student needs to graduate given their major and catalog year",
            "parameters": {
                "type": "object",
                "properties": {
                    "major": {
                        "type": "string",
                        "description": "The student's major e.g. Computer Science"
                    },
                    "catalog_year": {
                        "type": "string",
                        "description": "The year the student enrolled e.g. 2023"
                    }
                },
                "required": ["major", "catalog_year"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_available_courses",
            "description": "Get available courses for a given semester filtered by what the student has already completed",
            "parameters": {
                "type": "object",
                "properties": {
                    "semester": {
                        "type": "string",
                        "description": "The upcoming semester e.g. Fall 2026"
                    }
                },
                "required": ["semester"]
            }
        }
    }
]

def get_completed_courses(user_id):
    return [
        {"code": "EECS 280", "name": "Programming and Data Structures", "credits": 4},
        {"code": "MATH 214", "name": "Linear Algebra", "credits": 4},
        {"code": "EECS 203", "name": "Discrete Math", "credits": 4},
    ]

def get_graduation_requirements(major, catalog_year):
    return {
        "required": [
            {"code": "EECS 281", "name": "Data Structures and Algorithms", "credits": 4},
            {"code": "EECS 370", "name": "Computer Organization", "credits": 4},
            {"code": "EECS 376", "name": "Foundations of Computer Science", "credits": 4},
            {"code": "EECS 485", "name": "Web Systems", "credits": 4},
        ],
        "total_credits_required": 128,
        "credits_completed": 12
    }

def get_available_courses(semester, user_id):
    completed_codes = [c["code"] for c in get_completed_courses(user_id)]
    all_courses = [
        {"code": "EECS 281", "name": "Data Structures and Algorithms", "credits": 4, "prerequisites": ["EECS 280"], "rating": 4.2, "difficulty": "hard"},
        {"code": "EECS 370", "name": "Computer Organization", "credits": 4, "prerequisites": ["EECS 280"], "rating": 3.8, "difficulty": "medium"},
        {"code": "EECS 485", "name": "Web Systems", "credits": 4, "prerequisites": ["EECS 281"], "rating": 4.5, "difficulty": "medium"},
        {"code": "MATH 425", "name": "Statistics", "credits": 3, "prerequisites": ["MATH 214"], "rating": 3.9, "difficulty": "medium"},
    ]
    return [c for c in all_courses if c["code"] not in completed_codes]