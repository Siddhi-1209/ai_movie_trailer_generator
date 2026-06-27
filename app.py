import streamlit as st
import google.generativeai as genai
client = genai.Client(api_key="GEMINI_API_KEY")
st.write("Connected successfully!")
client = genai.Client(api_key="GEMINI_API_KEY")

models = client.models.list()

for model in models:
    st.write(model.name)
    break
movie_title = input("🎬 Enter Movie Title: ")
genre = input("🎭 Enter Genre: ")
prompt = f"""
Generate a short movie story.

Movie Title: {movie_title}
Genre: {genre}

The story should be exciting, cinematic, and suitable for a movie trailer.
Keep it within 150 words.
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

st.write(response.text)
trailer_prompt = f"""
Based on the movie story below, generate a cinematic movie trailer.

Movie Story:
{response.text}

Provide the output in the following format:

Scene 1:
Visual:

Narration:

Scene 2:
Visual:

Narration:

Scene 3:
Visual:

Narration:

Background Music Mood:
"""
trailer_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=trailer_prompt
)

st.write(trailer_response.text)
narration_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=narration_prompt
)

st.write(narration_response.text)
import edge_tts
import asyncio

voice_text = narration_response.text

async def generate_voice():
    communicate = edge_tts.Communicate(
        text=voice_text,
        voice="en-US-GuyNeural"
    )

    await communicate.save("/content/sample_data/trailer_voice.mp3")

await generate_voice()

st.write("Voice-over generated successfully!")
image_prompt_request = f"""
From the trailer below, extract the first 3 scenes.

For each scene, create a highly detailed cinematic image generation prompt.

The prompt should include:
- Environment
- Lighting
- Camera angle
- Mood
- Cinematic details

Return the output in the following format:

Scene 1 Prompt:
...

Scene 2 Prompt:
...

Scene 3 Prompt:
...

Trailer:

{trailer_response.text}
"""
image_prompt_response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=image_prompt_request
)

image_prompts = image_prompt_response.text

st.write(image_prompts)
import moviepy

st.write(moviepy.__version__)
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)

st.write("MoviePy imported successfully!")
from PIL import Image

for img_file in [
    "/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg",
    "/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg",
    "/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg"
]:
    img = Image.open(img_file)
  st.write(img_file, img.size)
from moviepy.editor import AudioFileClip

audio = AudioFileClip("/content/sample_data/trailer_voice.mp3")

st.write("Duration:", audio.duration)
from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)

# Load narration
audio = AudioFileClip("/content/sample_data/trailer_voice.mp3")

# Calculate duration per scene
scene_duration = audio.duration / 3

# Create image clips
clip1 = ImageClip("/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg").set_duration(scene_duration)
clip2 = ImageClip("/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg").set_duration(scene_duration)
clip3 = ImageClip("/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg").set_duration(scene_duration)

# Combine clips
video = concatenate_videoclips([clip1, clip2, clip3])

# Add narration
video = video.set_audio(audio)

# Export
video.write_videofile(
    "final_movie_trailer.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
from IPython.display import Video

Video("final_movie_trailer.mp4", embed=True)
def zoom_out_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = get_frame(t)

        import cv2
        import numpy as np

        h, w = img.shape[:2]

        scale = 1 + zoom_ratio * (clip.duration - t)

        new_w = int(w / scale)
        new_h = int(h / scale)

        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2

        cropped = img[y1:y1+new_h, x1:x1+new_w]

        return cv2.resize(cropped, (w, h))

    return clip.fl(effect)
  def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = get_frame(t)

        import cv2

        h, w = img.shape[:2]

        scale = 1 + zoom_ratio * t

        new_w = int(w / scale)
        new_h = int(h / scale)

        x1 = (w - new_w) // 2
        y1 = (h - new_h) // 2

        cropped = img[y1:y1+new_h, x1:x1+new_w]

        return cv2.resize(cropped, (w, h))

    return clip.fl(effect)
    from moviepy.editor import (
    ImageClip,
    AudioFileClip,
    concatenate_videoclips
)

audio = AudioFileClip(
    "/content/sample_data/trailer_voice.mp3"
)

scene_duration = audio.duration / 3

clip1 = ImageClip(
    "/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg"
).set_duration(scene_duration)

clip1 = zoom_in_effect(clip1)

clip2 = ImageClip(
    "/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg"
).set_duration(scene_duration)

clip2 = zoom_out_effect(clip2)

clip3 = ImageClip(
    "/content/sample_data/WhatsApp Image 2026-06-27 at 13.36.16.jpeg"
).set_duration(scene_duration)

clip3 = zoom_in_effect(clip3)

# Fade transitions
clip1 = clip1.fadein(1).fadeout(1)
clip2 = clip2.fadein(1).fadeout(1)
clip3 = clip3.fadein(1).fadeout(1)

video = concatenate_videoclips(
    [clip1, clip2, clip3],
    method="compose"
)

video = video.set_audio(audio)

video.write_videofile(
    "cinematic_trailer.mp4",
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
from IPython.display import Video

Video("cinematic_trailer.mp4", embed=True)
