
import json

IF = "if"
THEN = "then"
FINAL = "final"


asked = []
partial_conclusions = []
false_conclusions = []
final_conclusions = []


def false_premise_present(premises):
    for premise in premises:
        if premise in false_conclusions:
            return True
    return False


def already_got_fired(rule):
    return rule[THEN] in partial_conclusions or rule[THEN] in false_conclusions or false_premise_present(rule[IF])


def evaluate_premises(premises, rule):
    for premise in premises:
        value = evaluate_premise(premise, rule)
        if not value:
            # for the moment there's an AND between the premises
            return False

    return True


def evaluate_premise(premise, rule):
    # check for >, < inside of string of atomic rule
    if " < " in premise:
        aux = premise.split(" < ")
        variable = aux[0]
        value = int(aux[1])
        for partial_conclusion in partial_conclusions:
            if variable + " = " in partial_conclusion:
                if int(partial_conclusion.split(" = ")[1]) < value:
                    return True
                else:
                    # found, but doesn't meet the requirement, then I have to add to false conclusions
                    false_conclusions.append(rule[THEN])
                    return False
        return False

    if " > " in premise:
        aux = premise.split(" > ")
        variable = aux[0]
        value = int(aux[1])
        for partial_conclusion in partial_conclusions:
            if variable + " = " in partial_conclusion:
                if int(partial_conclusion.split(" = ")[1]) > value:
                    return True
                else:
                    false_conclusions.append(rule[THEN])
                    return False
        return False

    if premise in partial_conclusions:
        return True
    else:
        return False


# documentatie de max 3 pagini: ce tehn am folosit, o pagina de user guide si o pagina de descriere a proiectuluil (a codului)
def check_if_conclusion_is_false(conclusion):
    if conclusion in false_conclusions:
        return True
    return False


def ask_question():
    # TODO: false_conclusions: invalidate false conclusions(for < or >)
    for rule in rules:
        if check_if_conclusion_is_false(rule[THEN]):   # we verify if there isn't something that we dont' have to ask
            continue
        if rule[IF] in asked:
            continue

        if len(rule[IF]) == 1 and "set" in rule[IF][0]:
            print(rule[IF][0].replace("set ", "") + "? (int value)")
            answer = input()
            partial_conclusions.append(rule[THEN].replace("set ", "") + " = " + answer)
            asked.append(rule[IF])
            return True

        if not (rule[IF] in asked) and not (rule[THEN] in partial_conclusions) and not false_premise_present(rule[IF]):
            s = []
            for subrule in rule[IF]:
                if not (subrule in asked) and not (subrule in partial_conclusions) and not (subrule in false_conclusions):
                    s.append(subrule)

            if s:
                print(' AND '.join(s) + "?")
                answer = input()
                if answer == "True":
                    partial_conclusions.append(rule[THEN])
                    # subrules = s.split(" AND ")
                    # for subrule in subrules:
                        # for rule in rules:

                        # if subrule in [rule[IF] for rule in rules]:
                    asked.append(rule[IF])
                    return True
                elif answer == "False":
                    false_conclusions.append(rule[THEN])
                    asked.append(rule[IF])
                    return True

    print("NO MORE QUESTIONS LEFT")
    return False


if __name__ == '__main__':

    with open('knowledge_base.json') as file:
        rules = json.load(file)

    # loop until we get to a conclusion
    while True:
        print("partial_conclusions:", partial_conclusions)
        print("false_conclusions:", false_conclusions)
        no_change = True
        for rule in rules:
            if already_got_fired(rule):
                continue
            # extract the premises
            premises = rule[IF]
            rule_can_be_fired = evaluate_premises(premises, rule)
            if rule_can_be_fired:
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
            print("final conclusions: ", final_conclusions)
            rules2 = rules.copy()
            for final_conclusion in final_conclusions:
                for rule in rules:
                    if rule[THEN] == final_conclusion:
                        rules2.remove(rule)
            rules = rules2
            final_conclusions = []
            print("Would you like to continue?")
            answer = input()
            if answer == "False":
                break
        if no_change:
            if not ask_question():
                break

    print("Exited.")
    # not yet sure how I'm going to have more final conclusions, but we'll see
