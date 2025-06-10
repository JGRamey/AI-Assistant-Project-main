from utils import log_audit
import boto3


def handle_alert_request(data, user_id):
    try:
        sns = boto3.client('sns')
        if data.get('task') == 'set_alert':
            sns.publish(
                TopicArn=data.get('topic_arn'),
                Message=f"Trade Alert: {data.get('message')}"
            )
            return {'status': 'alert_sent'}
        log_audit(user_id, 'alert_task', {'task': data.get('task')})
        return {'status': 'success'}
    except Exception as e:
        log_audit(user_id, 'alert_task', {'error': str(e)})
        return {'error': str(e)}
