from dataclasses import dataclass
from typing import Dict
from enum import Enum

class IntentState(Enum):
    READY_FOR_FULFILLMENT = 'ReadyForFulfillment'
    FULFILLED = 'Fulfilled'

class IntentName(Enum):
    START_SERVER = 'StartServer'

@dataclass
class Intent:
    name: IntentName
    state: IntentState

def parse_intent(event):
    raw_intent = event['sessionState']['intent']
    return Intent(IntentName(raw_intent['name']), IntentState(raw_intent['state']))