import ollama # type: ignore
import base64

def describe_image(image_bytes, model="llava"):
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    
    response = ollama.chat(
        model=model,
        messages=[{
            "role": "user",
            "content": "Describe this image in detail. If it contains diagrams, equations, or handwritten notes, transcribe and explain them clearly.",
            "images": [image_b64]
        }]
    )
    
    return response['message']['content']