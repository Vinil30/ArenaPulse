import os
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()


class ImageforArenaPulse:
    def __init__(self):
        self.api_key = os.environ.get("HF_API_KEY")
        if not self.api_key:
            raise ValueError("HF_API_KEY not found")

        # Proper Inference Client (2026 supported way)
        self.client = InferenceClient(
            provider="hf-inference",
            api_key=self.api_key,
        )

        # Use a publicly hosted model
        self.model = "black-forest-labs/FLUX.1-schnell"

    def generate_image_arena(self, prompt: str, max_retries: int = 3):
        if not prompt or not prompt.strip():
            raise ValueError("Image prompt is empty")

        for attempt in range(max_retries):
            try:
                print(f"Generating image via HF Inference (attempt {attempt+1}/{max_retries})...")

                image = self.client.text_to_image(
                    prompt=prompt,
                    model=self.model,
                    height=1280,
                    width=720,
                )

                # It already returns PIL.Image
                return image

            except Exception as e:
                print(f"⚠ Attempt {attempt+1} failed: {e}")

        raise RuntimeError("Image generation failed after retries")