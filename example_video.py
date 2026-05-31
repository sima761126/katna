import os
import os.path
import cv2
import sys, getopt
from Katna.video import Video
from Katna.writer import KeyFrameDiskWriter
import multiprocessing
import ntpath
#from icecream import install
#install()


class CustomDiskWriter(KeyFrameDiskWriter):
    """

    :param KeyFrameDiskWriter: Writer class to overwrite
    :type KeyFrameDiskWriter: Writer
    """

    def generate_output_filename(self, filepath, keyframe_number):
        """Custom output filename method

        :param filepath: [description]
        :type filepath: [type]
        """
        filename = super().generate_output_filename(filepath, keyframe_number)

        suffix = "keyframe"

        return "_".join([filename, suffix])


def get_video_duration(video_path):
    """获取视频时长（秒）"""
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"无法打开视频文件: {video_path}")

    # 获取总帧数
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    # 获取帧率
    fps = cap.get(cv2.CAP_PROP_FPS)
    # 计算时长（秒）
    duration_seconds = total_frames / fps if fps > 0 else 0
    cap.release()

    return duration_seconds

def calculate_keyframe_count(video_path, frames_per_minute=2):
    """
    根据视频时长计算应提取的关键帧数量

    Args:
        video_path: 视频文件路径
        frames_per_minute: 每分钟提取的关键帧数，默认2张

    Returns:
        int: 关键帧数量（至少为1）
    """
    duration_seconds = get_video_duration(video_path)
    duration_minutes = duration_seconds / 60

    # 计算总帧数 = 分钟数 × 每分钟帧数
    frame_count = int(duration_minutes * frames_per_minute)

    # 确保至少提取1帧
    frame_count = max(frame_count, 1)

    # 打印详细信息
    print(f"视频时长: {duration_minutes:.2f} 分钟 ({duration_seconds:.2f} 秒)")
    print(f"提取规则: 每 {60 / frames_per_minute:.1f} 秒提取1张关键帧")
    print(f"应提取关键帧数: {frame_count} 张")

    return frame_count


def main_dir():
    if len(sys.argv) ==1:
        dir_path = os.path.join(".", "tests", "data")
    else:
        dir_path = sys.argv[1]

    vd = Video()

    no_of_frames_to_returned = calculate_keyframe_count(dir_path, frames_per_minute=2) # 12
    print('key frames:',no_of_frames_to_returned)
    diskwriter = KeyFrameDiskWriter(location="selectedframes")

    vd.extract_keyframes_from_videos_dir(
        no_of_frames=no_of_frames_to_returned, dir_path=dir_path,
        writer=diskwriter
    )    


def main():

    # Extract specific number of key frames from video
    # if os.name == 'nt':
    #     multiprocessing.freeze_support()

    if len(sys.argv) ==1:
        video_file_path = os.path.join(".", "tests", "data", "38623576720-1-192.mp4")
    else:
        video_file_path = sys.argv[1]
       
    vd = Video()

    # number of images to be returned
    no_of_frames_to_returned = calculate_keyframe_count(video_file_path, frames_per_minute=1)  # 12

    diskwriter = KeyFrameDiskWriter(location="selectedframes")

    # VIdeo file path
    #video_file_path = os.path.join(".", "tests", "data", "pos_video.mp4")
    print(f"Input video file path = {video_file_path}")

    vd.extract_video_keyframes(
        no_of_frames=no_of_frames_to_returned, file_path=video_file_path,
        writer=diskwriter
    )


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    main()
    #main_dir()
