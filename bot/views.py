# chat/views.py
import json
import requests
from django.conf import settings
from django.http import JsonResponse
from django.views import View
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class ChatPageView(TemplateView):
    template_name = "chat/chat.html"  

@method_decorator(csrf_exempt, name='dispatch')
class ChatbotAPIView(View):


    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            user_message = data.get("message", "")

            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8000",  
                "X-Title": "School Chatbot",
            }

            payload = {
                "model": "deepseek/deepseek-chat",  
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful school assistant. Answer clearly and simply."
                    },
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            }

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=payload
            )

            result = response.json()
            reply = result["choices"][0]["message"]["content"]

        except Exception as e:
            reply = f"Server error: {str(e)}"

        return JsonResponse({"reply": reply})
