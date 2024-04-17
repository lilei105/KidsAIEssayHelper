import base64, requests, time, configparser

# OpenAI API Key
api_key = ""

# Model to use
model = "claude-3-haiku-20240307"

# Path to your image
image_path = "test5.jpg"

def get_api_key_from_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    # global api_key
    api_key = config["DEFAULT"]["api_key"]
    return api_key

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def extract_text_from_image(image_path):
    # Getting the base64 string
    base64_image = encode_image(image_path)
    api_key = get_api_key_from_config()
    
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract text from this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 1000,
    }

    start_time = time.time()
    response = requests.post(
        "https://api.fast-tunnel.one/v1/chat/completions", headers=headers, json=payload
    )
    end_time = time.time()
    print(f"{model}的执行时间: {end_time - start_time}")

    print(response.json()["choices"][0]["message"]["content"])



extract_text_from_image(image_path)