from src.utils.helpers import log_audit
import tweepy


def handle_social_request(data, user_id):
    """Handles social media related tasks."""
    task = data.get('task')
    try:
        if task == 'post':
            auth = tweepy.OAuthHandler(
                data.get('consumer_key'), data.get('consumer_secret')
            )
            auth.set_access_token(
                data.get('access_token'), data.get('access_secret')
            )
            api = tweepy.API(auth)
            api.update_status(data.get('content'))
            log_audit(user_id, 'social_task', {'task': task})
            return {'status': 'posted'}

        log_audit(user_id, 'social_task', {'task': task or 'unknown'})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'social_task', {'error': str(e)})
        return {'error': str(e)}
