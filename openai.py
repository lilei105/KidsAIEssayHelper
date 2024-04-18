import base64, requests, time, configparser

# OpenAI API Key
api_key = ""

# Model to use
model = "claude-3-sonnet-20240229"

# Path to your image
image_path = "test5.jpg"

base_url = "http://154.9.243.105:3000/v1/chat/completions"


def get_api_key_from_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
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
                    {
                        "type": "text",
                        "text": "Extract text from this image, do not explain.",
                    },
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
        base_url, headers=headers, json=payload
    )
    end_time = time.time()
    print(f"{model}的执行时间: {end_time - start_time}")
    print()
    text = response.json()["choices"][0]["message"]["content"]
    return text


# text = "My future school life \
#         In the future, I think the will be full of technology. \
#         Students can learn with robots, robots will be their teachers or classmates. Students will study on the internet. They can learn the old classes whenever they are. Study will be convenient and full of interesting.\
#         The parents can check their kid's grade very fast and they can know what should they do with what's value.\
#         Students can do alots of things after school. The most popular and the most important thing maybe is do sports.\
#         In the future, almost everything can't work without the internet. but people will be very rely on the internet, so they will do some sports to let their body and eyes have a rest and train their sport skills."


def correct(text):
    api_key = get_api_key_from_config()

    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    payload = {
        "model": model,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant designed to give written advices to non-native English speaking student. Given the text, you need to carry out the following tasks: You speak Chinese except for the original text and the suggestions for improment; Read and print the handwritten English text; Identify the grammatical errors, provide detailed reasons for each, and offer suggestions for improvement; Say something nice when you point out errors and give suggestions; Your suggestions should solely use basic vocabulary and grammar; Finally, print the full English text as modified by your suggestions.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        "max_tokens": 1000,
    }

    start_time = time.time()
    response = requests.post(
        base_url, headers=headers, json=payload
    )
    end_time = time.time()
    print(f"{model}的执行时间: {end_time - start_time}")
    
    try:
        text = response.json()["choices"][0]["message"]["content"]
        print(text)
    except Exception as e:
        print(e)
        
    


text = extract_text_from_image(image_path)
print(text)
print()
correct(text)
