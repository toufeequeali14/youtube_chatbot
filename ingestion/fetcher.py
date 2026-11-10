# YouTube transcript extraction & metadata parsing
import json

from youtube_transcript_api import YouTubeTranscriptApi

def get_video_transcript(video_id: str = None) -> list:


    try:

        yt_transcript_api = YouTubeTranscriptApi()

        transcript_list = yt_transcript_api.fetch(video_id, languages=["en", "hi"])

        raw_transcript = transcript_list.to_raw_data()

        # save the catched transcipt into json file for debugging
        with open("transcripts_list.json", "w") as f:
            json.dump(raw_transcript, f, indent=4, ensure_ascii=False)

        transcript = transcript_list[0]

        # flatten it into plain text
        transcript = " ".join(chunk.text for chunk in transcript_list)

        return transcript

    except Exception as exc:
        print(exc)
        return None
