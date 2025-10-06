lfrom litellm import completion

response = completion(
            model="hosted_vllm/Qwen3-8B",
            messages = [{ "content": "Hello, how are you?","role": "user"}],
            api_base="http://localhost:8002/v1",  
            api_key="nonce"  # Add this line  
)
print(response)