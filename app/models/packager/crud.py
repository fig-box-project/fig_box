import yaml
import os
import zipfile

class Packager:
    # 标识文件夹是否有更新过
    stamp:dict #str:bool
    
    def __init__(self):
        os.makedirs("files", exist_ok=True)
        os.makedirs("files/packager", exist_ok=True)
        if os.path.exists("files/packager/stamp.yaml"):
            with open("files/packager/stamp.yaml", "r") as f:
                self.stamp = yaml.load(f)
        else:
            self.stamp = {}
    
    # 关闭服务器前先运行一下这个
    def dump(self):
        with open("files/packager/stamp.yaml", "w") as f:
            yaml.dump(self.stamp, f)

    # 某个包中发生了更改
    def updated_files(self,package_name):
        self.stamp[package_name] = True
    
    # 打包某个包
    def pack(self,package_name):
        # 如果存在该文件夹
        if os.path.exists( "files/" + package_name):
            # 如果dict里有
            if package_name in self.stamp.keys():
                if self.stamp[package_name] == True:
                    self.pack_files(package_name)
                    self.stamp[package_name] = False
                    return True
                else:
                    return True
            else:
                self.pack_files(package_name)
                self.stamp[package_name] = False
                return True
        else:
            # 没有文件夹,无法打包
            return False

    # 打包
    def pack_files(self,package_name):
        zip = zipfile.ZipFile("files/packager/{}.zip".format(package_name),"w",zipfile.ZIP_DEFLATED)
        for path,dirs,files in os.walk("files/{}".format(package_name)):
            file_path = path.replace("files/{}".format(package_name),"")
            for file in files:
                zip.write(os.path.join(path,file),os.path.join(file_path,file))
        zip.close()

packager = Packager()