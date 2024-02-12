from common.handlers.file_handler import FileHandler
from common.handlers.file_parser import FileParser
from common.time_utils import TimeUtils
from src.utility.stream_factory import StreamFactory
from src.model_handler import ModelHandler
from src.segment_mover import SegmentMover
from src.stream_merger import StreamMerger
from src.utility.template_parser import TemplateParser
from src.utility.video_factory import VideoFactory
from src.ffmpeg_handling.ffmpeg_api import FFMPEGAPI
from src.video_handler import VideoHandler


class MergeComponentContext:
    """A context class containing all required high-level components for the merge pipeline."""
    def __init__(self) -> None:
        _api: FFMPEGAPI = FFMPEGAPI()
        _file_parser: FileParser = FileParser()

        self._template_parser = TemplateParser()
        self._time_utils: TimeUtils = TimeUtils()
        self._file_handler: FileHandler = FileHandler()
        self._video_handler: VideoHandler = VideoHandler()
        self._video_factory: VideoFactory = VideoFactory(_file_parser, _api)
        self._stream_factory: StreamFactory = StreamFactory(self._template_parser)
        self._model_handler: ModelHandler = ModelHandler(_file_parser, self._file_handler)
        self._segment_mover: SegmentMover = SegmentMover(self._video_handler, self._template_parser, self._video_factory, _api)
        self._stream_merger: StreamMerger = StreamMerger(_api, self._video_handler, self._template_parser, self._segment_mover.move_path_based)

    @property
    def template_parser(self) -> TemplateParser: 
        return self._template_parser

    @property
    def time_utils(self) -> TimeUtils: 
        return self._time_utils

    @property
    def video_factory(self) -> VideoFactory: 
        return self._video_factory

    @property
    def segment_mover(self) -> SegmentMover: 
        return self._segment_mover

    @property
    def stream_merger(self) -> StreamMerger: 
        return self._stream_merger

    @property
    def model_handler(self) -> ModelHandler:
        return self._model_handler
    
    @property
    def file_handler(self) -> FileHandler:
        return self._file_handler

    @property
    def video_handler(self) -> VideoHandler:
        return self._video_handler

    @property
    def stream_factory(self) -> StreamFactory:
        return self._stream_factory
