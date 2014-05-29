
from AddTaskResourcesDialog import AddTaskResourcesDialog

class AddResourcesDialogCustomizer:
    ############################
    def __init__( self, gui, logic ):

        assert isinstance( gui, AddTaskResourcesDialog )

        self.gui        = gui
        self.logic      = logic

        self.resources  = []

        self.__setupConnections()

    #############################
    def __setupConnections( self ):
        self.gui.ui.okButton.clicked.connect( self.__okButtonClicked )

    #############################
    def __okButtonClicked( self ):
        self.resources = self.gui.ui.folderTreeView.model().exportChecked()
        self.gui.window.close()