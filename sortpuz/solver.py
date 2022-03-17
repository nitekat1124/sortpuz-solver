from collections import defaultdict, deque


class Solver:
    def __init__(self, level, quicker=False):
        self.level = level
        self.quicker = quicker

        self.mapping, self.bottles = self.read_level_data()
        self.w = len(self.bottles)
        self.h = len(self.bottles[0])
        self.check_data()

        self.history = None
        self.print_state = {"index": -1, "prev": None}

    def read_level_data(self):
        with open(f"levels/level_{self.level}.txt", "r") as f:
            data = [line.strip() for line in f.readlines()]
        return self.parse_data(data)

    def parse_data(self, data):
        mapping = {".": "empty"}
        bottles = [[color for color in line[1:-1].split(",")] for line in data if line[0] == "[" and line[-1] == "]"]
        colors = set([color for bottle in bottles for color in bottle]) - {"empty"}
        for color in colors:
            mapping[chr(len(mapping) + 64)] = color

        mapping_reverse = {v: k for k, v in mapping.items()}
        bottles_symbol = [[mapping_reverse[b] for b in row] for row in bottles]

        return mapping, bottles_symbol

    def check_data(self):
        state = self.serialize(self.bottles)
        types = set(state) - {"."}
        for t in types:
            if state.count(t) != self.h:
                raise Exception(f"Invalid data. {self.mapping[t]} is not a valid color.")

    def solve(self):
        self.print_bottles()

        state = self.serialize(self.bottles)
        seen = {state: 0}
        queue = deque([(state, 0, [state])])

        while queue:
            state, steps, history = queue.popleft()

            if self.valid(state):
                self.history = history
                self.print_history()
                return True
            else:
                next_states = self.next_states(state)
                for next_state in next_states:
                    if next_state not in seen or seen[next_state] > steps + 1:
                        seen[next_state] = steps + 1
                        if self.quicker:
                            queue.appendleft((next_state, steps + 1, history + [next_state]))
                        else:
                            queue.append((next_state, steps + 1, history + [next_state]))

    def serialize(self, bottles):
        return "".join([color for bottle in bottles for color in bottle])

    def valid(self, state):
        bottles = [list(state[i * self.h : (i + 1) * self.h]) for i in range(self.w)]
        for bottle in bottles:
            if len(set(bottle)) != 1:
                return False
        return True

    def next_states(self, state):
        new_states = []

        for i in range(self.w):
            for j in range(self.w):
                if i == j:
                    continue

                bottles = [list(state[i * self.h : (i + 1) * self.h]) for i in range(self.w)]
                elem_pos_i = [x for x, v in enumerate(bottles[i]) if v != "."]
                elem_pos_j = [x for x, v in enumerate(bottles[j]) if v != "."]

                max_amount = 1
                for k in range(1, len(elem_pos_i)):
                    if bottles[i][elem_pos_i[k]] == bottles[i][elem_pos_i[0]]:
                        max_amount += 1
                    else:
                        break

                if len(elem_pos_i) == 0:
                    continue

                if len(elem_pos_i) == 4 and len(set(bottles[i])) == 1:
                    continue

                if len(elem_pos_j) == self.h:
                    continue

                if len(elem_pos_j) == 0 and max_amount == len(elem_pos_i):
                    continue

                if self.h - len(elem_pos_j) < max_amount:
                    continue

                ci = bottles[i][elem_pos_i[0]]
                candidates = [x for x, v in enumerate(bottles) if set(v) - {"."} == {ci}]
                if len(candidates) and j not in candidates:
                    continue

                cj = bottles[j][elem_pos_j[0]] if len(elem_pos_j) else "."
                if len(elem_pos_j) == 0 or ci == cj:
                    for k in range(min(max_amount, self.h - len(elem_pos_j))):
                        bottles[i][elem_pos_i[k]] = "."
                        bottles[j][(elem_pos_j[0] if len(elem_pos_j) else self.h) - 1 - k] = ci

                    new_states += [self.serialize(bottles)]

        return new_states

    def print_history(self):
        for state in self.history[1:]:
            bottles = [list(state[i * self.h : (i + 1) * self.h]) for i in range(self.w)]
            self.print_bottles(bottles)

    def print_bottles(self, bottles=None):
        output = []
        size = max(len(i) for i in self.mapping.values()) + 2
        if bottles is None:
            bottles = self.bottles

        self.print_state["index"] += 1
        if self.print_state["index"] == 0:
            output += ["\nthe puzzle:"]
        else:
            output += [f"step {self.print_state['index']}:"]

        move_pos = [0, 0]
        for pos in range(self.h):
            line = ""
            for i in range(self.w):
                text = self.mapping[bottles[i][pos]]
                is_moved = "\033[7m" if self.print_state["prev"] is not None and bottles[i][pos] != self.print_state["prev"][i][pos] else ""
                line += is_moved + self.colorize(text) + " " * (size - len(text))
                if is_moved:
                    move_pos[text != "empty"] = i + 1
            output += [line]
        if sum(move_pos):
            output[0] += f" move from {move_pos[0]} to {move_pos[1]}"

        self.print_state["prev"] = bottles
        print(*output + [""], sep="\n")

    def colorize(self, text):
        colors = defaultdict(lambda: "\033[0m")
        colors["empty"] = "\033[38;2;96;96;96m"

        colors["red"] = "\033[38;2;255;0;0m"
        colors["brown"] = "\033[38;2;139;69;19m"

        colors["orange"] = "\033[38;2;255;165;0m"
        colors["yellow"] = "\033[38;2;255;255;0m"
        colors["gold"] = "\033[38;2;255;215;0m"

        colors["green"] = "\033[38;2;34;139;34m"
        colors["lime"] = "\033[38;2;0;255;0m"
        colors["olive"] = "\033[38;2;107;142;35m"

        colors["blue"] = "\033[38;2;0;128;255m"
        colors["cyan"] = "\033[38;2;0;255;255m"

        colors["violet"] = "\033[38;2;186;85;211m"
        colors["pink"] = "\033[38;2;255;192;255m"

        colors["gray"] = "\033[38;2;192;192;192m"

        return colors[text.strip()] + text + "\033[0m"
