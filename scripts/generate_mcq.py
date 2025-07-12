# 简答题改为选择题的prompt
def generate_mcq_prompt(question: str, answer: str) -> dict:
    return  f"""
You are an expert at creating multiple-choice questions. Your task is to convert the given question and answer into a well-structured multiple-choice question.

**Instructions:**
- Rewrite the given question into a multiple-choice format.
- Ensure the question requires **genuine reasoning** rather than simple recall or memorization.
- Do **not reduce the original difficulty** of the question.
- Provide at least **four answer options, but more are allowed if needed**.
- Ensure **only one correct answer** is present.
- Make the incorrect options plausible but clearly incorrect.
- Return the question and options in with the correct answer explicitly marked.

**Input:**
Question: "{question}"
Answer: "{answer}"

**Output Format:**
{{
    "question": "Your rewritten multiple-choice question that requires reasoning",
    "options": {{
        "A": "Option A",
        "B": "Option B",
        "C": "Option C",
        "D": "Option D",
        "E": "Option E",  # Optional extra options
        "F": "Option F"   # Optional extra options
    }},
    "correct_answer": "A"  # The correct option letter
}}

Now, generate the multiple-choice question while ensuring it requires reasoning.
        """.strip()

# generate_mcq_prompt(data_json[102220]['prompt'],data_json[102220]['gold_standard_solution'])