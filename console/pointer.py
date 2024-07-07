import logging, re
from .shell import MenuShell
from .utilities import clear_console, varg

class MenuPointer:
    '''
    Pointer controller and navigator for Menu system.

    Methods:
         __init__: Initialize pointer attached to a single MenuShell.
           select: Move to next child node by selection.
             back: Go backward in chain of selections.
             roll: List available selections from current node.

    Attributes:
            node: (MenuShell) Menu system shell. Menu must be compiled before
                  pointer can function.
         traceid: (list) Selection history list of nodes by ID. Used for 'back'
                  method.
        tracecmd: (list) Selection history list of nodes by sequenced input
                  commands. Used to help execute path items.
    '''
    # v: 2024-07-07

    def __init__(self, shell:MenuShell):
        '''
        Initialize MenuPointer object to a MenuShell.

        Arguments:
            shell: (MenuShell) Initial root node.

        Return:
            None
        '''
        # v: 2024-07-07
        
        self.node = shell.root
        self.shell = shell
        self.traceid = list()       # sequencing ID of menu selection
        self.tracecmd = list()      # sequencing command of menu selection

    def back(self):
        '''
        Select prior node in menu sequence.

        Arguments:
            None

        Return:
            None
        '''
        # v: 2024-07-07

        if len(self.traceid) > 0:
            self.node = self.traceid.pop()
            prior = self.tracecmd.pop()
            logging.debug(f"Returned pointer to {self.node.id}.")
        else:
            logging.info(f"Can't go back, already at pointer origin.")

    def roll(self, echo = False):
        '''
        List available inputs from current node to children nodes.

        Arguments:
            None

        Return:
            Dictionary of selection modes and available inputs.
        '''
        # v: 2024-07-07

        dlist = dict()
        for child in self.node.children:
            if child.mode not in dlist.keys():
                dlist[child.mode] = list()
            
            match child.mode:
                case 'id':
                    dlist[child.mode].append(child.selection[0])

                case 'choice':
                    dlist[child.mode] = dlist[child.mode] + child.selection
                case _:
                    print('UNHANDLED CASE IN LIST METHOD TO FIX LIST NESTING')
                    raise NotImplementedError()
                    dlist[child.mode].append(child.selection)

        if echo:
            for key, value in dlist.items():
                print(key, value)
        return dlist

    def reset(self):
        '''
        Reset MenuPointer to Menu root.

        Arguments:
            None

        Returns:
            None
        '''
        # v: 2024-07-07

        self.__init__(self.shell)

    def run(self, prefix:str = '> ', prefix_chain:bool = False):
        '''
        Initializes menu in looping console interface.

        Arguments:
                  prefix: (str) Command line interface prefix characters.
            prefix_chain: (bool) Append command history as string chain to
                          command line.

        Returns:
            None
        '''
        # v: 2024-07-07

        # validate arguments
        varg(prefix, str, varname= 'prefix')
        varg(prefix_chain, bool, varname= 'prefix_chain')

        _prefix = prefix
        while True:
            cmd = input(_prefix)

            match cmd:
                # START structural (built-in) commands
                case 'exit':
                    break

                case 'clear':
                    clear_console()
                    _prefix = prefix

                case 'back':
                    if prefix_chain:
                        _prefix = _prefix.rsplit(self.node.id, 1)[0]
                    self.back()

                case 'list':
                    self.roll(True)
            
                case 'reset':
                    self.reset()
                    _prefix = prefix
                # END structural (built-in) commands

                # Invalid/Unknown commands
                case cmd if self.select(cmd) == None:
                    logging.info(f"Invalid command")

                # Known menu commands
                case _:
                    if prefix_chain:
                        _prefix = _prefix + self.node.id + ' '
            
    def select(self, input:str):
        '''
        Select next child node in menu sequence.

        Arguments:
            input: (str) Element used to select child node.

        Return:
            None
        '''
        # v: 2024-07-07

        # validate arguments
        varg(input, str, varname= 'input')

        for child in self.node.children:
            logging.debug(f"Running input against {child.id} child node.")
            match child.mode:
                case 'id' | 'choice':
                    for selector in child.selection:
                        if input == selector:
                            self.traceid.append(self.node)
                            self.tracecmd.append(str(input))
                            self.node = child
                            logging.debug(f"Child node {child.id} selected with {input} input.")
                            return '|'.join(self.tracecmd)
                    
                case 'pattern':
                    for selector in child.selection:
                        if re.match(selector, input):
                            self.traceid.append(self.node)
                            self.tracecmd.append(input)
                            self.node = child
                            logging.debug(f"Child node {child.id} selected with {input} input.")
                            return '|'.join(self.tracecmd)
                        
                case _:
                    logging.debug(f"Unhandled selection mode {child.mode}.")
                    raise NotImplementedError()

        logging.info(f"Invalid selection of {input}.")