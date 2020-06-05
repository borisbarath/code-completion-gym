

class Counter():

    def count_keystrokes(self, file, limit, model=None):
        f = open(file, "r")
        text = ''.join(f.readlines())

        if model is None:
            return self.count_keystrokes_base(text)

        return(self.count_keystrokes_predictor(text, model, limit, f) / self.count_keystrokes_base(text))

    def count_keystrokes_base(self, text):
        return len(text)

    def count_keystrokes_predictor(self, function, predictor, limit, file):
        keystrokes = 0
        lines = function.split("\n")
        for lineno, line in enumerate(lines):
            line_len = len(line)

            if lineno == len(lines) - 1 and line_len == 0:
                break
            if line_len == 0:
                keystrokes += 1
                continue

            line = line + "\n"
            keystrokes += 1

            columns = [i for i in range(line_len)]
            line_iter = iter(columns)

            for i in line_iter:

                # skip whitespace
                if line[i] in "\t\"\' .,/*&#[]()}{:":
                    keystrokes += 1
                    continue
                keystrokes += 1
                # row always == 1 as processing row by row
                code_so_far = line[:i+1]

                if lineno > 0:
                    code_so_far = '\n'.join(lines[:lineno]) + '\n' + line[:i+1]

                try:
                    cs = predictor.predict(
                        code_so_far, lineno, i, limit=limit, path=file.name)
                except:
                    cs = []

                for completion_index, comp in enumerate(cs):
                        # if current + completion is shorther than line
                    if line_len >= i + len(comp):
                        # if the sequence expected matches the completion
                        if line[i+1:i+1+len(comp)] == comp and len(comp) != 0:
                            # completion_index indicates how many arrow presses to select correct prediction
                            if len(comp) > completion_index + 1:
                                keystrokes += completion_index + 1
                                for _ in range(len(comp)):
                                    next(line_iter)
                                break

        return keystrokes
