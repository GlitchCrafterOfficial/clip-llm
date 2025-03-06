from subprocess import run, Popen, PIPE
from litellm import completion
from pathlib import Path
import json
import os

def open_file():
    file_path = Path('/home/jaime/.clillm/config.json')
    if not file_path.exists():
        print("Run clipllm init first")
        
    with open(file_path, 'r') as f: 
        return json.load(f) 

def copy_selected_text_to_clipboard():
    try:
        run("xclip -selection primary -o | xclip -selection clipboard", shell=True)
    except FileNotFoundError as e:
        print("xclip not found, to install: sudo apt-get install xclip")

def get_clipboard_text():
    return run("xclip -selection clipboard -o", shell=True, capture_output=True).stdout.decode("utf-8")

def set_clipboard_text(text):

    process = Popen(["xclip", "-selection", "clipboard"], stdin=PIPE)
    process.communicate(input=text.encode("utf-8"))

def preprocess_prompt(text, preprocess):
    print("preprocee")
    if preprocess:
        print(preprocess)
        print(text)
        return preprocess + '\n\n' + text

    return text

def use_model(input_prompt, preprocess_config, model_id, advanced_config):
    prompt = preprocess_prompt(input_prompt, preprocess_config)
    if 'gemini' in model_id:
        model = 'gemini/'+model_id
    return completion(
        model = model,
        messages = [{'role':'user', 'content':prompt}],
        temperature=advanced_config['temperature'],
        top_p=advanced_config['top_p'],
        top_k=advanced_config['top_k'],
        max_tokens=advanced_config['max_tokens']
    )['choices'][0]['message']['content']

def gen_env(provider, api_key):
    os.environ[provider] = api_key

def main():
    config = open_file()
    provider = config['provider']['value']
    api_key = config['api_key']
    gen_env(provider, api_key)
    copy_selected_text_to_clipboard()
    input_prompt = get_clipboard_text()
    set_clipboard_text(f"{config['model_id']} Is Thinking...")
    response = use_model(input_prompt, config['initial_prompt'], config['model_id'], config['advanced'])
    set_clipboard_text(response)


if __name__ == "__main__":
    main()



