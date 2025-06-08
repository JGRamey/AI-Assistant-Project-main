from utils import log_audit
import tweepy

def handle_social_request(data, user_id):
    try:
        auth = tweepy.OAuthHandler(data.get('consumer_key'), data.get('consumer_secret'))
        auth.set_access_token(data.get('access_token'), data.get('access_secret'))
        api = tweepy.API(auth)
        if data.get('task') == 'post':
            api.update_status(data.get('content'))
            return {'status': 'posted'}
        log_audit(user_id, 'social_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'social_task', {'error': str(e)})
        return {'error': str(e)}