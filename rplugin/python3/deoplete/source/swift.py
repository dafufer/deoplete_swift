from .base import Base
from deoplete.util import (error, error_vim, debug)

class Source(Base):
    def __init__(self, vim):
        from distutils.spawn import find_executable

        Base.__init__(self, vim)

        self.name = 'swift'
        self.mark = '[swift]'
        self.filetypes = ['swift']
        self.input_pattern = r'((?:\.|(?:,|:|->)\s+)\w*|\()'

        self.__spm = None
        self.__target = None
        self.__sdk = None

        try:
            if not find_executable("sourcekitten"):
                error(self.vim, 'Can not find sourcekitten, you need https://github.com/jpsim/SourceKitten')

            if not find_executable("swift") and self._check_xcode_path():
                error(self.vim, 'Can not find swift or XCode: https://swift.org')

        except Exception as ex:
            error(self.vim, ex)

    def _check_xcode_path(self):
        from distutils.spawn import find_executable
        import subprocess

        if find_executable("xcode-select"):
            try:
                return subprocess.check_output(['xcode-select', '-p'])
            except subprocess.CalledProcessError as ex:
                error(self.vim, ex)

        return None


    def on_init(self, context):
        self.__spm = self.vim.eval('deoplete_swift#get_spm_module()')
        self.__target = self.vim.eval('deoplete_swift#get_target()')
        self.__sdk = self.vim.eval('deoplete_swift#get_sdk()')

    def get_complete_position(self, context):
        import re

        result = re.compile(r'\w*$').search(context['input'])

        if result is None:
            return self.vim.eval('col(\'.\')') - 1

        return result.start()


    def gather_candidates(self, context):
        import subprocess
        import json

        lnum = self.vim.eval('line(\'.\')')
        col = context['complete_position'] + 1
        buf = self.vim.current.buffer[:]
        enc = self.vim.options['encoding']
        path = self.vim.call('expand', '%:p')
        if len(path) == 0:
            path = None

        content = '\n'.join(buf)

        offset = 0
        for row_current, text in enumerate(buf):
            if row_current < lnum - 1:
                offset += len(bytes(text, enc)) + 1
                offset += col - 1

        try:
            # Set sourcekitten arguments
            args = ['sourcekitten', 'complete', '--text', content.encode(enc), '--offset', str(offset)]
            if self.__spm:
                args += ['--spm-module', self.__spm]

            if self.__target or self.__sdk:
                args += ['--']

            if self.__target:
                args += ['-target', self.__target]

            if self.__sdk:
                args += ['-sdk', self.__sdk]

            # Run sourcekitten command
            output, _ = subprocess.Popen(
                args,
                stdout=subprocess.PIPE,
            ).communicate()

            json_list = json.loads(output.decode())

        except subprocess.CalledProcessError:
            return []

        matches = []
        for item in json_list:
            doc = ""
            if "docBrief" in item:
                doc = '\n' + item["docBrief"]

            kind = item['kind'].split('.')[-1]
            if kind == "free":
                kind = item['kind'].split('.')[-2]

            matches.append({
                'word': item['sourcetext'],
                'abbr': item['name'],
                'kind': kind,
                'dup': 1,
                'info': item['descriptionKey'] + doc,
            })

        return matches
