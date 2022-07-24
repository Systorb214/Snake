from typing import Callable, List


class MenuElement:

    def __init__(self, string: str, func: Callable | None, *args):
        if string == "":
            raise Exception("Menu element must have a string.")

        #setup
        self.string = string
        self.func = func
        self.args = args
        self.highlighted = False

    def __str__(self):
        return self.string

    def Select(self):
        """selects the menu element if it is highlighted."""
        if self.func != None and self.highlighted == True:
            #call the given function
            self.func(*self.args)

class Menu:
    """The base class for all menus and options."""

    def __init__(self, elements: List[MenuElement]):
        elementCount = len(elements)
        if elementCount < 1:
            raise Exception("Menu must have at least one element.")
            
        self.elements = elements
        
    def Control(self, keyPressed):
        """Controls the menu. This method is called when a key is pressed."""
        #only one element is highlighted at a time
        
        #if no element is highlighted, highlight the first element
        self.elements[0].highlighted = True