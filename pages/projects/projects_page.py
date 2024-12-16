import json
from pathlib import Path
from mako.template import Template


class ProjectsPage:

    ROOT_PATH = Path('pages/projects')

    def render(self, page_path):
        template_path = ProjectsPage.ROOT_PATH / 'projects.html.in'
        template = Template(open(template_path).read())
        projects = json.load(open(ProjectsPage.ROOT_PATH / 'projects.json'))
        page = template.render(projects=projects)
        open(page_path, 'w').write(page)
