import asyncio
import os
import sys

try:
    from copilot import CopilotClient
    from copilot.generated.session_events import AssistantMessageData, SessionIdleData
    from copilot.session import PermissionHandler
except ImportError:
    print("Error: github-copilot-sdk is not installed. Please run 'pip install github-copilot-sdk'.")
    sys.exit(1)

async def main():
    """
    Example script to interact with GitHub Copilot via the SDK.
    Requires GITHUB_TOKEN environment variable.
    """
    if not os.getenv("GITHUB_TOKEN"):
        print("Error: GITHUB_TOKEN environment variable is not set.")
        print("You can generate a token at https://github.com/settings/tokens")
        return

    print("--- GitHub Models API Example ---")
    try:
        from azure.ai.inference import ChatCompletionsClient
        from azure.ai.inference.models import SystemMessage, UserMessage
        from azure.core.credentials import AzureKeyCredential

        endpoint = "https://models.inference.ai.azure.com"
        model_name = "gpt-4o"

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(os.getenv("GITHUB_TOKEN")),
        )

        print(f"Sending request to GitHub Models ({model_name})...")
        response = client.complete(
            messages=[
                SystemMessage(content="You are a helpful assistant."),
                UserMessage(content="Explain the importance of AI in software engineering."),
            ],
            model=model_name,
        )

        print(f"Response: {response.choices[0].message.content}\n")
    except Exception as e:
        print(f"GitHub Models API Example failed: {e}\n")

    print("--- GitHub Copilot SDK Example ---")
    try:
        # Client automatically starts on enter and cleans up on exit
        async with CopilotClient() as client:
            print("Creating session...")
            # Create a session with automatic cleanup
            # approve_all allows every tool invocation (use with caution in production)
            async with await client.create_session(
                on_permission_request=PermissionHandler.approve_all,
                model="gpt-4o",
            ) as session:
                # Wait for response using session.idle event
                done = asyncio.Event()

                def on_event(event):
                    if hasattr(event, 'data'):
                        if isinstance(event.data, AssistantMessageData):
                            print(f"\nCopilot: {event.data.content}", end="", flush=True)
                        elif isinstance(event.data, SessionIdleData):
                            done.set()

                session.on(on_event)

                prompt = "Briefly summarize the architecture of this project based on README.md."
                print(f"Sending prompt: {prompt}")

                # Send a message and wait for completion
                await session.send(prompt)
                await done.wait()
                print("\n\nSession complete.")
    except Exception as e:
        print(f"An error occurred during Copilot interaction: {e}")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
    except Exception as e:
        print(f"Unexpected error: {e}")
