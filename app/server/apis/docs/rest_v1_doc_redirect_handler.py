from server.apis.endpoint import Endpoint


class RestV1DocumentationRedirectHandler(Endpoint):
    def set_default_headers(self):
        super().set_default_headers()

        self.add_header("Allow", "GET")

    def get(self, path):
        doc_url = "http://opserv.org/docs/apis/rest/v1/data"

        sub_paths = path[1:].split("/")
        parts = len(sub_paths)

        if parts >= 1:
            sub_paths[0] = "component_type"
        if parts >= 2:
            sub_paths[1] = "component_arg"
        if parts >= 3:
            sub_paths[2] = "metric"

            path = "/" + "/".join(sub_paths)

        if path is not None:
            doc_url += path

        self.redirect(doc_url)
