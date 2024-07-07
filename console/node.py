import logging, re
from .utilities import varg

class MenuNode:
    '''
    Node controller for Menu system. Interacts with MenuPointer and MenuShell.

    Methods:
         __init__: Initialize node with preliminary attributes.
         __repr__: Minimal representation string showing ID and Selection Mode.
            _pack: Tuple packaging of Node attributes; for exporting.
        add_child: Add child node to the current MenuNode.

    Attributes:
         children: (list) Contains all children nodes.
           parent: (MenuNode) Traceback attribute of parent; made upon creation
                   of 'add_child'
               id: (str) Primary identifier of the node; optionally (though
                   recommended) unique per Menu object.
             mode: (str) Executable command selection styles; used by
                   MenuPointer.
        selection: (list) Selection options given mode parameters; referenced
                   by MenuPointer.
    '''
    # v: 2025-07-06

    def __init__(
            self,
            id:str,
            truefalse:bool = False,
            choice:list = None,
            pattern = None,
            bounds:range = None,
            run = None,
            **kwargs
    ):
        '''
        Initializing method for MenuNode objects.

        Arguments:
                   id: (str) Primary identification field used to ID Node
                       within Menu object
            truefalse: (bool) Selection Mode for boolean commands.
               choice: (list) Selection Mode for multiple choice or list-based
                       options. All list elements must be string or
                       string-castable.
              pattern: (list) Selection Mode for regular expression patterns.
                       Inputs acceptable are single pattern-able string or
                       list. All list elements must be string-like objects

        Return:
        '''
        # v: 2025-07-06

        # validate basic arguments
        varg(id, str, varname= 'id')
        varg(truefalse, bool, varname= 'truefalse')
        varg(choice, list, varname= 'choice')
        varg(pattern, list, re.Pattern, varname= 'pattern')

        # validate advanced arguments
        if choice != None:
            [varg(x, bool, float, int, str, varname= 'choice') for x in choice]
        if isinstance(pattern, list):
            [varg(x, re.Pattern, varname= 'pattern') for x in pattern]
        
        # validate options
        opt = len(list(filter(
                lambda x: x is not None and x is not False,
                (truefalse, choice, pattern, bounds)
            )))
        if opt > 1:
            raise ValueError(f"Only single input mode option allowed. Arguments show {opt} modes selected.")
        
        # initialize primary attributes
        self.id = id
        self.children = []
        self.mode = None
        self.selection = None
        self.run = run

        # set node options
        ## choices are finite lists of options, all options are converted to strings
        for key, value in kwargs.items():
            if key in ['mode', 'selection']:
                setattr(self, key, value)

        ## passthrough imports (from pickle importer in MenuShell class)
        if self.selection and self.mode:
            logging.debug(f"MenuNode {self.id} created via passthru insertion.")

        elif choice != None:
            self.selection = choice
            self.mode = 'choice'

        ## patters are regular expressions
        elif pattern != None:
            if isinstance(pattern, str):
                self.selection = [pattern]
            else:
                self.selection = pattern
            self.mode = 'pattern'

        ## otherwise use ID as the available node selection (i.e. choice of 1)
        else:
            self.selection = [id]
            self.mode = 'id'
        logging.debug(f"MenuNode {self.id} created using {self.mode} Selection Mode.")

    def __repr__(self):
        '''
        Minimal representative value of MenuNode showing ID, Selection Mode
        and Selection Size.

        Arguments:
            None

        Return:
            (str): Representative string.
        '''
        # v: 2025-07-06

        return f"MenuNode= {self.id}. Mode= {self.mode}. Size= {len(self.selection)}."
    
    def _pack(self):
        '''
        Tuple packing used for node decomposition.

        Arguments:
            none

        Return:
            (tuple): Packed MenuNode.
        '''
        # v: 2025-07-06

        return (self.id, self.parent, self.mode, self.selection)
    
    def add_child(self, child):
        '''
        Adds a child node to the current MenuNode.

        Arguments:
            child: (MenuNode) MenuNode child object. 

        Return:
            None
        '''
        # v: 2025-07-06

        # validate arguments
        if not isinstance(child, MenuNode):
            raise TypeError(f"Invalid child argument. Expected MenuNode, got {type(child)}.")
        
        # set parent id for traceback
        child.parent = self.id
        
        self.children.append(child)
        logging.debug(f"MenuNode Child {child.id} created under Parent {self.id}.")

def _rec_decompose_node(node:MenuNode):
    '''
    Recursive decomposition of nested nodes.

    Arguments:
        node: (MenuNode) File path and name of exporting file.

    Yield:
        Individual MenuNode packages
    '''
    # v: 2025-07-06

    if node.children:
        for child in node.children:
            yield child._pack()
            if child.children:
                yield from _rec_decompose_node(child)
    else:
        yield node