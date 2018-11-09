import sublime
import sublime_plugin

import subprocess

import os

CABAL_DIR = os.path.join(os.path.expanduser('~'), '.cabal', 'bin')

PATH = os.environ.get('PATH', '')
if CABAL_DIR not in PATH:
    os.environ['PATH'] = CABAL_DIR + ':' + PATH


def worker(view, edit, region, text, encoding):

    p = subprocess.Popen(
        ['hindent'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE
    )

    output, stderr = p.communicate(text.encode(encoding))

    if p.returncode == 0:
        view.replace(edit, region, output.decode(encoding))


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
