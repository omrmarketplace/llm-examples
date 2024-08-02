import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import requests

# Initialize OpenAI client
api_key = st.secrets["openai"]["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)


# Function to encode the image
def encode_image(image):
    buffered = io.BytesIO()
    # Convert RGBA to RGB if necessary
    if image.mode == "RGBA":
        image = image.convert("RGB")
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Function to describe the image
def describe_image(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response.json()

# Function to generate an image based on the description
def generate_image(description):
    response = client.images.generate(
        prompt=description,
        model="dall-e-3",
        size="1024x1024",
        n=1,
    )
    return response.data[0].url

# Streamlit app
def main():
    st.title("Image Description and Generation")

    # Image upload
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Encode the image in base64
        base64_image = encode_image(image)

        # Generate description
        if st.button("Describe and Generate Image"):
            try:
                # Get the image description
                description_response = describe_image(base64_image)
                description = description_response['choices'][0]['message']['content']
                st.write("Image Description:")
                st.write(description)  # Output the description in plain text

                # Use the description as a prompt to generate a new image
                generated_image_url = generate_image(description)
                st.write("Generated Image URL:")
                st.write(generated_image_url)
                st.image(generated_image_url, caption="Generated Image", use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if 'description_response' in locals():
                    st.write(description_response)  # Print raw response for debugging

if __name__ == "__main__":
    main()