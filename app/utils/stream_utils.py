from dataclasses import dataclass


@dataclass
class CreateStreamRequest:
    streamName : str
    filePath : str
    fps : int
    resolution : str
    status : bool
    loopEnabled : bool