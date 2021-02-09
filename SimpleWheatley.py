from subprocess import Popen
import PySimpleGUI as sg

class Wheatley():
    def __init__(self, tower_id, method, no_pause, pace):
        args = ['wheatley', tower_id]
        args += ['--method', method]
        args += ['-u'] # Up, down then in, start changes after two full rounds
        args += ['-s'] # Stop at rounds
        args += ['-S', str(int(pace * 5040 / 60))] # Peal speed pace of rounds in seconds times length of a peal in minutes  
        if no_pause:
            args += ['-k'] # Keep going, don't wait for assigned ringers to ring
        self.proc = Popen(args)

    def stop(self):
        self.proc.terminate()

def pace_to_speed(pace):
    return str(int(pace * 5040 / 3600)) + 'h ' + str(int(pace *5040 / 60) % 60) + 'm'

if __name__ == '__main__':
    wheatley = None

    pace = 3.0
    
    methods = ['Plain Bob Doubles', 'Grandsire Doubles', 'Plain Bob Minor', 'Plain Bob Triples']
    
    layout = [ [sg.Text('Tower ID'), sg.Input(key = '-TOWER_ID-', size = (15, 1), enable_events = True)],
               [sg.Text('Select method'), sg.Combo(methods, key = '-METHOD-', enable_events = True, readonly = True)],
               [sg.Checkbox('No waiting', key = '-NO_PAUSE-', default = False)],
               [sg.Text('Pace of rounds'),
                sg.Slider(key = '-PACE-', range = (2.0, 5.0), default_value = pace, resolution = 0.1, orientation = 'h', enable_events = True)],
               [sg.Text(f'Peal speed {pace_to_speed(pace)}', key = '-PEAL_SPEED-')],
               [sg.Button('Start Wheatley', key = '-START-', disabled = True),
                sg.Button('Stop Wheatley', key = '-STOP-', disabled = True)] ]

    window = sg.Window('Simple Wheatley', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            if wheatley:
                wheatley.stop()
                wheatley = None
            break
        if event == '-METHOD-':
            if wheatley:
                wheatley.stop()
            if len(values['-TOWER_ID-']) >= 9:
                window['-START-'].update(disabled = False)
        if event == '-TOWER_ID-':
            # Paste can dump a whole load of characters in one go so walk the text until
            # a non-number is found then ditch that and the rest of the string
            id = values['-TOWER_ID-']
            for ndx in range(len(id)):
                if id[ndx] not in '0123456789':
                    id = id[:ndx]
                    window['-TOWER_ID-'].update(id)
                    break
            if len(values['-TOWER_ID-']) >= 9 and values['-METHOD-'] != '':
                window['-START-'].update(disabled = False)
        if event == '-PACE-':
            window['-PEAL_SPEED-'].update(f'Peal speed {pace_to_speed(values["-PACE-"])}')
        if event == '-START-':
            window['-START-'].update(disabled = True)
            window['-STOP-'].update(disabled = False)
            wheatley = Wheatley(values['-TOWER_ID-'], values['-METHOD-'], values['-NO_PAUSE-'], values['-PACE-'])
        if event == '-STOP-':
            if wheatley:
                wheatley.stop()
                wheatley = None
            window['-STOP-'].update(disabled = True)
            if len(values['-TOWER_ID-']) >= 9 and values['-METHOD-'] != '':
                window['-START-'].update(disabled = False)

    window.close()
