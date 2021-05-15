#-*- encoding: utf8 -*-
import os
import sys
import ftplib


class FTPSync(object):
    def __init__(self):
        self.ftp = ftplib.FTP('127.0.0.1','softwares_sun','12345')
        self.ftp.encoding = 'utf-8'
        #self.ftp.cwd('/0428')   # 远端FTP目录
        #os.chdir('G:/ftpdata')        # 本地下载目录

    def get_dirs_files(self):
        u''' 得到当前目录和文件, 放入dir_res列表 '''
        dir_res = []
        self.ftp.dir('.', dir_res.append)
        print("dir+++",dir_res)
        files = [f.split(None, 8)[-1] for f in dir_res if f.startswith('-')]
        dirs = [f.split(None, 8)[-1] for f in dir_res if f.startswith('d')]
        return (files, dirs)

    def walk(self, remotedir, localdir):
        print('Walking to', remotedir,os.getcwd())
        self.ftp.cwd(remotedir)
        print("now2", os.getcwd())
        try:
            os.mkdir(remotedir)
            print("make dir",remotedir)
        except OSError:
            print("make dir error", remotedir)
            pass
        os.chdir(localdir)
        print("now dir", os.getcwd())
        ftp_curr_dir = self.ftp.pwd()
        local_curr_dir = localdir
        print("ftp_curr_dir",ftp_curr_dir)
        print("local dir",local_curr_dir)
        files, dirs = self.get_dirs_files()
        print("FILES: ", files)
        print("DIRS: ", dirs)
        for f in files:
            print(remotedir, ':', f)
            outf = open(f, 'wb')
            try:
                self.ftp.retrbinary('RETR %s' % f, outf.write)
            finally:
                outf.close()
        for d in dirs:
            print("Dir:", d, ftp_curr_dir)
            os.chdir(local_curr_dir)
            print("local ok")
            #self.ftp.cwd(ftp_curr_dir)
            self.walk(d,os.path.join(localdir,d))
        self.ftp.cwd('..')

    def download_dir(self,romotedir,localdir):
        os.chdir(localdir)
        print("now",os.getcwd())
        self.walk(romotedir,localdir)

    def upload_dir(self, remotedir='./', localdir='./'):
        '''
        实现文件的上传
        :param localdir: 
        :param remotedir: 
        :return: 
        '''
        print("start",remotedir,localdir)
        if not os.path.isdir(localdir):
            print("not")
            return
        print("DIR",remotedir,self.ftp.pwd())
        self.ftp.cwd(remotedir)
        print("CWD",self.ftp.pwd())
        for file in os.listdir(localdir):
            #src = os.path.join(localdir, file)
            src = localdir+'/'+file
            if os.path.isfile(src):
                self.upload_file(file,src)
            elif os.path.isdir(src):
                try:
                    self.ftp.mkd(file)
                except:
                    sys.stderr.write('the dir is exists %s' % file)
                self.upload_dir(file,src)
        self.ftp.cwd('..')

    def uploadFile(self, localpath, remotepath='./'):
        if not os.path.isfile(localpath):
            return
        print('+++ upload %s to %s' % (localpath, remotepath))
        self.ftp.storbinary('STOR ' + remotepath, open(localpath, 'rb'))
    def upload_file(self, remotepath:str ,localpath:str):
        """
        上传本地文件到服务器
        :param remotepath:  远端路径
        :param localpath:  本地路径
        :return: None
        """
        while  '//' in remotepath:
            remotepath = remotepath.replace('//', '/')
        while '//' in localpath:
            localpath = localpath.replace('//', '/')

        bufsize = 1024
        print(localpath)
        fp = open(localpath, 'rb')
        self.ftp.storbinary('STOR ' + remotepath, fp, bufsize)
        self.ftp.set_debuglevel(0)
        fp.close()
        print("上传本地文件：", localpath, "\t到远程：",remotepath , "成功")
def main():
    f = FTPSync()
    #f.run('test','G:/ftpdata/test10')
    #f.upload_dir('/数据/hello','G:/ftpdata/数据')
    f.download_dir('/test','G:/ftpdata/test')




if __name__ == '__main__':
    main()

