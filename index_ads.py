import os
import sys
import fiftyone as fo
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
from ad_brief_copilot.twelvelabs_api import index_videos_from_urls

load_dotenv()

INDEX_NAME = "ad-campaign-refs"
DATASET_NAME = "ad-campaign-refs"

VIDEO_URLS = [
    # Paste your public video URLs here, one per line, e.g.:
    # "https://storage.googleapis.com/your-bucket/ad1.mp4",
    # "https://storage.googleapis.com/your-bucket/ad2.mp4",
]


def main():
    api_key = os.getenv("TWELVE_LABS_API_KEY")
    if not api_key:
        raise ValueError("TWELVE_LABS_API_KEY not set in .env")
    if not VIDEO_URLS:
        raise ValueError("Add at least one video URL to VIDEO_URLS before running")

    print(f"Indexing {len(VIDEO_URLS)} videos into Twelve Labs index '{INDEX_NAME}'...")
    print("This may take a few minutes per video — grab a coffee.\n")

    result = index_videos_from_urls(api_key, INDEX_NAME, VIDEO_URLS)
    index_id = result["index_id"]
    video_map = result["video_map"]

    succeeded = {url: vid for url, vid in video_map.items() if vid}
    failed = [url for url, vid in video_map.items() if not vid]

    print(f"Index ID : {index_id}")
    print(f"Indexed  : {len(succeeded)}/{len(VIDEO_URLS)} videos")
    if failed:
        print(f"Failed   : {len(failed)} video(s):")
        for url in failed:
            print(f"  - {url}")

    print("\nBuilding FiftyOne dataset...")
    dataset = fo.Dataset(DATASET_NAME, overwrite=True)
    for url, vid_id in succeeded.items():
        sample = fo.Sample(filepath=url)
        sample["twelvelabs_video_id"] = vid_id
        sample["source_url"] = url
        dataset.add_sample(sample)

    dataset.info["index_id"] = index_id
    dataset.save()

    print(f"Dataset  : '{DATASET_NAME}' — {len(dataset)} samples\n")
    print("Setup complete. Launch the app with:")
    print(f'  uv run python -c "import fiftyone as fo; fo.launch_app(fo.load_dataset(\'{DATASET_NAME}\'))"')
    print(f"\nYour Twelve Labs Index ID (you'll need this for search_ad_references): {index_id}")


if __name__ == "__main__":
    main()
