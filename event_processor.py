import os
import requests
from kubernetes import client, config, watch
from slack_sdk import WebClient

def send_slack_notification(text):
    slack_token = os.environ.get('SLACK_TOKEN')
    client = WebClient(token=slack_token)

    channel_id = "#your-channel-id"  # Replace with your Slack channel ID
    response = client.chat_postMessage(
        channel=channel_id,
        text=text
    )

def main():
    config.load_incluster_config()
    v1 = client.CoreV1Api()

    w = watch.Watch()
    for event in w.stream(v1.list_pod_for_all_namespaces):
        if event['object'].status.container_statuses:
            for container_status in event['object'].status.container_statuses:
                if container_status.restart_count > 0:
                    message = f"Pod {event['object'].metadata.name} restarted {container_status.restart_count} times."
                    send_slack_notification(message)

if __name__ == '__main__':
    main()
