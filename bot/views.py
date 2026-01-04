from django.shortcuts import render, redirect
from .forms import PromptForm
from .models import Conversation
from google import genai
import markdown
import os

# Ensure GEMINI_API_KEY is set in your environment
client = genai.Client()  

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

            # 🔹 Generate response from Gemini
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )

            bot_response = markdown.markdown(response.text or "<i>No response from Gemini.</i>")

            # 🔹 Save conversation
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
