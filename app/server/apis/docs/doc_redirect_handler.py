from server.apis.endpoint import Endpoint


class DocumentationRedirectHandler(Endpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self, path, *trash):
        doc_url = "http://opserv.org/docs/apis"
        if path is not None:
            doc_url += path

        self.redirect(doc_url)
