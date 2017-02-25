from server.apis._api_management import ApiManagement
from server.apis.docs.doc_redirect_handler import DocumentationRedirectHandler
from server.apis.docs.rest_v1_doc_redirect_handler import RestV1DocumentationRedirectHandler


class DocumentationRedirectsManagement:
    @classmethod
    def get_handlers(cls) -> list:
        handlers = [
            ("/rest/v1/data((/[^/]+)+)/*", RestV1DocumentationRedirectHandler),
            ("((/[^/]+)+)/*", DocumentationRedirectHandler)
        ]

        return ApiManagement.add_prefix_to_handlers(
            "/docs",
            handlers
        )
