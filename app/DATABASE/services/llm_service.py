from langchain import PromptTemplate
from openai import OpenAI

from app.DATABASE.config.database import NeuralNetworkSettings
from typing import Dict

def search_together(query: str, data: dict, template: str) -> str | None:
    print("Query: " + query)

    settings = NeuralNetworkSettings.query.first()
    if not settings:
        print("Error: Neural network settings not found")
        return None

    client = OpenAI(
        base_url=settings.url,
        api_key=settings.api_key
    )

    # Простой подсчет токенов: примерно 4 символа на токен
    def estimate_tokens(text: str) -> int:
        return len(text) // 4

    # Функция для создания батча документов в пределах лимита токенов
    def create_batch(remaining_data: Dict, token_limit: int = 4000) -> Dict:
        batch = {}
        current_tokens = 0

        for kb_id, kb_data in remaining_data.items():
            content = f"Document {kb_id}:\nTitle: {kb_data['title']}\nContent: {kb_data['content']}\n\n"
            tokens = estimate_tokens(content)

            # Оставляем место для промпта и ответа
            if current_tokens + tokens > token_limit - 1000:
                break

            batch[kb_id] = kb_data
            current_tokens += tokens

        return batch

    # Функция для обработки одного батча документов
    def process_batch(batch_data: Dict) -> str | None:
        if not batch_data:
            return None

        combined_data = {
            "title": "Combined Knowledge Base",
            "content": "\n\n".join([
                f"Document: {kb_data['title']}\n{kb_data['content']}"
                for kb_data in batch_data.values()
            ])
        }

        try:
            prompt_template = PromptTemplate(template=template)
            messages = [{
                "role": "system",
                "content": prompt_template.format(query=query, data=combined_data)
            }]

            response = client.chat.completions.create(
                model=settings.model,
                messages=messages
            )

            return response.choices[0].message.content if response.choices else None

        except Exception as e:
            print(f"Error processing batch: {e}")
            return None

    # Обработка всех документов батчами
    responses = []
    remaining_data = data.copy()

    while remaining_data:
        # Создаем батч документов
        batch = create_batch(remaining_data)
        if not batch:
            break

        # Обрабатываем батч
        response = process_batch(batch)
        if response:
            responses.append(response)

        # Удаляем обработанные документы из оставшихся
        for kb_id in batch.keys():
            remaining_data.pop(kb_id)

    # Если получили только один ответ, возвращаем его
    if len(responses) == 1:
        return responses[0]

    # Если получили несколько ответов, суммируем их
    if len(responses) > 1:
        summary_prompt = PromptTemplate(
            template="""Given the following responses to the query: "{query}", 
            please provide a comprehensive summary that combines all relevant information:

            {responses}

            Please provide a clear, concise summary that addresses the original query."""
        )

        try:
            messages = [{
                "role": "system",
                "content": summary_prompt.format(
                    query=query,
                    responses="\n\n=== Next Response ===\n\n".join(responses)
                )
            }]

            final_response = client.chat.completions.create(
                model=settings.model,
                messages=messages
            )

            return final_response.choices[0].message.content if final_response.choices else None

        except Exception as e:
            print(f"Error creating summary: {e}")
            # В случае ошибки при суммаризации возвращаем все ответы как есть
            return "\n\n=== Next Response ===\n\n".join(responses)

    return None