from app.core.context import CriteriaContext, MessageEntry
from pydantic import BaseModel

class SpeechRateData(BaseModel):
    data: dict[str, float]

def speech_rate_evaluate(segments, criteria_context: CriteriaContext, message_entry: MessageEntry) -> SpeechRateData:    
    all_words = []

    for segment in segments:
        for word in segment.words:
            all_words.append(word)

    total_words = len(all_words)

    total_duration = all_words[-1].end - all_words[0].start

    words_per_second = total_words / total_duration

    VOWELS = "aeiouyáéíóúůýě"

    def count_syllables(word):
        word = word.lower()
        return sum(1 for char in word if char in VOWELS)

    total_syllables = 0

    for word in all_words:
        total_syllables += count_syllables(word.word)

    syllables_per_second = total_syllables / total_duration

    PAUSE_THRESHOLD = 0.5

    pauses = []

    for i in range(len(all_words) - 1):

        current_word = all_words[i]
        next_word = all_words[i + 1]

        pause_duration = next_word.start - current_word.end

        if pause_duration > PAUSE_THRESHOLD:
            pauses.append(pause_duration)


    pause_count = len(pauses)

    average_pause = (
        sum(pauses) / len(pauses)
        if pauses else 0
    )

    total_pause_time = sum(pauses)

    silence_ratio = total_pause_time / total_duration

    return SpeechRateData(data={
        "words_per_second": words_per_second,
        "syllables_per_second": syllables_per_second,
        "pause_count": pause_count,
        "average_pause_duration": average_pause,
        "silence_ratio": silence_ratio
    })