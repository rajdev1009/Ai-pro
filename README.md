# Ai-pro
## कैसे काम करता है (End-to-End Flow)

यह सेक्शन प्रोजेक्ट के हर स्टेप को साफ़, क्रमवार और तकनीकी रूप से बताता है ताकि कोई भी डेवलपर या उपयोगकर्ता समझ सके कि बॉट कैसे चलता है।

### 1. उपयोगकर्ता इनपुट
- उपयोगकर्ता Telegram पर बॉट को **text message** या **voice message** भेजता है।
- Telegram सर्वर बॉट की webhook/polling के माध्यम से यह संदेश पहुँचाता है।

### 2. Telegram Bot (pyTelegramBotAPI / telebot)
- `main.py` में Bot handlers होते हैं:
  - `@bot.message_handler(content_types=['text'])` — टेक्स्ट हैंडल करता है।
  - `@bot.message_handler(content_types=['voice'])` — वॉइस फाइलों को स्वीकार करता है।
- यदि voice message है, तो फ़ाइल डाउनलोड कर के स्थानीय रूप में `ogg`/`oga` के रूप में सेव की जाती है।

### 3. Speech-to-Text (Gemini Audio Model)
- वॉइस फ़ाइल को Google Gemini के audio-to-text endpoint पर भेजा जाता है।
- Gemini audio model वॉइस को transcribe कर के text लौटाता है (user_text)।
- ट्रांसक्रिप्ट की गुणवत्ता बढ़ाने हेतु `generation_config` में low temperature और domain/context hints दिए जा सकते हैं।

### 4. AI Response Generation (Gemini Text Model)
- User का text (या voice से निकला text) Gemini के text model (example: `gemini-pro`) को भेजा जाता है।
- Model context-aware और conversational response देता है (ai_reply) — आप prompts में system messages, conversation history, या persona instructions जोड़ सकते हैं।

### 5. Text Reply → User
- AI से आया text reply सीधे Telegram पर `bot.send_message(chat_id, ai_reply)` से user को भेजा जाता है।

### 6. Text → Speech (gTTS)
- `gTTS` का उपयोग कर `ai_reply` को Hindi (या configured language) में audio (MP3) में convert किया जाता है।
- जनरेट की गयी audio फ़ाइल को `bot.send_voice()` के माध्यम से user को भेजा जाता है — इस तरह user को voice reply भी मिलती है।

### 7. Error Handling & Resilience
- Polling loop में try/except — किसी भी exception पर bot 5 सेकंड बाद restart करता है।
- Network/Timeout errors को log/notify करना चाहिए और optional alerting (email/Telegram admin) जोड़ा जा सकता है।
- Temp audio files को cleanup करना जरूरी है, वरना disk भर सकता है — production में बेहतर होगा कि files ephemeral storage या memory streams में रहें।

### 8. Deployment Notes
- Flask server एक lightweight endpoint (`/`) चलता है ताकि PaaS (Heroku/Render) पर app "web dyno" के रूप में चल सके।
- `Procfile` में `web: python main.py` रखा जाता है ताकि Heroku पर web process शुरू हो जाए।
- `.env` में `GOOGLE_API_KEY` और `TELEGRAM_BOT_TOKEN` सुरक्षित रखिए — कभी repo में commit न करें।

### 9. Security & Privacy Best Practices
- User audio और transcripts
