
import os
import google.generativeai as genai
import json
from typing import Optional

def _generate_json_response(prompt: str) -> dict:
    """
    A helper function to send a prompt to the Gemini API and get a JSON response.

    Args:
        prompt: The prompt to send to the model.

    Returns:
        A dictionary parsed from the JSON response, or an empty dictionary on failure.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("⚠️ [bold yellow]警告: 未设置 GEMINI_API_KEY 环境变量。将跳过 AI 分析。[/bold yellow]")
        return {}

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    response = model.generate_content(prompt)

    # Clean the response text to ensure it's valid JSON
    cleaned_response_text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    
    analysis = json.loads(cleaned_response_text)
    return analysis


def get_llm_analysis(task_description: str, project: Optional[str], tag: Optional[str]) -> dict:
    """
    Analyzes a task description using the Gemini API to provide advice,
    and rate its importance and urgency.

    Args:
        task_description: The description of the task.
        project: The project the task belongs to.
        tag: The tag associated with the task.

    Returns:
        A dictionary containing the advice, importance, and urgency,
        or an empty dictionary if the API call fails.
    """
    try:
        context_str = ""
        if project:
            context_str += f"\n所属项目 (Project): {project}"
        if tag:
            context_str += f"\n相关标签 (Tag): {tag}"

        prompt = f"""
        你是一个专业的效率教练，请根据时间管理理论（例如艾森豪威尔矩阵），分析以下任务并提供建议。
        请结合任务的上下文（如下面的项目和标签信息）进行综合评估。
        请为任务评估一个“重要性”分数（1-10分）和一个“紧迫性”分数（1-10分）。
        - **重要性 (Importance)**：衡量任务对长期目标、个人价值或重大成果的贡献程度。高分表示任务对你的目标至关重要，低分表示任务相对不那么关键。
        - **紧迫性 (Urgency)**：衡量任务需要立即处理的程度，是否有明确的截止日期或延迟的后果。高分表示任务需要立即关注，低分表示任务可以稍后安排。
        
        请以 JSON 对象格式返回响应，包含 "advice"（建议）、"importance"（重要性分数）和 "urgency"（紧迫性分数）三个键。
        
        例如：{{ "advice": "这是一个重要的任务，建议立即开始。", "importance": 9, "urgency": 8 }}

        任务描述 (Task): "{task_description}"{context_str}
        """
        return _generate_json_response(prompt)

    except Exception as e:
        # Handle potential exceptions during the API call or JSON parsing
        print(f"An error occurred during LLM analysis: {e}")
        return {}

def get_encouragement_for_task(task: dict) -> str:
    """
    Generates a personalized and encouraging message for a specific task using the Gemini API.

    Args:
        task: The task to get encouragement for. It should be a dictionary
              containing 'description', 'importance', and 'urgency'.

    Returns:
        A string containing the encouragement message, or an empty string if the API call fails.
    """
    try:
        prompt = f"""
        The user's next task is: '{task['description']}'.
        The task has an importance of {task.get('importance', 'N/A')}/10 and an urgency of {task.get('urgency', 'N/A')}/10.
        Write a short, personalized, and encouraging message to the user to motivate them to start this task.
        Keep it concise and positive. Address the user directly.
        Return the response as a JSON object with a single key "encouragement".
        """
        response_data = _generate_json_response(prompt)
        return response_data.get("encouragement", "")

    except Exception as e:
        print(f"An error occurred during LLM encouragement generation: {e}")
        return ""

def get_overall_analysis(tasks: list) -> str:
    """
    Generates an overall analysis of the entire task list using the Gemini API.

    Args:
        tasks: A list of task dictionaries.

    Returns:
        A string containing the AI-powered analysis, or an empty string on failure.
    """
    try:
        # Format the task list for the prompt
        task_descriptions = [f"- {task['description']}" for task in tasks]
        formatted_tasks = "\n".join(task_descriptions)

        prompt = f"""
        You are a friendly and insightful productivity coach. Below is the user's current to-do list.
        Please analyze it and provide a brief, encouraging summary.
        Identify any common themes (e.g., "I see a lot of work-related tasks"), potential challenges, and offer one or two high-level suggestions for how to approach the day.
        Keep the tone positive and supportive. Address the user directly.

        Here is the to-do list:
        {formatted_tasks}

        Return your analysis as a JSON object with a single key "summary".
        """
        response_data = _generate_json_response(prompt)
        return response_data.get("summary", "")
    except Exception as e:
        print(f"An error occurred during LLM overall analysis: {e}")
        return ""
