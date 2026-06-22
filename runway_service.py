import os
from runwayml import RunwayML

def get_runway_client():
    api_key = os.environ.get("RUNWAYML_API_KEY")
    if not api_key:
        return None
    return RunwayML(api_key=api_key)

def generate_video(prompt):
    client = get_runway_client()
    if not client:
        return {"error": "RunwayML not configured"}

    try:
        # Using RunwayML Gen-3 Alpha by default
        # Note: Actual SDK methods may vary based on version
        task = client.tasks.create(
            model="gen3a_turbo",
            prompt_text=prompt
        )
        return {"status": "success", "task_id": task.id, "message": "Video generation task created"}
    except Exception as e:
        return {"error": str(e)}

def get_task_status(task_id):
    client = get_runway_client()
    if not client:
        return {"error": "RunwayML not configured"}

    try:
        task = client.tasks.get(task_id)
        return {"status": "success", "task_status": task.status, "url": getattr(task, 'url', None)}
    except Exception as e:
        return {"error": str(e)}
