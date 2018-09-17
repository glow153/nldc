from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QComboBox, QGroupBox, QVBoxLayout, QHBoxLayout,
                             QGridLayout, QLabel, QCheckBox,
                             QListWidget, QListWidgetItem)
from matplotlib import colors as mcolors

from pysparkmgr import PySparkManager


class GbxDatelist(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        self.listwdg = QListWidget()

        # get date list from dataframe using pyspark
        self.datelist = self.getDatelist()
        self.makeList(self.datelist)

        # init layout
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.listwdg)
        self.setLayout(self.layout)

    def getDatelist(self):  # 날짜만 가져옴
        pysparkmgr = PySparkManager()
        datelist = pysparkmgr.getDF('nt_srs') \
            .select('date') \
            .sort('date') \
            .distinct() \
            .toPandas().values.tolist()
        return list(map(lambda date: date[0], datelist))

    def makeList(self, datelist):
        for dt in datelist:
            item = QListWidgetItem()
            item.setText(dt)
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
            self.listwdg.addItem(item)

    def getItemChecked(self):
        ret = []
        for i in range(self.listwdg.count()):
            if self.listwdg.item(i).checkState() == Qt.Checked:
                ret.append(self.listwdg.item(i).text())
        return ret


class GbxVisual(QGroupBox):
    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)

        self.colorlist = self.getNamedColorList()
        self.markerlist = ['.', ',', 'o', 'v', '<', '>', '^',
                           '1', '2', '3', '4', 's', 'p', '*',
                           'h', 'H', '+', 'x', 'D', 'd']
        self.linelist = ['-', '--', '-.', ':']

        self.cbxColor = QComboBox()
        self.cbxMarkerType = QComboBox()
        self.cbxLineType = QComboBox()

        self.layout = QGridLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        # disable for testmode
        self.cbxColor.setEnabled(False)
        self.cbxMarkerType.setEnabled(False)
        self.cbxLineType.setEnabled(False)

    def getNamedColorList(self):
        # matplotlib color list : named_color.py
        # https://matplotlib.org/examples/color/named_colors.html
        colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
        by_hsv = sorted((tuple(mcolors.rgb_to_hsv(mcolors.to_rgba(color)[:3])), name)
                        for name, color in colors.items())
        sorted_names = [name for hsv, name in by_hsv]
        return sorted_names

    def setItemsInCbx(self):
        self.cbxColor.addItems(self.colorlist)
        self.cbxMarkerType.addItems(self.markerlist)
        self.cbxLineType.addItems(self.linelist)

    def setComponentsWithLayout(self):
        self.layout.setColumnStretch(1, 2)
        self.layout.setColumnStretch(2, 2)
        self.layout.setColumnStretch(3, 2)

        self.layout.addWidget(QLabel('색상'), 0, 0)
        self.layout.addWidget(self.cbxColor, 0, 1)
        self.layout.addWidget(QLabel('마커'), 1, 0)
        self.layout.addWidget(self.cbxMarkerType, 1, 1)
        self.layout.addWidget(QLabel('선'), 2, 0)
        self.layout.addWidget(self.cbxLineType, 2, 1)

        self.setLayout(self.layout)


class GbxAxis(QGroupBox):

    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)

        self.leftAxis = ['illum', 'cct', 'swr']
        self.rightAxis = ['illum', 'cct', 'swr']

        self.cbxLeft = QComboBox()
        self.cbxRight = QComboBox()
        self.chkEnableRightAxis = QCheckBox()
        self.layout = QGridLayout()

        self.chkEnableRightAxis.setChecked(False)
        self.cbxRight.setEnabled(False)

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        self.chkEnableRightAxis.stateChanged.connect(self.enableRightAxis)

    def setItemsInCbx(self):
        self.cbxLeft.addItems(self.leftAxis)
        self.cbxRight.addItems(self.rightAxis)

    def setComponentsWithLayout(self):
        self.layout.setColumnStretch(1, 3)
        self.layout.setColumnStretch(2, 3)

        self.layout.addWidget(QLabel('왼쪽 축'), 0, 1)
        self.layout.addWidget(self.cbxLeft, 0, 2)
        self.layout.addWidget(self.chkEnableRightAxis, 1, 0)
        self.layout.addWidget(QLabel('오른쪽 축'), 1, 1)
        self.layout.addWidget(self.cbxRight, 1, 2)
        self.setLayout(self.layout)

    def enableRightAxis(self):
        if self.chkEnableRightAxis.isChecked():
            self.cbxRight.setEnabled(True)
        else:
            self.cbxRight.setEnabled(False)

    def getSelectedItem(self):
        if self.chkEnableRightAxis.isChecked():
            return [str(self.cbxLeft.currentText()), str(self.cbxRight.currentText())]
        else:
            return [str(self.cbxLeft.currentText())]


class GbxFilter(QGroupBox):

    def __init__(self, title):
        QGroupBox.__init__(self, title)
        # self.setFixedSize(120, 150)
        self.setCheckable(True)
        self.setChecked(False)

        self.filterTypeList = ['jake\'s filter']

        self.cbxFilterType = QComboBox()
        self.layout = QHBoxLayout()

        self.setItemsInCbx()
        self.setComponentsWithLayout()

        # self.chkEnableFilter.stateChanged.connect(self.enableFilter)

    def setItemsInCbx(self):
        self.cbxFilterType.addItems(self.filterTypeList)

    def setComponentsWithLayout(self):
        # self.layout.addWidget(self.chkEnableFilter)
        self.layout.addWidget(QLabel('필터링 알고리즘'))
        self.layout.addWidget(self.cbxFilterType)
        self.layout.addStretch(1)
        self.setLayout(self.layout)

    # def enableFilter(self):
    #     if self.chkEnableFilter.isChecked():
    #         self.cbxFilterType.setEnabled(True)
    #     else:
    #         self.cbxFilterType.setEnabled(False)
