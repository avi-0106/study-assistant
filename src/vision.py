import ollama # type: ignore
import base64

def describe_image(image_bytes, model="llava"):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    
    response = ollama.chat(
        model=model,
        messages=[{
            "role": "user",
            "content": "This is an image from a university lecture slide or textbook. Transcribe ALL text you see including handwritten notes. Describe and explain any diagrams, graphs, plots or equations. Be precise and complete.",
            "images": [image_b64]
        }]
    )
    
    return response['message']['content']