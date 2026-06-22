from dataclasses import dataclass


@dataclass
class CreateStreamRequest:
    stream_name : str
    file_path : str
    fps : str
    resolution : str
    status : str