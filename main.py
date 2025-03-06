import requests
import time
import concurrent.futures

def send_webhook_message(webhook_url, message):
    data = {
        "content": message,
        "tts": True  
    }

    try:
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            print("Message sent successfully with TTS!")
        elif response.status_code == 429:
            reset_time = int(response.headers.get('X-RateLimit-Reset'))
            current_time = int(time.time())
            wait_time = reset_time - current_time + 1 
            print(f"Rate limit reached. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)  
            send_webhook_message(webhook_url, message) 
        else:
            print(f"Failed to send message. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error sending message: {e}")

def send_messages_concurrently(webhook_url, message, num_messages):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:  
        futures = []
        for _ in range(num_messages):
            futures.append(executor.submit(send_webhook_message, webhook_url, message))
        
        for future in concurrent.futures.as_completed(futures):
            try:
                future.result()
            except Exception as e:
                print(f"Error during message sending: {e}")

def main():
    webhook_url = input("Enter the webhook URL: ")
    message = input("What message would you like to send? ")

    try:
        num_messages = int(input("How many times would you like to send the message? "))
    except ValueError:
        print("Invalid number entered, exiting...")
        return

    send_messages_concurrently(webhook_url, message, num_messages)

if __name__ == "__main__":
    main()
