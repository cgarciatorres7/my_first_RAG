from pathlib import Path


class _Directories:

    def __init__(self):
        self.project = Path(__file__).parents[2].resolve()
        self.config = self.project / 'config'
        self.src = self.project / 'src'
        self.notebooks = self.project / 'notebooks'
        self.data = self.project / 'data'
        self.raw = self.data / 'raw'
        self.processed = self.data / 'processed'
        self.output = self.data / 'output'

        for dir_path in vars(self).values():
            try:
                dir_path.mkdir(exist_ok=True, parents=True)
            except Exception as e:
                # NOTE: could we just silently logger.error?
                raise OSError(
                    f"Either '{dir_path}' is not a directory, "
                    "or it can't be created. "
                    f"Make sure all attributes of {self.__class__} "
                    "are actual directory paths."
                ) from e


directories = _Directories()
