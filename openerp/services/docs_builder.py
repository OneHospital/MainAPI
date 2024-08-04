class DocsBuilder:
    def __init__(self, app_list: list[dict]):
        self.app_list = app_list
        self.docs = ""

        self.build_docs()

    def build_docs(self):
        print(f"Building docs")
        for app_dict in self.app_list:
            name = app_dict['title']
            docs_path = f"/{app_dict['name']}/docs"

            docs = f"\n**{name}**: [Docs]({docs_path})\n"
            self.docs += docs
