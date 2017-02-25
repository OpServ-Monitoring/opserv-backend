import os

from tornado.web import StaticFileHandler


class ExtensionlessStaticFileHandler(StaticFileHandler):
    """
    Taken from here: https://gist.github.com/waylan/eccb46e932444fb6c678
    All credit goes to the author.

    A static file handler which serves static content from a directory.

    In addition to the behavior of the default StaticFileHandler,
    provision is made to serve extensionless files. For example,
    if ``default_extension`` is set to ``.html`` and the url
    ``foo/bar`` is requested, the file `foo/bar.html`` will be
    served if it exists.
    """

    def __init__(self, application, request, **kwargs):
        self.default_extension = None

        super().__init__(application, request, **kwargs)

    def initialize(self, path, default_filename=None, default_extension=None):
        super(ExtensionlessStaticFileHandler, self).initialize(path, default_filename)

        self.default_extension = default_extension

    def validate_absolute_path(self, root, absolute_path):
        """
        Validate and return the absolute path.

        Same behavior as parent StaticFileHandler class, except that
        if the file is not found and does not have a file extension,
        a file extension is appended to the filename and another
        attempt is made to find the file.
        """
        if (self.default_extension is not None and
                not os.path.exists(absolute_path) and
                    os.path.splitext(absolute_path)[1] == '' and
                os.path.exists(absolute_path + self.default_extension)):
            # Append self.default_extension to extensionless file name.
            absolute_path += self.default_extension
        return super(ExtensionlessStaticFileHandler, self).validate_absolute_path(root, absolute_path)
