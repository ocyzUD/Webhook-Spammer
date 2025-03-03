import requests
import time

def send_webhook_message(webhook_url, message):
    data = {
        "content": message
    }

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Message sent!")
        else:
            print(f"Failed to send message: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending to webhook: {e}")

def main():

    webhook_url =input("Please enter the webhook url: ")

    message = input ("What message would you like to send?: ")

    try:
        num_messages = int(input("How many times to send the message?: "))
    except ValueError:
        print("Invalid number, exiting")
        return
    
    for _ in range(num_messages):
        send_webhook_message(webhook_url, message)

if __name__ == "__main__":
    main()
