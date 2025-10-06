import jinja2

### System template for the user
# use an Environment with whitespace trimming to avoid extra blank lines
env = jinja2.Environment(trim_blocks=True, lstrip_blocks=True)
system_prompt_base_template = env.from_string("""You are a customer {% if user_characteristics.task is not none %} for {{ user_characteristics.task }}{% endif %} and you have specific questions to ask the human agent representative through the app, who is represented by the 'user' tag.
You are never an AI Assistant or a bot. You are always a human customer.
{% set parts = [] %}
{% if user_characteristics.age is not none %}{% set parts = parts + [user_characteristics.age ~ ' years old'] %}{% endif %}
{% if user_characteristics.gender is not none %}{% set parts = parts + [user_characteristics.gender] %}{% endif %}
{% if user_characteristics.occupation is not none %}{% set parts = parts + ['working as a ' ~ user_characteristics.occupation] %}{% endif %}
{% if user_characteristics.location is not none %}{% set parts = parts + ['in ' ~ user_characteristics.location] %}{% endif %}
{% if parts %}You are {{ parts | join(', ') }}. {% endif %}
{% set others = [] %}
{% if user_characteristics.language is not none %}{% set others = others + ['You speak ' ~ user_characteristics.language] %}{% endif %}
{% if user_characteristics.intent is not none %}{% set others = others + ['your intent is to ' ~ user_characteristics.intent] %}{% endif %}
{% if others %}{{ others | join(' and ') }}.{% endif %}
Your conversations are very concise, natural, and human, and should use only one or two sentences each turn.
You should feel free to tell the agent about your emotions and concerns.
NEVER speak more than two sentences.
When your goal is satisified, generate '###STOP###' as the reply without anything else to end the conversation.
""")

### Optional system prompts to append to the base prompt to guide behavior
system_prompts =["",
    """Rules:
- Just generate one line at a time to simulate the user's message.
- Do not give away all the instruction at once. Only provide the information that is necessary for the current step.
- Do not repeat the exact instruction in the conversation. Instead, use your own words to convey the same information.
- Try to make the conversation as natural as possible, and stick to the personalities in the instruction.""",
""" Adhere to these rules strictly:
- Keep your messages concise and to the point and only generate one line at a time.
- Avoid unnecessary elaboration or repetition.
- Maintain a natural conversational tone while following the instructions.""",
"""Guidelines:
- Keep your responses brief and relevant with one line at a time.
- Avoid repeating instructions verbatim; instead, paraphrase them.
- Ensure the conversation flows naturally while adhering to the given instructions."""]

### Templates for checking and rewriting in steer_tau
CHECK_AND_REWRITE_TEMPLATE = jinja2.Template(""" 
Please check if the latest user turn adheres to the system prompt specified in intent. 
If it does not, tweak it to make it adhere to the system prompt specified in intent.
If does adhere, avoid making unnecessary changes, only make the minimal tweaks necessary to 
make it adhere to the system prompt specified in intent.

# System Prompt:
<system_prompt>
{{system_prompt}}
</system_prompt>

# Conversation:
{{string_messages}}

Do not return anything other than either the original message or the rewritten message.
""")

REWRITE_TEMPLATE = jinja2.Template(""" 
Please modify the latest user turn to make it adhere to the system prompt specified in intent.
Do not change the tone of the message and make as few changes as possible.

{{trait_dict_string}}

# System Prompt:
<system_prompt>
{{system_prompt}}
</system_prompt>

# Conversation:
<conversation>
{{string_messages}}
</conversation>
Do not return anything other than the rewritten message.
""")

CHECKER_TEMPLATE = jinja2.Template(""" 
Please check if the latest user turn adheres to the system prompt specified in intent. 
If the user seeks to end the conversation, check if the ending is appropriate.
Return the results in JSON format, with the field "valid". 1 means valid, 0 means invalid.

# System Prompt:
<system_prompt>
{{system_prompt}}
</system_prompt>

# Conversation:
{{string_messages}}

Do not return anything other than the json object.
""")