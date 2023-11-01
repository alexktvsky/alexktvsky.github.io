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




        # for project in projects:

        #     project_html = project_template.render(
        #         name=project['name'],
        #         year=project['year'],
        #         description=project['description'],
        #         buttons=self._render_buttons_for_project(project['buttons'])
        #     )

        #     result_list.append(project_html)

        #     print('[ProjectPage]: {}'.format(project['name']))

        # projects_html = projects_template.render(projects=''.join(result_list))

        # ProjectsPage._write_text_to_file(page_path, projects_html)



    # def _render_buttons_for_project(self, buttons):

    #     button_template = Template(
    #         ProjectsPage._read_text_file(
    #             ProjectsPage.ROOT_PATH / 'button.html.in'
    #         )
    #     )

    #     result_list = []

    #     # result_list.sort(key=lambda x: x['year'], reverse=True)

    #     for button in buttons:
    #         button_html = button_template.render(
    #             name=button['name'],
    #             url=button['url']
    #         )
    #         result_list.append(button_html)

    #     return ''.join(result_list)

