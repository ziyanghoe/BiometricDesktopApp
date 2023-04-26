import os
import json
import numpy
from _collections import OrderedDict
class data_manage():

    def __init__(self):
        self.keyarray = ["Patient Name", "Patient Age", "Patient gender", 'Patient IC', "Patient Race", "Date", "Doctor",
                    "DOB",
                    "shoul_abd_r", "shoul_add_r", "shoul_flex_abd", "ahoul_ext_r", "elbow_flx_r", "elbow_ext_r",
                    "wrist_flex_r", "wrist_ext_r", "grip_r", "hip_flex_r", "hip_ext_r"
            , "knee_ext_r", "knee_flex_r", "ankle_dor_r", "ankle_plantar_r"  # 23
            , "shoul_abd_l", "shoul_add_l", "shoul_flex_l", "shoul_ext_l", "elbow_flex_l", "elbow_ext_l",
                    "writst_flex_l", "wrist_ext_l", "grip_l", "hip_flex_l", "hip_ext_l"
            , "knee_ext_l", "knee_flex_l", "ankle_dor_l", "ankle_plantar_l"  # 38
            , "mshoul_abd_right", "mshoul_add_right", "mshoul_flex_right", "mshoul_ext_right"
            , "melbow_flex_r", "melbow_ext_r", "mwrist_flex_r", "mwrist_ext_r", "mgrip_r", "mhip_flex_r", "mhip_ext_r",
                    "mknee_ext_r", "mknee_flex_r", "mankle_dor_r", "mplantar_r"  # 53
            , "mshoul_abd_l", "mshoul_dd_l", "mshoul_flex_l", "mshoul_ext_l", "melbow_flex_l", "melbow_ext_l",
                    "mwrist_flex_l", "mwrist_ext_l", "mgrip_l", "mhip_flex_l", "mhip_ex_l"
            , "mknee_ext_l", "mknee_flex_l", "mankle_dor_l", "mankle_plantar_l"  # 68
            , "hip_abd_r", "hip_add_r", "hip_abd_l", "hip_add_l"  # hip add on 72
            , "mhip_abd_r", "mhip_add_r", "mhip_abd_l", "mhip_add_l"  # hip mas add on 76
            , "tardieu_shoul_abd_rr1", "tardieu_shoul_add_rr1", "tardieu_shoul_flex_rr1", "tardieu_shoul_ext_rr1",
                    "t_elbow_flex__rr1", "t_elbow_ext_rr1"
            , "twrist_flex_rr1", "twrist_ext_rr1", "tgrip_rr1", "thip_abd_rr1", "thip_add_rr1", "thip_flex_rr1",
                    "thip_ext_rr1", "tknee_flex_rr1"
            , "tknee_ext_rr1", "tankle_dor_rr1", "tankle_plantar_rr1"  # 93
            , "tardieu_shoul_abd_rr2", "tardieu_shoul_add_rr2", "tardieu_shoul_flex_rr2", "tardieu_shoul_ext_rr2",
                    "t_elbow_flex__rr2"
            , "t_elbow_ext_rr2", "twrist_flex_rr2", "twrist_ext_rr2", "tgrip_rr2", "thip_abd_rr2", "thip_add_rr2",
                    "thip_flex_rr2",
                    "thip_ext_rr2", "tknee_flex_rr2", "tknee_ext_rr2", "tankle_dor_rr2", "tankle_plantar_rr2"  # 110
            , "t_shoul_abd_rl1", "t_shoul_add_rl1", "t_shoul_flex_rl1", "t_shoul_ext_rl1", "t_elbow_flex_rl1",
                    "t_elbow_ext_rl1",
                    "t_wrist_flex", "t_wrist_ext", "t_grip_rl1", "thip_abd_rl1", "t_hip_add_rl1", "t_hip_flex_rl1",
                    "t_hip_ext_rl1",
                    "t_kenee_flex_rl1", "t_kenee_ext_rl1", "t_ankle_dor_rl1", "t_ankle_plantar_rl1"  # 127
            , "t_shoul_abd_rl2", "t_shoul_add_rl2", "t_shoul_flex_rl2", "t_shoul_ext_rl2", "t_elbow_flex_rl2",
                    "t_elbow_ext_rl2"
            , "t_wrist_flexrr2", "t_wrist_extrr2", "t_grip_rl2", "thip_abd_rl2", "t_hip_add_rl2", "t_hip_flex_rl2",
                    "t_hip_ext_rl2"
            , "t_kenee_flex_rl2", "t_kenee_ext_rl2"  # 142
            , "t_ankle_dor_rl2", "t_ankle_plantar_rl2","MAS result"

                         ]
        self.valuesarray = ["none"]*145
        print(self.valuesarray)
        self.patienticnum = "default"

    def saveToArray(self,*kwargs):
        words = []
        for i in kwargs:
            if i == "":
                print("blank data spotted")
                i  ="none"
                words.append(i)
            else:
                words.append(i)
        print(words)
        print(len(words))
        return words

    def savedata(self,keys,value,pid):
        if os.path.exists("userdata.json"):
            if self.CheckEmpty(pid):
                with open("userdata.json", 'r') as f:
                    self.userdata = {}
                    self.userdata = json.load(f)

                with open("userdata.json", "w") as f:
                    self.assignvalue(keys,value,pid)
                    json.dump(self.userdata, f, indent=4)

                print("file exist")
                return 1

            else:
                print("invalid data")
                return 0

        else:
            if self.CheckEmpty(pid):
                print("file not exist")
                self.userdata = OrderedDict()
                self.assignvalue(self.keyarray,self.valuesarray,self.patienticnum)
                with open("userdata.json", 'w') as f:
                    self.assignvalue(keys,value,pid)
                    print("assign success")
                    json.dump(self.userdata, f, indent=4)
                    return 1

            else:
                print("data not full")
                return 0



    def CheckEmpty(self,pid):
        if(pid !=""):
            return True
        else:
            print("empty")
            return  False

    def assignvalue(self,keys,value,pid):
        self.temp2 = {}
        for i,v in zip(keys,value):
            self.temp = {}
            self.temp[pid] = {i:v}
            self.temp2.update(self.temp[pid])
            self.userdata[pid] = self.temp2

    def searchdata(self,input,datatype,rowcount):
        if os.path.exists("userdata.json"):
            with open("userdata.json", 'r') as f:
                self.userdata = OrderedDict()
                self.userdata = json.load(f)
                self.searchresult = {}
                print("enter search")
                self.array = self.DictToArray(self.userdata,input,datatype,rowcount)

                return self.array
        else:
            return False

    def DictToArray(self,userdata,input,datatype,rowcount):
        self.NewArray = []
        self.outputarray = []
        for i in userdata:
            if input in userdata[i][datatype] and i != "default":
                self.NewArray = [i]
                for v in userdata[i].values():
                    self.NewArray.append(v)
                if self.outputarray == []:
                    self.outputarray = numpy.array(self.NewArray)
                else:
                    self.outputarray = numpy.vstack([self.outputarray,self.NewArray])
        self.outputarray = numpy.array(self.outputarray)
        self.getdimarray = self.outputarray.tolist()
        if self.outputarray.ndim == 1 and self.getdimarray !=[]:
            print("damn it")
            self.NewArray = ["default"]
            print(self.outputarray)
            for v in userdata["default"].values():
                self.NewArray.append(v)
            self.outputarray = numpy.vstack([self.outputarray, self.NewArray])

        print(self.outputarray)
        if self.getdimarray != []:
            self.outputarray1 = self.outputarray[:, :rowcount]
            self.outputarray = numpy.append(self.outputarray1,self.outputarray[:,-1:],axis=1)

        print(self.outputarray)
        self.outputarray = numpy.array(self.outputarray)
        return self.outputarray




    def setDefaultData(self):
        self.savedata(self.keyarray,self.valuesarray,self.patienticnum)




