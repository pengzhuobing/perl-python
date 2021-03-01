from multiprocessing import Pool
import sys
import os
import time
import random
import glob
import shutil #删除非空文件夹

start = time.time()

if os.name != 'nt':
    # linux 才导入文件锁的包
    import fcntl

# IDlst = "D:/2_work/myGit/data/metaseq/ID.lst"
# resultfile = "D:/2_work/myGit/data/metaseq/out.fq"
# filepath = "D:/2_work/myGit/data/metaseq/"
# fq1 = "D:/2_work/myGit/data/metaseq/BI.1.fq"
# fq2 = "D:/2_work/myGit/data/metaseq/BI.2.fq"

IDlst = "./161-2_1/Assemble_BI/ID.lst"
resultfile = "./out.fq"
filepath = "./161-2_1/Assemble_BI/"
fq1 = "./161-2_1/mash/BI.1.fq"
fq2 = "./161-2_1/mash/BI.2.fq"

def run_task(shell, path):
    #tt = random.randint(0, 10)
    if os.name == 'nt':
        os.system(shell) # windows 好像不用加sh
    else:
        os.system("sh %s" % shell)  # linux需要加sh
    #print("Start task, sleep: %s" % tt, shell)
    #time.sleep(tt)

    #if os.system("sh %s" % shell) != 0:
    #if os.system(shell) != 0:
    #     raise Exception("Thread exit nonzero")
    return path

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print("---  new folder...  ---")
        print("---  OK  ---")
    else:
        print( "---  There is this folder!  ---")

def Idvd(idvd):
    BCS = {}
    BCR = {}
    with open(idvd, 'r') as DD:
        for line in DD:
            line.strip()
            line = line.split("\t")
            BCS[line[0]] = line[1]
            BCR[line[0]] = line[2]
    return BCS, BCR

class TaskGenerate:

    def get_flock(self):
        # 获取文件锁，文件再被其他进程操作则会等待锁释放
        print("加锁中....")
        if os.name == 'nt':
            # windows 直接返回
            return
        fcntl.flock(self.output_fh, fcntl.LOCK_EX)
        print("加锁成功.")

    def release_flock(self):
        if os.name == 'nt':
            # windows 直接返回
            return
        fcntl.flock(self.output_fh, fcntl.LOCK_UN)
        print("锁释放成功....")

    def __init__(self, thread=2):
        self.thread = thread
        self.result_file = resultfile
        #self.output_fh = None
        self.p = None
        self.output_fh = open(self.result_file, 'w')
        self.current_task_number = 0
        pass

    def init(self):
        pass


    def run(self, target_func):
        def error_callback(data):
            print("=====================run error: %s" % data)
            # 某个样本运行失败，直接退出运行
            self.p.terminate()

        def success(data):
            print("Task complete, current_task_number: %s, return data: %s" % (self.current_task_number, data))
            self.current_task_number -= 1
            if glob.glob(data):
                self.get_flock()
                # 将所有文件输出到result中
                OUT = os.path.join(data + '/RCAclip.fa')
                OO = open(OUT)
                result = OO.read()
                self.output_fh.write(result)
                self.release_flock() # 进程结束后解锁
                OO.close()
                #os.remove(OUT) # 删除单个文件
                shutil.rmtree(data)
            else:
                print("no")


        self.p = Pool(self.thread)
        fh1 = open(fq1, "r")
        fh2 = open(fq2, "r")
        BCS, BCR = Idvd(IDlst)
        max_pending_task = self.thread * 2
        for key in BCS:
            # 保证最大投递任务数不超过 max_pending_task
            while self.current_task_number > max_pending_task:
                print(self.current_task_number, "waiting----")
                time.sleep(5)
            oDir = os.path.join(filepath, str('BI' + "%08d" % int(key)))
            mkdir(oDir)
            out1 = open(oDir + "/sort.1.fq", "w")
            out2 = open(oDir + "/sort.2.fq", "w")
            bc = BCS[key]
            rpb = BCR[key]
            ee = bc.replace("_","")
            # barName = ee
            # if ee < barName:
            #    print("error: ", ee, "is less than last bb, Make sure the IDs are ordered.")
            #    break
            rd = 0
            while True:
                line = fh1.readline()
                if not line:
                    break
                iID = line
                barName = iID.split("/")[1]
                barName = barName.replace("_","") # 替换_为空
                if barName < ee:
                    fh1.readline()
                    fh1.readline()
                    fh1.readline()
                    continue
                rd += 1
                out1.writelines(line)
                out1.writelines(fh1.readline())
                out1.writelines(fh1.readline())
                out1.writelines(fh1.readline())
                out2.writelines(fh2.readline())
                out2.writelines(fh2.readline())
                out2.writelines(fh2.readline())
                out2.writelines(fh2.readline())
                if rd == int(rpb):
                    batchName = '/batch.assemble.BI' + str("%08d" % int(key)) + '.sh'
                    fhs = open(oDir + batchName, 'w')
                    neirong = "cat " + oDir + "/sort.1.fq >" + oDir + "/RCAclip.fa"
                    #neirong = 'metabbq RCAasm.sh megahit SAM/159_1 BI ' + key + ' BI 10000000000 1 SAM/159_1/primers.cfg'
                    #neirong = 'metabbq RCAasm.sh megahit 161-2_1 BI ' + key + ' BI 10000000000 1 161-2_1/primers.cfg'
                    fhs.writelines(neirong)
                    fhs.close()
                    shellname = oDir + batchName # shell文件
                    self.p.apply_async(run_task, args=(shellname, oDir), callback=success,
                                       error_callback=error_callback) # 多线程执行多个shell文件
                    self.current_task_number += 1
                    break
            out1.close()
            out2.close()
        fh1.close()
        fh2.close()
        self.p.close()
        self.p.join()

    def generate_next_task(self):
        pass

if __name__ == '__main__':
    task_generator = TaskGenerate(2)
    task_generator.run(run_task)

end = time.time()
print(end-start)