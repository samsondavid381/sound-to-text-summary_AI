import streamlit as st
import openai
import speech_recognition as sr
from pydub import AudioSegment
import io

openai.api_key = 'APIKEY'

st.set_page_config(
    page_title="Speech Recognition and Summarization App",
    page_icon=":book:"
)

recognizer = sr.Recognizer()

st.title("Speech Recognition and Summarization App")

# Upload an audio file
st.radio('Select a function', ['Summarize','Translate','Create Similar'])
audio_file = st.file_uploader("Upload an audio file")

if audio_file is not None:
    st.write("File uploaded successfully!")

    # Convert the uploaded audio file to WAV format
    audio = AudioSegment.from_file(audio_file)
    audio = audio.set_channels(1)  # Set to mono channel
    audio = audio.set_frame_rate(16000)  # Set the sample rate to 16kHz
    wav_filename = "converted_audio.wav"
    audio.export(wav_filename, format="wav")

    with sr.AudioFile(wav_filename) as source:
        audio = recognizer.record(source)

    try:
        # Use the recognizer to transcribe the audio
        transcribed_text = recognizer.recognize_google(audio)
        st.write("Transcription:")
        st.write(transcribed_text)
    except sr.RequestError as e:
        st.error(f"Could not request results: {e}")
    except sr.UnknownValueError:
        st.error("Could not understand audio")

    if transcribed_text:
        st.subheader("Summary:")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a text-summarizer. Include points, formulas, methods, or other important information from the text in your summary. Write your response in list format, ordered from most important to least important."},
                {"role": "user", "content": "hello my name is David and I am testing this audio recognition for my app I want you to know that f equals m a is a very important formula for physics I also want you to know that inertia is the angular property of mass this is not so important but I like the book Dune"},
                {"role": "assistant", "content": "1. F = ma\n2. Inertia is the angular property of mass\n3.The author is David, he is testing the audio recognition feature of his app"},
                {"role": "user", "content": transcribed_text}
            ]
        )
        summary = response['choices'][0]['message']['content']
        st.write(summary)