import os
import urllib.request
import fiftyone as fo

VIDEO_MAP = {
    "https://huggingface.co/datasets/bhatanerohan/MarketingVideos/resolve/main/lux_06_mercedes.mp4": "69cfff9fff83935c54b822a1",
    "https://huggingface.co/datasets/bhatanerohan/MarketingVideos/resolve/main/lux_07_chanel.mp4": "69cfffb125007b94683968ec",
    "https://huggingface.co/datasets/bhatanerohan/MarketingVideos/resolve/main/lux_08_apple_air.mp4": "69cfffc4515d2f23431167ad",
    "https://huggingface.co/datasets/bhatanerohan/MarketingVideos/resolve/main/sport_01_nike_sowin.mp4": "69cfffd6ff83935c54b822c6",
    "https://huggingface.co/datasets/bhatanerohan/MarketingVideos/resolve/main/sport_02_nike_winning.mp4": "69cfffe925007b9468396907",
    "https://huggingface.co/datasets/bhatanerohan/MarketingVideos/resolve/main/ugc_08_honey.mp4": "69cffffc515d2f23431167d1",
}

INDEX_ID = "69cfff9fff83935c54b822a0"
DATASET_NAME = "ad-campaign-refs"
VIDEO_DIR = os.path.join(os.path.dirname(__file__), "videos")
os.makedirs(VIDEO_DIR, exist_ok=True)


def download_videos():
    for url in VIDEO_MAP:
        filename = url.split("/")[-1]
        local_path = os.path.join(VIDEO_DIR, filename)
        if not os.path.exists(local_path):
            print(f"  Downloading {filename}...")
            urllib.request.urlretrieve(url, local_path)
        else:
            print(f"  {filename} already downloaded")


if DATASET_NAME in fo.list_datasets():
    fo.delete_dataset(DATASET_NAME)

print("Downloading videos locally...")
download_videos()

dataset = fo.Dataset(DATASET_NAME, persistent=True)
for url, vid_id in VIDEO_MAP.items():
    filename = url.split("/")[-1]
    local_path = os.path.join(VIDEO_DIR, filename)
    sample = fo.Sample(filepath=local_path)
    sample["twelvelabs_video_id"] = vid_id
    sample["source_url"] = url
    dataset.add_sample(sample)

dataset.info["index_id"] = INDEX_ID
dataset.save()
print(f"Dataset ready: {len(dataset)} samples\n")

session = fo.launch_app(dataset)
session.wait()
