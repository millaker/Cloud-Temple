from fsm import TocMachine

states = ["Main", "Door", "Meditation", "Start", "DiceOne", "DiceTwo",
          "DiceThree", "Result", "Meaning", "Explanation", "Fail"]
transitions = [
    {
        "trigger" : "advance",
        "source" : "Main",
        "dest" : "Door",
        "conditions" : "is_going_to_Door"
    },
    {
        "trigger" : "advance",
        "source" : "Door",
        "dest" : "Meditation",
        "conditions" : "is_going_to_Meditation"
    },
    {
        "trigger" : "advance",
        "source" : "Meditation",
        "dest" : "Start",
        "conditions" : "is_going_to_Start"
    },
    {
        "trigger" : "advance",
        "source" : "Start",
        "dest" : "DiceOne",
        "conditions" : "is_going_to_Dice"
    },
    {
        "trigger" : "advance",
        "source" : "DiceOne",
        "dest" : "DiceTwo",
        "conditions" : "is_going_to_Dice"
    },
    {
        "trigger" : "advance",
        "source" : "DiceTwo",
        "dest" : "DiceThree",
        "conditions" : "is_going_to_Dice"
    },
    {
        "trigger" : "advance",
        "source" : "DiceThree",
        "dest" : "Result",
        "conditions" : "is_going_to_Result"
    },
    {
        "trigger" : "advance",
        "source" : "Result",
        "dest" : "Meaning",
        "conditions" : "is_going_to_Meaning"
    },
    {
        "trigger" : "advance",
        "source" : "Meaning",
        "dest" : "Explanation",
        "conditions" : "is_going_to_Explanation"
    },
    {
        "trigger" : "advance",
        "source" : "Explanation",
        "dest" : "Main",
        "conditions" : "is_going_to_Main"
    },
    {
        "trigger" : "advance",
        "source" : "Fail",
        "dest" : "Start",
        "conditions" : "is_going_to_Start"
    },
    {
        "trigger" : "go_Main",
        "source" : ["Main",
                    "Door",
                    "Meditation",
                    "Start",
                    "DiceOne",
                    "DiceTwo",
                    "DiceThree",
                    "Result",
                    "Meaning",
                    "Explanation",
                    "Fail"],
        "dest" : "Main",
        "conditions" : "is_going_to_Main"
    },
    {
        "trigger" : "go_Fail",
        "source" : ["DiceOne",
                    "DiceTwo",
                    "Start"],
        "dest" : "Fail",
    },
]

def create_machine():
    machine = TocMachine(states = states, transitions = transitions, initial = "Main",
                         auto_transitions = False,
                         show_conditions = True)
    return machine