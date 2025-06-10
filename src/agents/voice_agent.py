from utils import log_audit
import requests


def handle_voice_request(data, user_id):
    """Handles voice-related tasks like TTS and STT."""
    task = data.get('task')
    try:
        if task == 'tts':
            # Use Mimic 3 for TTS
            response = requests.post(
                'http://mimic3:59125/api/tts',
                json={'text': data.get('text')},
                timeout=10
            )
            response.raise_for_status()
            log_audit(user_id, 'voice_task', {'task': task})
            return {'audio': response.content.hex()}

        elif task == 'stt':
            # Placeholder for speech-to-text
            log_audit(user_id, 'voice_task', {'task': task})
            return {'text': 'Transcribed text'}

        log_audit(user_id, 'voice_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'voice_task', {'error': str(e)})
        return {'error': str(e)}