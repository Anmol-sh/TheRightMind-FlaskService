import base64
import os
from google import genai
from google.genai import types
from env_var import gemini_api_key


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()


async def generate(message = 'Create an image of a rose garden.'):
    client = genai.Client(
        api_key=gemini_api_key,
    )

    output_img = "output_img.jpeg"
    output_text = "/Users/anmol/Code/TheRightMind/output_text.txt"

    model = "gemini-2.0-flash-exp"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=message),
            ],
        )
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1.25,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_modalities=[
            "image",
            "text",
        ],
        response_mime_type="text/plain",
    )

    output_resp = {}
    response_type = ""
    img_f = open(output_img, "wb")
    text_f = open(output_text, "w")

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print("\n====== Chunk of response ===\n")
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        if chunk.candidates[0].content.parts[0].inline_data:
            img_f.write(chunk.candidates[0].content.parts[0].inline_data.data)
            print(
                "File of mime type"
                f" {chunk.candidates[0].content.parts[0].inline_data.mime_type} saved"
                f"to: {output_img}"
            )
            response_type = "img"
        else:
            print(chunk.text)
            text_f.write(chunk.text)
            response_type = "text"
    
    if response_type=="img":
        output_resp = {'img': "http://127.0.0.1:5000/image/" + output_img}
    else:
        text_f = open(output_text, "r")
        output_resp = {'text': text_f.read()}

    img_f.close()
    text_f.close()
    return output_resp

if __name__ == "__main__":
    generate()
