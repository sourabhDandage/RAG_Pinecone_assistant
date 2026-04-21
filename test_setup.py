import google.generativeai as genai
import os

genai.configure(api_key="AIzaSyC-VJyJz8It24oAvGK9Vfk-ijb7bT-F_40")


for m in genai.list_models():
    print('helo',m.name, m.supported_generation_methods)

model = genai.GenerativeModel("gemini-2.5-flash")

response = model.generate_content("How do you play spikeball")

print(response.text)