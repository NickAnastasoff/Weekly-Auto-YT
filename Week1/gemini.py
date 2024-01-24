import google.generativeai as genai
import os

gemini_key = os.environ['GEMINI_API_KEY']

def get_bytes(image_path):
    """Returns the bytes of an image."""
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
    return image_data

def prompt(prompt, temp=0.9, has_image=False):
    """Generates content from a prompt."""
    config = {
        "temperature": temp
    }

    try:
        # Configure API
        genai.configure(api_key=gemini_key)

        if has_image:
            # Use the 'gemini-pro-vision' model for image processing
            model = genai.GenerativeModel('gemini-pro-vision')
        else:
            # Use the 'gemini-pro' model for text processing
            model = genai.GenerativeModel('gemini-pro')


        response = model.generate_content([prompt], 
                                        generation_config=config)
        return response.text

    except Exception as e:
        print(e)
        return