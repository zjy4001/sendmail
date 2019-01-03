#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os,sys
import time
import commands
import smtplib
from email.mime.text import MIMEText
reload(sys)
sys.setdefaultencoding('utf8')


mail_host = "mail.51talk.com"
mail_user = "opnotice@51talk.com"
mail_pass = "Bk(qdE2re.A("
logfile="/data/cron/java_nginx_check.log"
maillists = ['hanxiaoqi@51talk.com','cuijianping08@51talk.com','baopengfei@51talk.com']
#maillists = ['cuijianping08@51talk.com']


def check_nginx(shell):
  (status, output) = commands.getstatusoutput(shell)
  f = open(logfile,'a')
  #if status == 0:
  #  f.writelines('java-nginx 未上线服务器：'+'\n')
  #  f.writelines(output)
  #  f.close()
  #  return status
  #else:
  f.writelines('java-nginx conf 巡检内容：' +'\n')
  f.writelines(output)
  f.writelines('\n'+ '说明：non-zero return code 表示没有下线的服务器')
  f.close()
  return status
  
def send_mail(to_list,sub,content):
    me='opnotice@51talk.com'
    fp = open(content, 'rb')
    msg = MIMEText(fp.read(),'plain',_charset='utf-8')
    fp.close()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ",".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False

def mailto(maillist,logfile):
    x = open(logfile,'r')
    a = x.read()
    if len(a) !=0:
      sub = 'java-nginx conf 巡检'
      if send_mail(maillist,sub,logfile):
        print ("%s Java nginx check mail send success!"%(time.strftime('%Y-%m-%d %X', time.localtime())))
      else:
        print ("%s Java nginx check mail send failed!"%(time.strftime('%Y-%m-%d %X', time.localtime())))


if __name__ == "__main__":
  ansible='/usr/local/bin/ansible'
  hostfile = '/home/init/hosts/java.hosts'
  hostgroup = 'nginx'
  command = 'grep "\#\{1,\}server" /usr/local/nginx/conf/nginx.conf'
  shell="%s -i %s %s -m shell -a '%s'" % (ansible,hostfile,hostgroup,command)
  check_nginx(shell)
  mailto(maillists,logfile)
  os.remove(logfile)
