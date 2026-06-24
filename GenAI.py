{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c4059ebd",
   "metadata": {
    "vscode": {
     "languageId": "plaintext"
    }
   },
   "outputs": [],
   "source": [
    "import gradio as gr\n",
    "from groq import Groq\n",
    "\n",
    "client = Groq(api_key=\"GROQ_API_KEY\")\n",
    "\n",
    "def respond(message, history, system_prompt, temperature):\n",
    "    messages = [{\"role\": \"system\", \"content\": system_prompt}]\n",
    "\n",
    "    for turn in history:\n",
    "        messages.append({\n",
    "            \"role\": turn[\"role\"],\n",
    "            \"content\": turn[\"content\"]\n",
    "        })\n",
    "\n",
    "    messages.append({\"role\": \"user\", \"content\": message})\n",
    "\n",
    "    stream = client.chat.completions.create(\n",
    "        model=\"llama-3.1-8b-instant\",\n",
    "        messages=messages,\n",
    "        temperature=temperature,\n",
    "        stream=True\n",
    "    )\n",
    "\n",
    "    partial = \"\"\n",
    "\n",
    "    for chunk in stream:\n",
    "        partial += chunk.choices[0].delta.content or \"\"\n",
    "        yield partial\n",
    "\n",
    "\n",
    "demo = gr.ChatInterface(\n",
    "    fn=respond,\n",
    "    type=\"messages\",\n",
    "    title=\"AI Expert\",\n",
    "    additional_inputs=[\n",
    "        gr.Textbox(\n",
    "            label=\"System Prompt\",\n",
    "            value=\"You are a football expert with experience in every aspect of football rules and regulations including the history of football.\",\n",
    "            lines=4\n",
    "        ),\n",
    "        gr.Slider(\n",
    "            minimum=0.0,\n",
    "            maximum=1.0,\n",
    "            value=0.4,\n",
    "            step=0.1,\n",
    "            label=\"Temperature\"\n",
    "        )\n",
    "    ]\n",
    ")\n",
    "\n",
    "demo.launch(debug=True)"
   ]
  }
 ],
 "metadata": {
  "language_info": {
   "name": "python"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
