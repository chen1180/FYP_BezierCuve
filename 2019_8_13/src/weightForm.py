from PyQt5 import QtCore, QtGui, QtWidgets
import sys
class NURBS_WeightForm(QtWidgets.QWidget):
    def __init__(self,nControlPoints,weights,parent=None):
        super(NURBS_WeightForm, self).__init__(parent)
        self.row=nControlPoints
        self.weights = weights
        self.doubleSpinbox=[]
        self.setupUI()
    def setupUI(self):
        self.setWindowTitle("Weights")
        self.layout=QtWidgets.QFormLayout()
        for i in range(self.row):
            label=QtWidgets.QLabel("weight {}".format(i))
            spinBox=QtWidgets.QDoubleSpinBox()
            spinBox.setValue(self.weights[i])
            spinBox.setMinimum(0.0)
            spinBox.setMaximum(1.0)
            spinBox.setSingleStep(0.1)
            self.doubleSpinbox.append(spinBox)
            self.layout.addRow(QtWidgets.QLabel("weight {}".format(i)),spinBox)
        self.okDialog=QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.layout.addRow(self.okDialog)
        self.setLayout(self.layout)
        self.okDialog.accepted.connect(self.accept)
        self.okDialog.rejected.connect(self.reject)
        self.show()
    def accept(self):
        for i in range(len(self.weights)):
            self.weights[i]=self.doubleSpinbox[i].value()
        print(self.weights)
        self.close()
    def reject(self):
        self.close()

if __name__ == '__main__':
    app = QtWidgets.QApplication(['Yo'])
    window = NURBS_WeightForm(5)
    window.show()
    sys.exit(app.exec_())