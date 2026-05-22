from faster_whisper import WhisperModel

whisper_model = WhisperModel("medium", device="cuda", compute_type="int8")
