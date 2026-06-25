
# pyrefly: ignore [missing-import]
from google.adk import Agent
from google.adk import Workflow
from google.adk import Event

# Agent to classify user query
process_message = Agent(
    name="process_message",
    model="groq/llama-3.3-70b-versatile", # using a currently supported model
    instruction="""Classify user message into either "SHIPPING" or "UNRELATED".
    If the query is related to shipping (rates, tracking, delivery, returns), respond with "SHIPPING".
    If the query is completely unrelated to shipping, respond with "UNRELATED".
    Only respond with one of the two options. Do not include any other text.""",
    output_schema=None
)

# Router node to redirect workflow based on classification
def router(node_input: str):
    routes = node_input.split(",")
    routes = [route.strip() for route in routes]
    return Event(route=routes)

# Node for unrelated questions
def response_unrelated(node_input: str):
    return Event(message="I'm sorry, but I am a shipping customer support representative. I can only assist with shipping-related queries like rates, tracking, delivery, and returns.")

# Agent to answer shipping questions
shipping_faq_agent = Agent(
    name="shipping_faq_agent",
    model="groq/llama-3.3-70b-versatile", # using a currently supported model
    instruction="""You are a helpful customer support representative for a shipping company.
    Answer the user's query regarding shipping (rates, tracking, delivery, returns).
    Be polite and professional.
    """,
    output_schema=None,
)

# Define the workflow graph
root_agent = Workflow(
    name="customer_support_workflow",
    edges=[
        ("START", process_message, router),
        (
            router,
            {
                "SHIPPING": shipping_faq_agent,
                "UNRELATED": response_unrelated,
            }
        )
    ],
)

if __name__ == "__main__":
    print("Graph Workflow initialized successfully.")
    # Example usage:
    # event = root_agent.run("What are your shipping rates for international packages?")
    # print(event.message)
