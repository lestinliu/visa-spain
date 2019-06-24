plan = [[1, 1], 1, [1, [1, 1]]]


def dream_come_try(dream: str):
    dream_results = understand_dream(dream)
    actions = investigate_dream(dream_results)
    plan = make_plan(actions)
    for action in plan:
        make_physical_action(action)


def understand_dream(dream) -> list:
    rusult_of_dream = []
    parts = input()
    for part in parts.split(";"):
        rusult_of_dream.append(part)
    return rusult_of_dream  # [part1, part2, part3]

def investigate_dream(dream_results):
    how_to_make_part_come_true = []
    for part in dream_results:
        print("search how people reach this goal")

def make_plan(actions):
    planned_actions = {}
    for action in actions:
        if len(action) == 1:
            planned_actions
        else:
            for a in:

    return planned_actions
