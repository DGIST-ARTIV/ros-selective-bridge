import rospy
import os
import sys
import subprocess

from PyQt5.QtWidgets import *
import PyQt5.QtWidgets as QtWidgets
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import *
from PyQt5 import QtGui, QtCore

import rosnode

from PyQt5.QtCore import Qt
sfUI = uic.loadUiType("artiv_bdg.ui")[0]

topicList = [ { "topic" : '/image', "type": "sensor_msgs/msg/Image", "queue_suze": 1 }, { "topic" : '/rosout', "type": "rcl_interfaces/msg/Log", "queue_suze": 1 }]

rospy.set_param("/topics", topicList)

#print(rospy.get_published_topics())



class MyWindow(QMainWindow, sfUI):
    def _int(self, value):
        val = Int16()
        val.data = int(value)
        return val
    def _float(self, value):
        val = Float32()
        val.data = float(value)
        return val

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.setupUi(self)
        # This is for special variable that ros1, ros2 type name is not following conventional type
        self.exceptionList = {"rosgraph_msgs/Log" : "rcl_interfaces/msg/Log"}

        self.objPoly = []
        self.rowCnt = 0

        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget_2.setSelectionMode(QAbstractItemView.SingleSelection)
        header = self.tableWidget.horizontalHeader()
        #header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.tableWidget.setRowCount(2)
        self.tableWidget.cellDoubleClicked.connect(self.addExclude)


        self.commandLinkButton.clicked.connect(self.run)
        self.commandLinkButton_2.clicked.connect(self.kill_bridge)
        self.pushButton.clicked.connect(self.clearExclude)
        self.pushButton_2.clicked.connect(self.savePreset)
        self.pushButton_3.clicked.connect(self.loadPreset)
        formUpdate = QTimer(self)
        formUpdate.start(10500)
        formUpdate.timeout.connect(self.dispUpdate)
        self.dispUpdate()

        formUpdate = QTimer(self)
        formUpdate.start(1000)
        formUpdate.timeout.connect(self.statUpdate)





        self.paramList = []
        self.excludeID = [] # this variable is currently not used anymore,

    def addExclude(self):
        rowPosition = self.tableWidget_2.rowCount()
        self.tableWidget_2.insertRow(rowPosition)
        tarIdx = self.tableWidget.currentRow()
        self.excludeID.append(tarIdx)
        #print(tarIdx)
        #print(self.tableWidget.item(tarIdx, 0).text())
        self.tableWidget_2.setItem(rowPosition, 0, QTableWidgetItem(self.tableWidget.item(tarIdx, 0).text()))
        self.tableWidget_2.setItem(rowPosition, 1, QTableWidgetItem(self.tableWidget.item(tarIdx, 1).text()))

    def clearExclude(self):
        self.tableWidget_2.setRowCount(0);
        self.excludeID = []
        self.paramList = []

    def savePreset(self):
        f = open(os.path.join(os.getcwd(),"bdg_preset.kansan"), 'w')
        for tb2item in range(self.tableWidget_2.rowCount()):
            f.write(self.tableWidget_2.item(tb2item, 0).text()+'\n')
        f.close()
        pass

    def loadPreset(self):
        f = open(os.path.join(os.getcwd(),"bdg_preset.kansan"), 'r')
        while True:
            line = f.readline()
            if not line: break
            rowPosition = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(rowPosition)
            self.tableWidget_2.setItem(rowPosition, 0, QTableWidgetItem(line.strip("\n")))
            self.tableWidget_2.setItem(rowPosition, 1, QTableWidgetItem("From Preset"))
        f.close()

        self.dispUpdate()


    def statUpdate(self):

        # Chk bdg is on
        if "/ros_bridge" in rosnode.get_node_names():
            self.label_5.setText("Bridge Status : ON")
        else:
            self.label_5.setText("Bridge Status : OFF")

        #self.label_6.setText(subprocess.check_output("ps -C parameter_bridge -o %cpu,%mem", shell=True))
        cpustat = "Not ready"
        try:
            cpustat = subprocess.check_output("ps -C parameter_bridge -o %cpu,%mem",shell=True,stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            #print("command '{}' return with error (code {}): {}".format(e.cmd, e.returncode, e.output))
            cpustat = e.output
        self.label_6.setText(cpustat)


    def dispUpdate(self):

        topics = rospy.get_published_topics()
        ros2Cmd = ". /opt/ros/melodic/setup.sh; . /opt/ros/dashing/setup.sh; ros2 topic list -t"
        ros2result = subprocess.check_output(ros2Cmd, shell=True)
        for rs2Topic in ros2result.split('\n')[1:]:
            try:
                topics.append([rs2Topic.split()[0].strip("[]"), rs2Topic.split()[1].strip("[]")])
            except:
                pass
                #print(rs2Topic, "is not parsed")
        #print(rs2Topic)

        self.tableWidget.setRowCount(len(topics))
        for idx, item in enumerate(topics):
            try:
                self.tableWidget.setItem(idx, 0, QTableWidgetItem(str(item[0])))
                self.tableWidget.setItem(idx, 1, QTableWidgetItem(str(item[1])))
                for i in range(self.tableWidget_2.rowCount()):
                    #print(str(item[0]), str(self.tableWidget_2.item(i, 0).text()))
                    if str(item[0]) == str(self.tableWidget_2.item(i, 0).text()):
                        #print("SKIP")
                        self.tableWidget.item(idx, 0).setBackground(QtGui.QColor(100,100,150))
                        self.tableWidget.item(idx, 1).setBackground(QtGui.QColor(100,100,150))
            except:
                pass

    def summarize(self):
        """
        Make final Topic list for publish topics, exclude topic...
        """
        self.paramList = []
        ''' This method has severe flaw
        for i in range(self.tableWidget.rowCount()):
            if i in self.excludeID:
                print(i, "is exclude", self.excludeID)
                continue
        '''
        tb2_topic_list = []
        for tb2item in range(self.tableWidget_2.rowCount()):
            tb2_topic_list.append(self.tableWidget_2.item(tb2item, 0).text())

        for tb1item in range(self.tableWidget.rowCount()):
            if self.tableWidget.item(tb1item, 0).text() in tb2_topic_list:
                #print("Skip", self.tableWidget.item(tb1item, 0).text())
                pass
            else:
                try:
                    if self.paramList[-1].get("topic") == str(self.tableWidget.item(tb1item, 0).text()): continue
                except:
                    pass
                self.paramList.append({'topic' : str(self.tableWidget.item(tb1item, 0).text()),
                                        "type" : self.toRos2type(str(self.tableWidget.item(tb1item, 1).text())),
                                        "queue_size" : 1 })
        #print(self.paramList)
        return self.paramList

    def toRos2type(self, data):
        if self.exceptionList.get(data):
            return  self.exceptionList.get(data)
        else:
            temp = data.split("/")
            if temp[1] == "msg": # for ros2 msg
                return data
            return temp[0] + "/msg/" + temp[1]

    def pubParam(self):
        #topicList = [ { "topic" : '/image', "type": "sensor_msgs/msg/Image", "queue_suze": 1 }, { "topic" : '/rosout', "type": "rcl_interfaces/msg/Log", "queue_size": 1 }]
        #self.paramList.append({ "topic" : '/FakeTopic', "type": "std_msgs/msg/Int16", "queue_suze": 1 })
        #print(self.paramList)
        rospy.set_param("/topics", self.paramList)

    def run(self):
        # Debug print function
        #temp = self.summarize()
        #for i in temp:
        #    print(i)
        self.summarize()
        self.pubParam()
        os.system(". /opt/ros/melodic/setup.sh; . /opt/ros/dashing/setup.sh; ros2 run ros1_bridge parameter_bridge &")

    def kill_bridge(self):
        rosnode.kill_nodes(["/ros_bridge"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()
