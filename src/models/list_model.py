from PySide6.QtCore import (
    QAbstractListModel, 
    QModelIndex, 
    QObject,
    Qt

)

class ListModel( QAbstractListModel ):
    """
    Custom List Model for holding a list of tasks.

    Each task is a Python dictionary shaped like:
        {
            "name": "Task name",
            "done": True / False
        }

    The model exposes two roles:
      • DisplayRole → Task name (string)
      • CheckStateRole → Checkbox state (Checked / Unchecked)
    """
    __mList = []

    def __init__(self, aParent: QObject = None ):
        """
        Initialize the list model.
        """
        super().__init__( aParent )
        self.__mList = []



    def rowCount( self, aParent: QModelIndex = QModelIndex()):
        """
        Return number of items in the list.
        For list models, parent is always invalid, so we ignore it.
        """
        return len(self.__mList)
    
    def data( self, aIndex: QModelIndex, aRole: int ):
        """
        Return data for a given row and role.

        Qt.DisplayRole      → Return task name (string)
        Qt.CheckStateRole   → Return checkbox (Qt.Checked / Qt.Unchecked)
        """
        if not aIndex.isValid(): return None

        item = self.__mList[aIndex.row()]
        if Qt.ItemDataRole.DisplayRole == aRole:
            return item["name"]
        
        if Qt.ItemDataRole.CheckStateRole == aRole:
            return Qt.CheckState.Checked \
                if item["done"] else Qt.CheckState.Unchecked
    
    def setData( self, aIndex: QModelIndex, aValue: dict, aRole: int ):
        """
        Update model data when the user edits an item.
        Must emit dataChanged() for views (QListView/QTableView) to update.
        
        For Qt.CheckStateRole → value is an integer: 0 = Unchecked, 2 = Checked
        For Qt.DisplayRole    → value is a string for renaming
        """
        if not aIndex.isValid(): return False

        item = self.__mList[aIndex.row()]
        
        if Qt.ItemDataRole.DisplayRole == aRole:
            item["name"] = aValue["name"]
            self.dataChanged.emit( aIndex, aIndex, [aRole] )
            return True
        
        if Qt.ItemDataRole.CheckStateRole == aRole:
            item["done"] = aValue == Qt.CheckState.Checked.value
            self.dataChanged.emit( aIndex, aIndex, [aRole] )
            # self.dataChanged.emit()
            return True
        
        return False
        
    def flags(self, aIndex: QModelIndex):
        """
        Return item capabilities.

        Qt.ItemIsUserCheckable → enables checkbox in QListView
        """
        return (
            Qt.ItemIsEnabled
            | Qt.ItemIsSelectable
            | Qt.ItemIsUserCheckable
        )

    def buildModel( self, aTasks: list[dict] ):
        """
        Reset the entire model with a new list of tasks.
        beginResetModel/endResetModel tells views to fully refresh.
        """
        self.beginResetModel()
        self.__mList = aTasks
        self.endResetModel()

    def addTask( self, aTask: dict ):
        """
        Insert a new task at the end of the list.
        beginInsertRows/endInsertRows notifies views properly.
        """
        self.beginInsertRows( QModelIndex(), len( self.__mList), len(self.__mList))
        self.__mList.append( aTask )
        self.endInsertRows()

    




