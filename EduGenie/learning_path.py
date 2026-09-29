from gemini_client import generate_text


def get_learning_recommendations(topic: str) -> str:
    prompt = f"""
You are EduGenie's learning-path module.
Create a personalized learning path for the topic below.
Organize it from beginner to advanced, and include suggested time ranges plus useful learning resources
such as videos, articles, documentation, or books. Keep recommendations practical and suitable for a learner.
If the learner's level is unknown, explicitly say that the path assumes beginner level and can be adjusted.

Topic:
{topic}
"""
    return generate_text(prompt)
