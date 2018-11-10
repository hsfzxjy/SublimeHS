import sublime
import sublime_plugin

import subprocess

import os

CABAL_DIR = os.path.join(os.path.expanduser('~'), '.cabal', 'bin')

PATH = os.environ.get('PATH', '')
if CABAL_DIR not in PATH:
    os.environ['PATH'] = CABAL_DIR + ':' + PATH

HINDENT_PANEL_NAME = 'haskell_hindent'


def worker(view, edit, region, text, encoding):

    hide_output(view, HINDENT_PANEL_NAME)

    p = subprocess.Popen(
        ['hindent'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output, error_output = p.communicate(text.encode(encoding))

    print(output, error_output)
    if p.returncode == 0:
        view.replace(edit, region, output.decode(encoding))
    else:
        show_output(view, HINDENT_PANEL_NAME, error_output.decode(encoding))


def hide_output(edit_view, panel_name):

    edit_view.window().run_command('hide_panel', {'panel': 'output.' + panel_name})


def show_output(edit_view, panel_name, message):
    print(message)
    output_panel = edit_view.window().create_output_panel(panel_name)
    output_panel.run_command('haskell_output_message', {'text': message})
    edit_view.window().run_command('show_panel', {'panel': 'output.' + panel_name})


class HaskellOutputMessage(sublime_plugin.TextCommand):

    def run(self, edit, text, **kwargs):

        if not text:
            return

        self.view.set_read_only(False)
        self.view.erase(edit, sublime.Region(0, self.view.size()))
        self.view.insert(edit, self.view.size(), text)
        self.view.set_read_only(True)


class HaskellHindentCommand(sublime_plugin.TextCommand):

    def get_selection(self):

        region = sublime.Region(0, self.view.size())

        return region, self.view.substr(region), self.view.encoding()

    def run(self, edit, *args):

        region, text, encoding = self.get_selection()  # noqa
        # threading.Thread(target=worker, args=(self.view, edit, region, text, encoding)).start()
        worker(self.view, edit, region, text, encoding)

    def is_enabled(self, *args):
        return 'haskell' in self.view.settings().get('syntax').lower()

    def is_visible(self, *args):
        return True
