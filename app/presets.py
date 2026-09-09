PRESETS={"cinematic":"cinematic lighting, dramatic composition","realistic":"photorealistic, natural detail","anime":"anime style, expressive","product":"clean product photography","portrait":"professional portrait"}
def apply(prompt,preset=""): return f"{prompt}. {PRESETS.get(preset,'')}".strip()
