import streamlit as st
from google import genai
from google.genai import types
import wave
def wave_file(filename, pcm_data):
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)      
        wf.setframerate(24000) 
        wf.writeframes(pcm_data)
client = genai.Client(api_key="AIzaSyD1odZDB2nykk9js3EJ0-7jyvmDuF0DodM")
st.title("AI Text → Translation → Speech App")
text_input = st.text_area("Enter text")
language = st.selectbox("Select your desired language", ["Hindi", "Telugu", "French", "Spanish", "German"])
if st.button("Translate & Speak"):
    if not text_input.strip():
        st.warning("Please enter text")
    else:
        translate_prompt = f"Translate the following text into {language} without any extra text:\n{text_input}"
        translate_response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[translate_prompt]
        )
        translated_text = translate_response.text.strip()
        st.subheader("Translated Text")
        st.success(translated_text)
        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=[translated_text],
            config=types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=types.SpeechConfig(
                    voice_config=types.VoiceConfig(
                        prebuilt_voice_config=types.PrebuiltVoiceConfig(
                            voice_name="Kore"
                        )
                    )
                )
            )
        )
        pcm_data = response.candidates[0].content.parts[0].inline_data.data
        file_name = "out.wav"
        wave_file(file_name, pcm_data)
        with open(file_name, "rb") as f:
            st.audio(f.read(), format="audio/wav")