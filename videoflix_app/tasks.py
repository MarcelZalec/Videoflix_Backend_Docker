import subprocess
import os
from core import settings
from pathlib import Path

ffmpeg_path = r'/usr/bin/ffmpeg'
RESOLUTIONS = {
    '240p': 'scale=426:240',
    '360p': 'scale=640:360',
    '480p': 'scale=854:480',
    '720p': 'scale=1280:720',
    '1080p': 'scale=1920:1080',
}


def convert_240p(source):
    """
    Converts a video to 240p resolution using FFmpeg.

    :param source: Path to the original video file
    """
    target = remove_mp4_from_string(source) + '_240p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd240 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)


def convert_480p(source):
    """
    Converts a video to 480p resolution using FFmpeg.

    :param source: Path to the original video file
    """
    target = remove_mp4_from_string(source) + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)


def convert_720p(source):
    """
    Converts a video to 720p resolution using FFmpeg.

    :param source: Path to the original video file
    """
    target = remove_mp4_from_string(source) + '_720p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)
    # new_file_name = source + '_720p.mp4'
    # cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file)
    # run = subprocess.run(cmd, capture_output=True)


def convert_1080p(source):
    """
    Converts a video to 1080p resolution using FFmpeg.

    :param source: Path to the original video file
    """
    target = remove_mp4_from_string(source) + '_1080p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, target)
    subprocess.run(cmd)


def remove_mp4_from_string(s):
    """
    Removes the .mp4 file extension from the input string.

    :param s: Filename as a string
    :return: Filename without .mp4 extension
    """
    s:str = s
    return s.replace('.mp4', '')


def get_thumbnail(video_path):
    """
    Extracts a thumbnail image from a video using FFmpeg.

    :param video_path: Path to the source video file
    :return: Result of the subprocess call (or None if failed)
    """
    thumbnail_name = os.path.basename(video_path).replace('.mp4', '.png')
    output_image_path = os.path.join(settings.THUMBNAIL_FOLDER, thumbnail_name)
    
    
    try:
        os.makedirs(settings.THUMBNAIL_FOLDER, exist_ok=True)
        # FFmpeg Befehl erstellen
        command = [
            'ffmpeg',
            '-i', video_path,  # Eingabevideo
            '-ss', '0:00:01.000',  # Sprung zu der Anfangszeit (1 Sekunden)
            '-vframes', '1',  # Extrahiere nur ein Bild
            '-f', 'image2',  # Ausgabeformat (PNG)
            output_image_path  # Pfad für das Ausgabelbild
        ]

        # FFmpeg ausführen
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        print("Erstes Bild erfolgreich extrahiert.")
        
        return output_image_path

    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Extrahieren des Bildes: {e}")
    except FileNotFoundError:
        print("FFmpeg nicht gefunden. Bitte installieren.")


def run_ffmpeg_command(cmd):
    """
    Runs an ffmpeg command, checks for errors and prints them if there are any
    :param cmd: The list of arguments to pass to ffmpeg
    :return: The return code of the ffmpeg command
    """
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr.decode()}")
    return result.returncode


def convert_video_to_hls(v_path):
    """
    Converts a video file to multiple HLS streams with different resolutions.

    This function takes a video file path, and for each predefined resolution,
    creates an HLS (HTTP Live Streaming) output directory containing the playlist
    and segment files. The conversion is performed using ffmpeg with specified
    video and audio codecs.

    :param video_path: The file path of the input video to be converted.
    """
    basename = os.path.splitext(v_path)[0]
    
    for res, scale in RESOLUTIONS.items():
        output_dir = f"{basename}_{res}_hls"
        os.makedirs(output_dir, exist_ok=True)
        
        hls_playlist = os.path.join(output_dir, f"index.m3u8")

        cmd = [
            'ffmpeg', '-i', v_path,
            '-vf', scale,
            '-c:v', 'libx264', '-crf', '23',
            '-c:a', 'aac', '-strict', '-2',
            '-f', 'hls',
            '-hls_time', '5',
            '-hls_playlist_type', 'vod',
            hls_playlist
        ]

        return_code = run_ffmpeg_command(cmd)
        if return_code != 0:
            print(f"Error: Failed to convert video to {res}")


def process_video(inst):
    """
    Job to convert a Video instance's video_file to HLS (HTTP Live Streaming)
    format.

    The function takes an instance of the Video model as an argument, checks if
    the video file exists, and if yes, converts it to HLS format using ffmpeg.

    The converted video is saved in separate folders with the same name as the
    original video but with the appended resolution (e.g. "video_240p_hls").
    
    - Deletes the original video file after processing

    :param instance: An instance of the Video model
    :return: None
    """
    if not os.path.exists(inst.video_file.path):
        return
    convert_video_to_hls(inst.video_file.path)
    
    if not inst.thumbnail or inst.thumbnail == '':
        thumbnail_path = get_thumbnail(inst.video_file.path)
    
    if inst.video_file:
        if thumbnail_path:
            relative_path = Path(thumbnail_path).relative_to(settings.MEDIA_ROOT)
            inst.thumbnail = relative_path.as_posix()
        inst.save()
        try:
            if inst.video_file.path.lower().endswith('.mp4') and os.path.isfile(inst.video_file.path):
                os.remove(inst.video_file.path)
                print("Datei erfolgreich gelöscht.")
            else:
                print("Datei nicht gefunden oder kein .mp4")
        except Exception as e:
            print("Fehler beim Löschen:", e)