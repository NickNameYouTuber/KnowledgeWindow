from openai import OpenAI
from langchain import PromptTemplate
from app.config.database import NeuralNetworkSettings

def search_together(query: str, data: dict, template: str) -> str | None:
    print("Query: " + query)

    # Get neural network settings from the database
    settings = NeuralNetworkSettings.query.first()
    if not settings:
        print("Error: Neural network settings not found")
        return None

    # Initialize OpenAI client with Together.ai base URL and API key
    client = OpenAI(
        base_url=settings.url,
        api_key=settings.api_key
    )

    print("Client")

    # Create PromptTemplate using LangChain
    prompt_template = PromptTemplate(
        input_variables=["query", "data"],
        template=template
    )

    # Collect responses from each file
    responses = []
    for kb_id, kb_data in data.items():
        # Format messages for API request
        messages = [
            {
                "role": "system",
                "content": prompt_template.format(query=query, data=kb_data)
            }
        ]

        try:
            response = client.chat.completions.create(
                model=settings.model,
                messages=messages
            )

            # Process response
            if response.choices:
                for choice in response.choices:
                    print(choice.message.content)
                responses.append(response.choices[0].message.content)

        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    # Combine responses into a final answer
    final_response = "\n".join(responses)
    return final_response