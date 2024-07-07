import logging
from pickle import dump, load
from .node import MenuNode, _rec_decompose_node
from .utilities import varg
from ..exceptions import IntegrityError, CompositeError

class MenuShell:
    '''
    Shell container for Menu system. Contains all MenuNode objects for
    interaction with MenuPointer.

    Methods:
         __init__: Initialize shell with empty attributes.

    Attributes:
        root: (MenuNode) Menu system root node. Only 1 root node allowed at a
              time.
    '''
    # v: 2024-07-07

    def __init__(self):
        '''
        Initialize empty MenuShell object.

        Arguments:
            root: The primary and top-level node of the MenuShell. Initializes
                  empty; use add_node method with parent = None to establish
                  Root Node.

        Return:
            None
        '''
        # v: 2024-07-07
        
        # initialize empty menu shell at root
        self.root = None

    def add_node(self, id:str, parent:MenuNode = None, **kwargs):
        '''
        Add new node to the MenuShell as child to 'parent' node. Initial node
        must have no parent (creates root node).

        Arguments:
                  id: (str) Primary identifier of the node. Used as selection
                      when no Selection Mode identified via kwargs.
              parent: (MenuNode) Parent Node to subject, as applicable.
            **kwargs: Keyword arguments passed to the MenuNode class.

        Return:
            MenuNode object for newly created node. Node is also subsetted to
            Parent Node, if applicable.
        '''
        # v: 2024-07-07

        # validate arguments
        varg(id, str, varname= 'id')
        varg(parent, MenuNode, varname= 'parent')

        node = MenuNode(id, **kwargs)
        if id == 'root':
            if self.root is None:
                self.root = node
                self.root.parent = None
                logging.debug(f"New root node {node.id} created in MenuShell.")
            else:
                raise ValueError(f"Root Node for MenuShell already exists.")
        else:
            parent.add_child(node)
            logging.debug(f"New node {node.id} created under {parent.id} parent node.")

        return node

    def menu_tree(self):
        '''
        Displays the full menu tree in nested list form.

        Arguments:
            None

        Return:
            None
        '''
        # v: 2024-07-07

        if self.root is None:
            logging.info(f"No menu tree available; root node does not exist")
            return None

        def _recursive_tree(node):
            if not node.children:
                return node.id
            else:
                return [node.id, [_recursive_tree(child) for child in node.children]]
        return _recursive_tree(self.root)
    
    def to_pkl(self, filepath:str = None):
        '''
        Export menu decomposition as pickle file.

        Arguments:
            filepath(str): File path and name of exporting file.

        Return:
            None
        '''
        # v: 2024-07-07 UNSTABLE

        # validate arguments
        varg(filepath, str, varname= 'filepath')
        if isinstance(filepath, str):
            ext = filepath.rsplit('.', 1)[-1]
            if ext not in ['pkl', 'pickle']:
                raise ValueError(f"Invalid filetype given. Expected pickle-equivalent, got {ext}.")

        # set default values
        if not filepath:
            filepath = str().join([self.root.id, '.pkl'])

        # decompose menu nodes
        mx = tuple(decompose_menu(self))

        # export
        with open(filepath, 'wb') as f:
            dump(mx, f)
        logging.debug(f"Pickle file created at {filepath}.")

def decompose_menu(menu:MenuShell):
    '''
    Decomposition of nested node with recursion.

    Arguments:
        menu: {MenuShell) File path and name of exporting file.

    Yield:
        Individual MenuNode packages
    '''
    # v: 2024-07-07

    # validate arguments
    varg(menu, MenuShell, varname= 'menu')

    if menu.root:
        yield menu.root._pack()
        yield from _rec_decompose_node(menu.root)

    else:
        logging.WARNING(f"MenuShell is empty and does not contain a root node.")
        return
    
def from_pkl(filepath:str):
    '''
    Creates menu from pickle decomposed elements.

    Arguments:
        filepath(str): File path and name of importing file.

    Yield:
        Individual MenuNode packages
    '''
    # v: 2024-07-07 UNSTABLE

    # validate arguments
    varg(filepath, str, varname= 'filepath')
    if isinstance(filepath, str):
        ext = filepath.rsplit('.', 1)[-1]
        if ext not in ['pkl', 'pickle']:
            raise ValueError(f"Invalid filetype given. Expected pickle-equivalent, got {ext}.")
            
    with open(filepath, 'rb') as f:
        mi = load(f)
    logging.debug(f"Pickle file imported from {filepath}.")

    return from_tuple(mi, False)

    

def from_tuple(obj:tuple, validate:bool = True):
    '''
    Import and build MenuShell with nodes from existing tuple object.

    Arguments:
            obj(tuple): Sequential tuple object of menu nodes instanced from root
                        node to all sequential and nested children nodes.
        validate(bool): Validate sequence and integrity of sequential interior
                        tuple elements.

    Return:
        MenuShell object with compiled and nested nodes.

    Version:
        v1; 2024-05-14
    '''

    # validate arguments
    if not isinstance(obj, tuple):
            raise TypeError(f"Invalid obj argument. Expected tuple, got {type(obj)}.")
    if not isinstance(validate, bool):
            raise TypeError(f"Invalid validate argument. Expected bool, got {type(validate)}.")
    
    if validate:
        val_list = []
        for n, (id, parent, mode, selection) in enumerate(obj):
            # nesting and sequence
            if n == 0 and parent:
                raise IntegrityError(f"First nodal element is not a root node. Parent value is {parent}.")
            elif n > 0 and id not in val_list:
                raise IntegrityError(f"Parent node is not initialized prior to current node. Nodal IDs are: Current= {id}, Parent= {parent}.")
            
            # element values
            if not isinstance(id, str):
                raise TypeError()
            if mode not in ['id', 'choice', 'pattern']:
                raise CompositeError()
            if not isinstance(selection, list):
                raise TypeError()
            
            # populate end of IF loop iteration
            val_list.append(id)
    
    m = MenuShell()
    for n, (id, parent, mode, selection) in enumerate(obj):     
        if n == 0:
            locals()[id] = m.add_node(id)
        else:
            locals()[id] = m.add_node(id, locals()[parent], mode = mode, selection = selection)
    return m