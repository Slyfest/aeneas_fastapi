from aeneas.executetask import ExecuteTask
from aeneas.task import Task
import boto3
import os
import glob
import json

s3 = boto3.client("s3")


def load_audio(bucket_id, sub_dir, file_name):
    key = f"{sub_dir}/{file_name}"
    s3.download_file(bucket_id, key, "data/audio.wav")


def prepare_text(text):
    sentences = [x.strip() for x in text.split(".") if x != ""]
    with open("data/transcript.txt", "w") as f:
        for sentence in sentences:
            f.write(sentence + "\n")


def clean_dir():
    for file in glob.glob("data/*"):
        os.remove(file)


def force_align():
    WORK_DIR = os.path.abspath("data")
    conf = "task_language=rus|is_text_type=plain|os_task_file_format=json"

    task = Task(config_string=conf)
    task.audio_file_path_absolute = f"{WORK_DIR}/audio.wav"
    task.text_file_path_absolute = f"{WORK_DIR}/transcript.txt"

    ExecuteTask(task).execute()
    return json.loads(task.sync_map.json_string)["fragments"]
