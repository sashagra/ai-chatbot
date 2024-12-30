from openai import OpenAI
from dataclasses import dataclass

from ai_chatbot.config import OPENAI_API_KEY

# TODO резнести логику сохран ения диалогов и общения с АПИ
@dataclass
class Dialog:
    id: int
    messages: list

class ChatGptDialogs:
    def __init__(self, dialogs={}):
        self.dialogs = dialogs
    
    def is_registrated(self, id:int) -> bool:
        return id in self.dialogs

    def user_register(self, id:int) -> str:
        if id in self.dialogs: return "Вы уже зарегистрированы. Повторная решистрация не требуется"
        self.dialogs[id] = Dialog(id, [])
        return "Вы зарегистрированы как пользователь. Можете общаться с ботом. Первой сообщением задайте описание агента. \
Если хотите общаться с дефолтным агентом, пошлите знак '-'"


    def reset_dialog(self, id:int) -> str:
        self.dialogs[id].messages = []
        return "Диалог был сброшен. Первым сообщением задайте описание агента. \
Если хотите общаться с дефолтным агентом, пошлите знак '-'"


    def send_to_openai(self, id:int, message:str) -> str:
        if message == '-':
            self.dialogs[id].messages = [{"role": "system", "content": "не используй маркдаун в ответе"}]
            return 'Оставлен дефолтный агент. Можете теперь обшаться. Чтобы задать агента и сбросить диалог - введите команду /new'

        if len(message) >= 10 and not self.dialogs[id].messages:
            self.dialogs[id].messages = [{"role": "system", "content": f"{message} и не используй маркдаун в ответе"}]
            return "Агент задан. Можете теперь общаться. Чтобы задать другого агента и сбросить диалог введите команду /new"

        self.dialogs[id].messages.append({"role": "user", "content": message})
        client = OpenAI(api_key=OPENAI_API_KEY)
        completion = client.chat.completions.create(
                model="gpt-4o-mini",
                store=True,
                messages=self.dialogs[id].messages
        )
        res = completion.choices[0].message
        if res:
            self.dialogs[id].messages.append({"role": "assistant", "content": res.content})

        return res.content or "Произошла ошибка. Обратитесь к разработчику"
