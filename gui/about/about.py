from kivy.uix.screenmanager import Screen
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
import webbrowser


class AboutScreen(Screen):
    def __init__(self, **kw):
        self.opened_web_browser_dialog = MDDialog(
            title="Open Link",
            text="Your webbrowser has been opened. Continue there",
            buttons=[
                MDFlatButton(text="Ok", on_release=lambda _: self.opened_web_browser_dialog.dismiss()),
            ],
        )
        super().__init__(**kw)

    def goto(self, loc: str):
        if loc == "wiki":
            webbrowser.open('https://github.com/janishutz/BiogasControllerApp/wiki', new=2)
        elif loc == "issues":
            webbrowser.open('https://github.com/janishutz/BiogasControllerApp/issues', new=2)
        elif loc == "repo":
            webbrowser.open('https://github.com/janishutz/BiogasControllerApp', new=2)
        self.opened_web_browser_dialog.open()

Builder.load_file('./gui/about/about.kv')
