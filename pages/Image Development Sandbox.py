import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import requests

# Initialize OpenAI client
api_key = st.secrets["openai"]["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

# Function to generate an image variation
def generate_image_variation(image_file):
    response = client.images.create_variation(
        image=image_file,
        n=1,
        size="1024x1024"
    )
    # Access the URL from the response object
    variant_url = response.data[0].url
    return variant_url

# Streamlit app
def main():
    st.title("Image Variation Generator")
    
    # Image upload
    uploaded_file = st.file_uploader("Upload an image (1:1 ratio required)", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        # Open the uploaded image
        image = Image.open(uploaded_file)
        width, height = image.size
        
        # Check if the image is 1:1 ratio
        if width != height:
            st.error("The uploaded image must have a 1:1 ratio.")
        else:
            st.image(image, caption="Uploaded Image", use_column_width=True)
            st.write("Generating image variation...")

            # Convert image to binary for API
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            # Generate variation
            try:
                variant_url = generate_image_variation(img_byte_arr)
                st.write("Generated Variation URL:")
                st.write(variant_url)  # Display the URL of the generated image variation
                
                # Display the generated image in an image container
                response = requests.get(variant_url)
                generated_image = Image.open(io.BytesIO(response.content))
                st.image(generated_image, caption="Generated Variation", use_column_width=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()