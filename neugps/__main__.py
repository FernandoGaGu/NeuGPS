from .interfaz import PromptInterface
from .model import MODELS

MODELS_DICT = {
    'a': MODELS['AD vs HC'],
    'b': MODELS['bvFTD vs HC'],
    'c': MODELS['bvFTD/AD vs HC'],

}

INPUT_OPTIONS = {
    'a': '(a) Alzheimer\' disease VS healthy control decision tree.',
    'b': '(b) Behavioral variant frontotemporal dementia (bvFTD) VS healthy control decision tree.',
    'c': '(c) Behavioral variant frontotemporal dementia (bvFTD) or Alzheimer\' disease VS healthy control '
         'decision tree.'
}

if __name__ == '__main__':
    interface = PromptInterface()

    print('Please select a model:\n')
    for key, value in INPUT_OPTIONS.items():
        PromptInterface.print('    %s' % value, 'white')
    print('\n')

    # User model selection
    valid_input = False
    user_input = interface.getInput('Selection: ').lower()
    while not valid_input:
        if user_input not in MODELS_DICT:
            interface.error()
            user_input = interface.getInput('\nSelection: ').lower()
        else:
            valid_input = True

    print()
    for key, value in INPUT_OPTIONS.items():
        PromptInterface.print('    %s' % value, 'green' if key == user_input else 'red')
    print('\nBelow you will be asked to enter the scores obtained for various neurocognitive tests.\n')

    # Run the algorithm
    model = MODELS_DICT[user_input]
    input_memory = {}  # Cache all user inputs (To avoid having to enter twice the same cognitive test)
    while True:
        if str(model.current_level) in input_memory:
            user_input = input_memory[str(model.current_level)]
        else:
            user_input = interface.update(model.current_level)
            input_memory[str(model.current_level)] = user_input
            PromptInterface.print(f'{model.current_level} = {user_input:.3f}', 'green')

        model = model.updateLevel(user_input)
        if model.current_level is None:
            break

    # Display the result
    interface.end(model.getCurrentProbabilities())

