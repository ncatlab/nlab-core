import mistletoe.span_token
import os
import re
import subprocess

from renderer.exception import SourceRendererException

class InlineLatexTokenRenderingException(SourceRendererException):
    def __init__(self, message):
        super().__init__(message)

"""
Matches anything within $ and $, and processes it with itex2MML
"""
class InlineLatexToken(mistletoe.span_token.SpanToken):
    pattern = re.compile(r"\$(.+?)\$")

    def __init__(self, match):
        self.latex = match.group(0)

    def render(self):
        latex_renderer_subprocess = subprocess.run(
            os.environ["NLAB_DEPLOYED_RUN_COMMAND_FOR_LATEX_COMPILER"].split(),
            capture_output = True,
            text = True,
            check = True,
            input = self.latex)
        rendered_latex = latex_renderer_subprocess.stdout
        if "<merror>" in rendered_latex:
            raise InlineLatexTokenRenderingException(
                "LaTeX syntax error in following: " +
                self.latex)
        return rendered_latex
