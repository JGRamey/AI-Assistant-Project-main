from utils import log_audit
import requests

def handle_voice_request(data, user_id):
    try:
        if data.get('task') == 'tts':
            # Use Mimic 3 for TTS
            response = requests.post(
                'http://mimic3:59125/api/tts',
                json={'text': data.get('text')}
            )
            return {'audio': response.content.hex()}
        elif data.get('task') == 'stt':
            # Placeholder for speech-to-text
            return {'text': 'Transcribed text'}
        log_audit(user_id, 'voice_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'voice_task', {'error': str(e)})
        return {'error': str(e)}