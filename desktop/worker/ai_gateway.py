import tiktoken  # for OpenAI models
import sys # for printing to stderr
import json # for JSON parsing

# --- Model Configuration ---
# TODO: Keep this updated with the latest model context windows.
MODEL_CONTEXT_WINDOWS = {
    "gpt-4o": 128000,
    "gpt-4": 8192,
    "gpt-3.5-turbo": 16385,
    "claude-3-opus-20240229": 200000,
    "claude-3-sonnet-20240229": 200000,
    "gemini-1.5-pro-latest": 1048576,
    "grok-1": 8192, # Placeholder, check official Grok-4 context size
}

# --- Token-Smart Chunker ---

def get_tokenizer(model_name: str):
    """Returns the appropriate tokenizer for a given model."""
    # TODO: Add tokenizers for other model families (Claude, Gemini, Grok).
    # For now, we default to the GPT-4o tokenizer as a reasonable approximation.
    return tiktoken.encoding_for_model("gpt-4o")

def chunk_data(data: list, model_name: str, chunk_size_ratio: float = 0.85) -> list:
    """
    Splits extracted data into chunks that fit within the model's context window.
    """
    max_tokens = MODEL_CONTEXT_WINDOWS.get(model_name, 8192)
    chunk_max_size = int(max_tokens * chunk_size_ratio)
    tokenizer = get_tokenizer(model_name)
    
    chunks = []
    current_chunk = []
    current_chunk_tokens = 0
    
    # TODO: Improve this logic to be more sophisticated.
    # This is a very basic implementation that just groups data items.
    # A better approach would be to split items themselves if they are too large.
    for item in data:
        # Simple serialization for token counting.
        item_str = str(item)
        item_tokens = len(tokenizer.encode(item_str))
        
        if current_chunk_tokens + item_tokens > chunk_max_size:
            chunks.append(current_chunk)
            current_chunk = [item]
            current_chunk_tokens = item_tokens
        else:
            current_chunk.append(item)
            current_chunk_tokens += item_tokens
            
    if current_chunk:
        chunks.append(current_chunk)
        
    print(f"Split data into {len(chunks)} chunks for model {model_name}.", file=sys.stderr)
    return chunks

# --- AI Gateway ---
from openai import OpenAI

def get_ai_client(api_key: str):
    return OpenAI(api_key=api_key)

def create_review_prompt(chunk: list, profile: dict) -> str:
    """Creates a detailed prompt for the AI review."""
    # TODO: Make this prompt more sophisticated based on the dual-pass strategy.
    
    profile_str = str(profile) # Simple serialization for now
    chunk_str = str(chunk)
    
    return f"""
    You are an expert TAB (Testing, Adjusting, and Balancing) report analyst.
    Review the following data extracted from a TAB report and identify any issues
    based on the provided tolerance profile.

    Tolerance Profile:
    {profile_str}

    Report Data Chunk:
    {chunk_str}

    Identify any readings that are outside the specified tolerances.
    For each issue, provide the page number and a clear description of the problem.
    Respond with a JSON object containing a list of findings, where each finding
    is an object with "page" and "issue" keys.
    If there are no issues, return an empty list.
    """

def call_gpt(client: OpenAI, model_name: str, prompt: str):
    """Calls a GPT model and returns the JSON response."""
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that responds in JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            # TODO: Send enterprise/no-log headers where applicable
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling GPT model {model_name}: {e}", file=sys.stderr)
        return None

def call_claude(api_key: str, model_name: str, prompt: str):
    print(f"Calling Claude model {model_name}...")
    return {"response": "This is a placeholder response from Claude."}

def call_gemini(api_key: str, model_name: str, prompt: str):
    print(f"Calling Gemini model {model_name}...")
    return {"response": "This is a placeholder response from Gemini."}

def call_grok(api_key: str, model_name: str, prompt: str):
    print(f"Calling Grok model {model_name}...")
    return {"response": "This is a placeholder response from Grok."}

def run_ai_review(api_key: str, model_name: str, chunks: list, profile: dict) -> list:
    """
    Runs the dual-pass AI review on the provided data chunks.
    """
    # TODO: Add logic to select the correct client based on model_name
    client = get_ai_client(api_key)
    
    all_findings = []
    
    # This is a simplified single-pass implementation for now.
    print(f"Starting AI review with {model_name}...")
    for chunk in chunks:
        prompt = create_review_prompt(chunk, profile)
        
        # TODO: Route to the correct model call
        response_json_str = call_gpt(client, model_name, prompt)
        
        if response_json_str:
            try:
                response_data = json.loads(response_json_str)
                findings = response_data.get("findings", [])
                all_findings.extend(findings)
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON response: {response_json_str}", file=sys.stderr)

    return all_findings 