import os
from elevenlabs.client import ElevenLabs

def get_elevenlabs_client():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        return None
    return ElevenLabs(api_key=api_key)

def text_to_speech(text, voice_id="21m00Tcm4TlvDq8ikWAM"):
    client = get_elevenlabs_client()
    if not client:
        return {"error": "ElevenLabs not configured"}

    try:
        audio = client.generate(
            text=text,
            voice=voice_id,
            model="eleven_monolingual_v1"
        )

        # Save audio to a temporary file in the uploads directory
        import uuid
        filename = f"tts_{uuid.uuid4().hex}.mp3"
        upload_folder = 'uploads'
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filepath = os.path.join(upload_folder, filename)

        # ElevenLabs generate() returns a generator of bytes
        with open(filepath, "wb") as f:
            for chunk in audio:
                if chunk:
                    f.write(chunk)

        return {
            "status": "success",
            "message": "Audio generated successfully",
            "filename": filename,
            "filepath": filepath
        }
    except Exception as e:
        return {"error": str(e)}

def get_voices():
    client = get_elevenlabs_client()
    if not client:
        return {"error": "ElevenLabs not configured"}
    try:
        voices_response = client.voices.get_all()
        voices = [{"id": v.voice_id, "name": v.name} for v in voices_response.voices]
        return {"status": "success", "voices": voices}
    except Exception as e:
        return {"error": str(e)}
