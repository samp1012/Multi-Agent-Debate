import os
import logging
from ollama import Client as OllamaClient

client = OllamaClient()

os.makedirs('logs', exist_ok=True)
logging.basicConfig(filename='logs/debate_log.txt',
                    level=logging.INFO,
                    format='%(asctime)s - %(message)s')

def log(message):
    print(message)
    logging.info(message)

def user_input_node(state):
    topic = input("Enter topic for debate: ")
    state['topic'] = topic
    log(f"Debate topic: {topic}")
    return state

def agent_node(state, round_num):
    topic = state['topic']
    memory = state.get('memory', [])
    history_text = "\n".join([f"{m['speaker']}: {m['argument']}" for m in memory])

    if round_num % 2 == 0:
        speaker = "Scientist"
        persona_prompt = "You are a scientist arguing for strict AI regulation based on public safety, risks, and real-world implications."
    else:
        speaker = "Philosopher"
        persona_prompt = "You are a philosopher arguing against strict AI regulation, focusing on ethics, autonomy, and societal evolution."

    prompt = f"""{persona_prompt}

Debate Topic: {topic}

Debate so far:
{history_text}

Your next argument should be ONE SHORT, CLEAR SENTENCE ONLY, summarising your strongest next point. Do not explain or elaborate. Do not greet or conclude. Just output the argument sentence.
"""

    response = client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    argument = response['message']['content'].strip()

    # Log and update memory
    log(f"[Round {round_num+1}] {speaker}: {argument}")
    if 'memory' not in state:
        state['memory'] = []
    state['memory'].append({'speaker': speaker, 'argument': argument})

    return state

def judge_node(state):
    topic = state['topic']
    memory = state['memory']
    summary_text = "\n".join([f"{m['speaker']}: {m['argument']}" for m in memory])

    prompt = f"""
You are an impartial judge summarizing a debate between a Scientist and a Philosopher.

Debate Topic: {topic}

Debate Transcript:
{summary_text}

1. Provide a structured summary of both sides' arguments.
2. Decide who won the debate with logical justification.
3. Output clearly as:

Summary:
...
Winner: [Scientist/Philosopher]
Reason: ...
"""

    response = client.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    result = response['message']['content'].strip()

    log("[Judge] Final Verdict:\n" + result)
    print("\n[Judge] Final Verdict:\n" + result)

    return result

def main():
    state = {}
    state = user_input_node(state)

    log("Starting debate between Scientist and Philosopher...")

    for round_num in range(8):
        state = agent_node(state, round_num)

    judge_node(state)

if __name__ == "__main__":
    main()
