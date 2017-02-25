from server.static_hosting.extensionless_static_file_handler import ExtensionlessStaticFileHandler


class StaticHostingManagement:
    @classmethod
    def get_handlers(cls) -> list:
        return [
            (
                "/(.*)/*",
                ExtensionlessStaticFileHandler,
                {
                    "path": "server/static_hosting/public",
                    "default_filename": "index.html",
                    "default_extension": ".html"
                }
            )
        ]
