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
    st.text("Upload must be under 2MB and a 1:1 aspect ratio. Each generation costs us about 10 cents. Only upload 1 image at a time.")

    # Image upload
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)

        # Display a resized version of the image (512x512)
        resized_image = image.resize((512, 512))
        st.image(resized_image, caption="Uploaded Image", use_column_width=False, width=512)

        # Encode the image in base64 (using original full-size image)
        base64_image = encode_image(image)

        # Initialize session state for description and generated image URL
        if 'description' not in st.session_state:
            st.session_state.description = ''
        if 'generated_image_url' not in st.session_state:
            st.session_state.generated_image_url = ''

        # Generate description
        if st.button("Describe Image"):
            try:
                # Get the image description
                description_response = describe_image(base64_image)
                description = description_response['choices'][0]['message']['content']
                st.session_state.description = description  # Store description in session state
                st.write("Generated Description:")
                st.session_state.generated_image_url = ''  # Reset generated image URL
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if 'description_response' in locals():
                    st.write(description_response)  # Print raw response for debugging

        # Display and allow editing of the description
        if st.session_state.description:
            edited_description = st.text_area("Edit Description", st.session_state.description, height=150)

            # Button to generate the image
            if st.button("Generate Image"):
                if edited_description:
                    generated_image_url = generate_image(edited_description)
                    if generated_image_url:
                        st.session_state.generated_image_url = generated_image_url

        # Display the generated image if available
        if st.session_state.generated_image_url:
            st.write("Generated Image URL:")
            st.write(st.session_state.generated_image_url)
            st.image(st.session_state.generated_image_url, caption="Generated Image", use_column_width=False, width=512)

if __name__ == "__main__":
    main()