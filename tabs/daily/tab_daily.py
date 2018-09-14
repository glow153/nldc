import numpy as np
from PyQt5.QtCore import (Qt, pyqtSlot)
from PyQt5.QtWidgets import (QHBoxLayout, QPushButton, QVBoxLayout, QWidget)
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from pysparkmgr import PySparkManager
from tabs.daily.filter import JFilter
from tabs.daily.gbox import (GbxDatelist, GbxVisual, GbxAxis, GbxFilter)


class TabDaily(QWidget):
    def __init__(self):
        QWidget.__init__(self, flags=Qt.Widget)

        # init components

        self.fig = plt.Figure()
        self.canvas = FigureCanvas(self.fig)

        self.datelist = GbxDatelist('날짜 선택')
        self.gbxAxis = GbxAxis('y축 설정')
        self.gbxVisual = GbxVisual('선 종류')
        self.gbxFilter = GbxFilter('필터링 적용')
        self.btn_drawPlot = QPushButton("차트그리기")

        # Left Layout
        self.leftLayout = self.mainLayout_left()
        # Right Layout
        self.rightLayout = self.mainLayout_right()

        # Main Layout
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)
        self.mainLayout.setStretchFactor(self.leftLayout, 1)
        self.mainLayout.setStretchFactor(self.rightLayout, 0)

        self.setLayout(self.mainLayout)

        # set events
        self.btn_drawPlot.clicked.connect(self.drawLinePlot)

        # get PySparkManager
        self.pysparkmgr = PySparkManager()

    def mainLayout_left(self):
        layout_l = QVBoxLayout()
        layout_l.addWidget(self.canvas)
        return layout_l

    def mainLayout_right(self):
        layout_r = QVBoxLayout()
        layout_r.addWidget(self.datelist)
        layout_r.addWidget(self.gbxAxis)
        layout_r.addWidget(self.gbxVisual)
        layout_r.addWidget(self.gbxFilter)
        layout_r.addWidget(self.btn_drawPlot)
        layout_r.addStretch(1)
        return layout_r

    @pyqtSlot(name='drawPlot')
    def drawLinePlot(self):
        # reset plot
        plt.close()
        self.fig.clear()

        daylist = self.datelist.getItemChecked()
        selectedColumn = self.gbxAxis.getSelectedItem()
        plotTitle = ''

        for day in daylist:  # multiple select by checked days
            df = self.pysparkmgr.getDF('nt_srs')

            # select every single day
            sel = df.filter('date == "%s"' % day)

            timelist = sel.select('time') \
                .toPandas() \
                .values

            left = sel.select(selectedColumn[0]) \
                .toPandas() \
                .values

            hmlist = [x[0] for x in timelist]
            xtick_list = []
            xticklabel_list = []
            for i in range(0, len(hmlist)):
                if hmlist[i].split(':')[1] == '00':
                    xtick_list.append(i)
                    xticklabel_list.append(hmlist[i].split(':')[0])

            ax_left = self.fig.add_subplot(111)
            ax_left.plot(np.arange(len(timelist)), left,
                         color='blue', label=day + ' ' + selectedColumn[0])
            ax_left.set_xticks(xtick_list)
            ax_left.set_xticklabels(xticklabel_list)

            ax_left.set_ylim(0, GbxAxis.default_ylim(selectedColumn[0]))

            ax_left.set_xlabel('time')
            ax_left.set_ylabel(selectedColumn[0])

            if self.gbxFilter.isChecked():
                filter = JFilter()
                right_filtered = filter.process(left)
                ax_left.plot(np.arange(len(timelist)), right_filtered,
                             color='green', label=day + ' ' + selectedColumn[0] + '_filtered')

            if len(selectedColumn) == 2:
                right = sel.select(selectedColumn[1]) \
                    .toPandas() \
                    .values
                ax_right = ax_left.twinx()

                ax_right.plot(np.arange(len(timelist)), right,
                              color='red', label=day + ' ' + selectedColumn[1])
                ax_right.set_ylim(0, GbxAxis.default_ylim(selectedColumn[1]))
                ax_right.set_ylabel(selectedColumn[1])

                if self.gbxFilter.isChecked():
                    filter = JFilter()
                    right_filtered = filter.process(right)
                    ax_right.plot(np.arange(len(timelist)), right_filtered,
                                  color='orange', label=day + ' ' + selectedColumn[1] + '_filtered')

            self.fig.legend(loc='upper right', fontsize=10)
            self.canvas.draw()

    # def makeTimeline(self, timelist):
    #     hmlist = [x[0] for x in timelist]
    #     xtick_list = []
    #     xticklabel_list = []
    #     for i in range(0, len(hmlist)):
    #         if hmlist[i].split(':')[1] == '00':
    #             xtick_list.append(i)
    #             xticklabel_list.append(hmlist[i].split(':')[0])
