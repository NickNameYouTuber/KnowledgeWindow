from together import Together
from langchain import PromptTemplate

TOGETHER_API_KEY = "c00408153177483c93bb3a5eb3c8cc1e8de2fac5ddacc09203d6d6bbf54585aa"  # Replace this with your actual API key


def search_together(query: str, data: dict, template: str) -> str | None:
    client = Together(api_key=TOGETHER_API_KEY)

    # Создаем PromptTemplate с использованием LangChain
    prompt_template = PromptTemplate(
        input_variables=["query", "data"],
        template=template
    )

    # Формируем сообщение для Together
    messages = [
        {"role": "system", "content": prompt_template.format(query=query, data=data)}
    ]

    # Создаем запрос к Together API для модели (не потоковое)
    response = client.chat.completions.create(
        model="meta-llama/Llama-Vision-Free",  # Пример модели
        messages=messages,
    )

    # Доступ к ответу как в вашем примере
    if response.choices:  # Проверяем, есть ли варианты в ответе
        for choice in response.choices:
            print(choice.message.content)
        return response.choices[0].message.content
    else:
        return "No response from model"