import jedi
import os
from .predictor import Predictor


class JediPredictor(Predictor):
    def predict(self, line, lineno, column, limit=None, path=None):
        if path is not None:
            path = os.path.abspath(os.path.split(path)[0])

        # Jedi uses 1-indexed lines and columns while our script uses 0-indexed lines and columns
        script = jedi.Script(line, lineno + 1, column + 1, sys_path=path)

        cs = []
        for c in script.completions():
            cs.append(c.complete)
        if limit is None:
            return cs
        else:
            return cs[:limit]
