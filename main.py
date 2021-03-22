
import json

IF = "if"
THEN = "then"
FINAL = "final"

asked = []
partial_conclusions = []
final_conclusions = []


def got_fired(rule):
    return rule[THEN] in partial_conclusions


def evaluate_premises(premises):
    for premise in premises:
        # TODO: check for keywords like OR, AND
        # check for >, < inside of string of atomic rule
        if not (premise in partial_conclusions):
            # for the moment there's an AND between the premises
            return False

    return True

# documentatie de max 3 pagini: ce tehn am folosit, o pagina de user guide si o pagina de descriere a proiectuluil (a codului)


def ask_question():
    for rule in rules:
        if not (rule[THEN] in asked) and not (rule[THEN] in partial_conclusions):
            # TODO: ask just one part of if
            print(' AND '.join(rule[IF]) + "?")
            answer = input()
            if answer == "True":
                partial_conclusions.append(rule[THEN])
                return

    print("TODO: NO MORE QUESTIONS LEFT, start asking again")
    return


if __name__ == '__main__':

    with open('knowledge_base.json') as file:
        rules = json.load(file)
        # print(rules)

    # loop until we get to a conclusion
    while True:
        no_change = True
        for rule in rules:
            if got_fired(rule):
                continue
            # extract the premises
            premises = rule[IF]
            fire_rule = evaluate_premises(premises)
            if fire_rule:
                no_change = False
                # validate conclusion (add to partial_conclusions)
                if rule[FINAL]:
                    final_conclusions.append(rule[THEN])
                else:
                    partial_conclusions.append(rule[THEN])
            # check if we have any final conclusion? or maybe outside of for
            if final_conclusions:
                break
        if final_conclusions:
            break
        if no_change:
            ask_question()

    print("final conclusions: ", final_conclusions)
    # not yet sure how I'm going to have more final conclusions, but we'll see