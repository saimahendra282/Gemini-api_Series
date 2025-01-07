# to -do 
# write code idiot
import os
import google.generativeai as genai
genai.configure(api_key="Uwu put u r api key here")
generation_config = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_NONE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_NONE",
    },
]
# "Using Megumi Charecter"
# Initialize the generative model
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    safety_settings=safety_settings,
    generation_config=generation_config,
    system_instruction="In this chat, your name is Megumi from konosuba seires , must give responses in plain  telugu text  only also keep them concise and expressive",
)

def upload_video_to_gemini(path):
    """Uploads a video file to the Gemini API."""
    video_file = genai.upload_file(path, mime_type="video/mp4")
    print(f"Uploaded video '{video_file.display_name}' as: {video_file.uri}")
    return video_file

def ask_question_about_video(video_file, question):
    """Asks a question about the uploaded video."""
    chat_session = model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    video_file,
                    question,
                ],
            },
        ]
    )
    response = chat_session.send_message(question)
    print(f'S: {response.text}')
    return response

def process_image_and_prompt():
    while True:
        print("Choose an option to provide an image:")
        print("1. Take screenshot from clipboard")
        print("2. Provide image path")
        choice = input("Enter the number of your choice: ")

        if choice == '1':
            try:
                img = ImageGrab.grabclipboard()
                if img is None:
                    print("No image found in clipboard. Please try again.")
                    continue
                img_data = io.BytesIO()
                img.save(img_data, format='PNG')
                img_data = img_data.getvalue()
                break
            except Exception as e:
                print(f"Error: {e}")
                continue

        elif choice == '2':
            img_path = input("Enter the image path (PNG file): ")
            img_path = Path(img_path)

            if not img_path.exists():
                print("File not found. Please enter a valid path.")
                continue

            img_data = img_path.read_bytes()
            break

        else:
            print("Invalid choice. Please try again.")
            continue

    while True:
        question = input("Enter your question about the image: ")

        img_part = {
            "mime_type": "image/png",
            "data": img_data,
        }

        prompt = [f"{question}:\n", img_part]
        res = model.generate_content(prompt)

        for chunk in res:
            print(chunk.text, end="", flush=True)

        another_question = input("\nDo you have any other questions regarding this image? (yes/no): ").lower()
        if another_question == 'no':
            break
        elif another_question == 'yes':
            continue
        else:
            print("Invalid input. Exiting.")
            break

def gemini_pro_chat():
    sleep(3)
    history = []

    while True:
        user_input = input("You: ")
        print()

        if "bye" in user_input.lower():
            print("OK Bye User-kun. See you again..👋🏻!")
            break
        if "img" in user_input.lower():
          process_image_and_prompt()
        if "video" in user_input.lower():
          # to do add a method to recieve video path,quetion string and give response 
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text
        print(f'Megumi Saying: {model_response}')
        
        # generate_and_play_speech(model_response)
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})


# run_ui_in_thread()
gemini_pro_chat()
