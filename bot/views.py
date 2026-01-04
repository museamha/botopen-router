from django.shortcuts import render, redirect
from .forms import PromptForm
from .models import Conversation
from django.conf import settings
import google.generativeai as genai
import markdown

genai.configure(api_key=settings.GEMINI_API_KEY)


def chat_view(request):
    conversations = Conversation.objects.all().order_by("created_at")

    if request.method == "POST":

        # 🔹 Clear chat
        if "clear" in request.POST:
            Conversation.objects.all().delete()
            return redirect("chat")

        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]

            # 🔹 Build chat history
            history = []
            for convo in conversations:
                history.append({
                    "role": "user",
                    "parts": [convo.user_message]
                })
                history.append({
                    "role": "model",
                    "parts": [convo.bot_response]
                })

            # 🔹 Start Gemini chat
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            chat = model.start_chat(history=history)

            response = chat.send_message(prompt)

            # ✅ Default value
            bot_response = "<i>No response from Gemini.</i>"

            if response and response.candidates:
                raw_text = response.candidates[0].content.parts[0].text
                bot_response = markdown.markdown(raw_text)  # Convert markdown to HTML

            # 🔹 Save conversation once
            Conversation.objects.create(
                user_message=prompt,
                bot_response=bot_response
            )

            return redirect("chat")

    else:
        form = PromptForm()

    return render(request, "bot/index.html", {
        "form": form,
        "conversations": conversations
    })
