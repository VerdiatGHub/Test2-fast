import random
import string
from fastapi import HTTPException
import secrets
import re
import json


class CustomError(HTTPException):
    def __init__(self, status_code: int, message: str):
        super().__init__(status_code=status_code, detail=message)
        self.message = message


def generate_random_string(size=32):
    random_string = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(size)])
    return random_string


def generate_ver_token():
    return 'ver_token_' + generate_random_string(128)


def generate_user_id():
    return 'na_usr_' + generate_random_string(20)


def generate_thread_id():
    return generate_random_string(20)


def generate_random_number(size=6):
    number = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, size)])
    return number


def generate_api_key():
    return 'na-sk-' + secrets.token_urlsafe(64)


def extract_json(raw: str):
    """Extract the first valid JSON object from a string, handling nested braces correctly."""
    start_idx = raw.find('{')
    if start_idx == -1:
        raise ValueError("No valid JSON found in model response.")
    
    brace_count = 0
    in_string = False
    escape_next = False
    
    for i in range(start_idx, len(raw)):
        char = raw[i]
        
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
        
        if char == '"':
            in_string = not in_string
            continue
        
        if not in_string:
            if char == '{':
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                
                if brace_count == 0:
                    json_str = raw[start_idx:i+1]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Invalid JSON found in model response: {str(e)}")
    
    raise ValueError("No valid JSON found in model response (unbalanced braces).")


def extract_json_array(raw: str):
    """Extract the first valid JSON array from a string, handling nested brackets correctly."""
    start_idx = raw.find('[')
    if start_idx == -1:
        raise ValueError("No valid JSON array found in model response.")
    
    bracket_count = 0
    in_string = False
    escape_next = False
    
    for i in range(start_idx, len(raw)):
        char = raw[i]
        
        if escape_next:
            escape_next = False
            continue
        
        if char == '\\':
            escape_next = True
            continue
        
        if char == '"':
            in_string = not in_string
            continue
        
        if not in_string:
            if char == '[':
                bracket_count += 1
            elif char == ']':
                bracket_count -= 1
                
                if bracket_count == 0:
                    json_str = raw[start_idx:i+1]
                    try:
                        return json.loads(json_str)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Invalid JSON array found in model response: {str(e)}")
    
    raise ValueError("No valid JSON array found in model response (unbalanced brackets).")
