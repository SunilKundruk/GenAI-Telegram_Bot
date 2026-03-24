"""
Image description module — uses Gemini Vision API.
"""
from google import genai
from PIL import Image
import io
import config

class ImageDescriber:
    def __init__(self):
        self.client = genai.Client(api_key=config.GEMINI_API_KEY)

    def describe(self, image_bytes: bytes) -> dict:
        try:
            image = Image.open(io.BytesIO(image_bytes))
            prompt = "Analyze this image and provide a short caption and exactly 3 keyword tags.\nFormat: CAPTION: ... TAGS: tag1, tag2, tag3"
            response = self.client.models.generate_content(model=config.LLM_MODEL, contents=[prompt, image])
            return self._parse(response.text)
        except Exception as e:
            return {"caption": f"Error: {e}", "tags": []}

    def _parse(self, text: str) -> dict:
        caption, tags = text, ["image"]
        for line in text.strip().split('\n'):
            if line.upper().startswith('CAPTION:'): caption = line[8:].strip()
            elif line.upper().startswith('TAGS:'): tags = [t.strip() for t in line[5:].split(',')]
        return {"caption": caption, "tags": tags[:3]}
