from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
import webbrowser


class AboutScreen(Screen):
    def report_issue(self):
        webbrowser.open('https://github.com/janishutz/BiogasControllerApp/issues', new=2)

Builder.load_file('./gui/about/about.kv')
