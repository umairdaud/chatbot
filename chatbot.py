# Importing the necessary dependences
import chainlit as cl
from my_secrets import Secrets  # Loading the Custom module where api key, model and baseurl are stored
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    set_tracing_disabled,
    OpenAIChatCompletionsModel,
)
from typing import cast
from rich import print  
import json  


# This function runs when a new chat session starts
@cl.on_chat_start
async def start():
    # Load secrets credentials from environment
    secrets = Secrets()

    # Initialize the external client
    external_client = AsyncOpenAI(
        base_url=secrets.gemini_api_url,
        api_key=secrets.gemini_api_key,
    )

    # Disable the tracing
    set_tracing_disabled(True)

    # Creating Agent 
    agent = Agent(
        name="Assistant",
        instructions="You are a helpful assistant.",
        model=OpenAIChatCompletionsModel(
            model=secrets.gemini_api_model,
            openai_client=external_client,
        ),
    )

    # Save the agent and an empty chat history to the user's session
    cl.user_session.set("agent", agent)
    cl.user_session.set("history", [])

    # Send a welcome message to the user
    await cl.Message(
        content="Hello! I am your assistant. How can I help you today?"
    ).send()


# Handling incoming user messages
@cl.on_message
async def main(message: cl.Message):

    # Create and send a placeholder message while processing
    msg = cl.Message(content="Thinking...")
    await msg.send()

    # Retrieve the AI agent from the session
    agent: Agent = cast(Agent, cl.user_session.get("agent"))

    # Get the chat history from the session
    history = cl.user_session.get("history") or []

    # Add the current user message to the history
    history.append({"role": "user", "content": message.content})

    try:
        # Run the agent synchronously with the chat history as input
        result = Runner.run_sync(starting_agent=agent, input=history)

        # Update the placeholder message with the agent's response
        msg.content = result.final_output
        await msg.update()

        # Save updated history back to the session
        cl.user_session.set("history", result.to_input_list())

    except Exception as e:
        # If an error occurs, send a user-friendly message and log the error
        msg.content = f"An error occurred while processing your request, Please try again. \n Error:{e}"
        await msg.update()
        print(f"Error updating message: {e}")


# This function is triggered when the chat session ends
@cl.on_chat_end
async def end():
    # Get the final chat history from the session
    history = cl.user_session.get("history") or []

    # Saving the chat history to JSON file for 
    with open("chat_history.json", "w") as f:
        json.dump(history, f, indent=2)
