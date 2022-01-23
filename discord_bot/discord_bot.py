from intent import parse_intent, IntentName, IntentState
from copy import deepcopy
    
def close(intent_request, final_intent_state: IntentState):
    session_state = deepcopy(intent_request['sessionState'])
    session_state['intent']['state'] = final_intent_state.value
    return {
        'sessionState': {
            'activeContexts': session_state.get('activeContexts', []),
            'sessionAttributes': session_state.get('sessionAttributes', {}),
            'dialogAction': {'type': 'Close'},
            'intent': session_state['intent']
        }
    }


def lambda_handler(event, context):
    print(event)

    intent = parse_intent(event)

    if intent.name is IntentName.START_SERVER and intent.state is IntentState.READY_FOR_FULFILLMENT:
        return close(event, IntentState.FULFILLED)

    raise Exception('Unhandled intent ' + intent.name.value + ' with state ' + intent.state)
