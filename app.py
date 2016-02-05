from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
import pyblish.api


class Window(QTreeWidget):

    def __init__(self, plugins):
        QTreeWidget.__init__(self)

        self.setHeaderHidden(True)
        self.itemExpanded.connect(self.handleExpanded)
        self.itemClicked.connect(self.handleClicked)

        self.context = pyblish.api.Context()

        for plugin in plugins:
            p = plugin()
            item = QTreeWidgetItem(self)
            item.setText(0, p.__class__.__name__)
            item.plugin = p
            instance = pyblish.api.Instance(p.__class__.__name__, self.context)
            item.instance = instance
            self.addItems(item)

    def addItems(self, parent):
        parent.plugin.process(parent.instance)

        for instance in parent.instance:
            item = QTreeWidgetItem(parent)
            item.setText(0, str(instance))
            item.plugin = parent.plugin
            item.instance = instance
            item.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)

        if not parent.instance:
            parent.setChildIndicatorPolicy(QTreeWidgetItem.DontShowIndicator)

    def handleExpanded(self, item):
        if item is not None and not item.childCount():
            self.addItems(item)

    def handleClicked(self, item, column):
        print item.instance

if __name__ == '__main__':

    import sys
    import mocking
    app = QApplication(sys.argv)
    window = Window(mocking.plugins)
    window.show()
    sys.exit(app.exec_())
