import yaml
from checkers import getout
from sshcheckers import ssh_checkout, upload_files, ssh_getout


with open('config.yaml') as f:
   data = yaml.safe_load(f)

class TestPositive:


   def save_log(self, starttime, name):
       with open(name, 'w') as f:
           f.write(getout(f'journalctl --since "{starttime}"'))

   def test_step1(self, start_time):
       res = []
       upload_files(data.get("ip"), data.get("user"), data.get("passwd"), data.get("pkgname")+".deb",
                    f'/home/{data.get("user")}/{data.get("pkgname")}.deb')
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "echo '{}' | sudo -S dpkg -i"
               " /home/{}/{}.deb".format(data.get("passwd"), data.get("user"), data.get("pkgname")),
                               "Настраивается пакет"))
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "echo '{}' | "
                   "sudo -S dpkg -s {}".format(data.get("passwd"), data.get("pkgname")),
                               "Status: install ok installed"))
       self.save_log(start_time, "log1.txt")
       assert all(res), "test1 FAIL"

   def test_step2(self, make_folders, clear_folders, make_files, start_time):
       res1 = ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "cd {};"
           " 7z a {}/arx2".format(data.get("folder_in"), data.get("folder_out")), "Everything is Ok")
       res2 = ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'ls {data.get("folder_out")}', "arx2.7z")
       self.save_log(start_time, "log2.txt")
       assert res1 and res2, "test2 FAIL"

   def test_step3(self, clear_folders, make_files, start_time):
       res = []
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "cd {}; 7z a "
           "{}/arx2".format(data.get("folder_in"), data.get("folder_out")), "Everything is Ok"))
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "cd {}; 7z e "
           "arx2.7z -o{} -y".format(data.get("folder_out"), data.get("folder_ext")), "Everything is Ok"))
       for item in make_files:
           res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'ls {data.get("folder_ext")}', item))
       self.save_log(start_time, "log3.txt")
       assert all(res), "test3 FAIL"

   def test_step4(self, start_time):
       self.save_log(start_time, "log4.txt")
       assert ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_out")}; 7z t arx2.7z', "Everything is Ok"), "test4 FAIL"

   def test_step5(self, start_time):
       self.save_log(start_time, "log5.txt")
       assert ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; 7z u arx2.7z', "Everything is Ok"), "test5 FAIL"

   def test_step6(self, clear_folders, make_files, start_time):
       res = []
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arx2', "Everything is Ok"))
           
       for item in make_files:
           res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "cd {}; 7z l"           # ????????
           " arx2.7z".format(data.get("folder_out"), data.get("folder_ext")), item))
       self.save_log(start_time, "log6.txt")
       assert all(res), "test6 FAIL"

   def test_step7(self, clear_folders, make_files, make_subfolder, start_time):
       res = []
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arx', "Everything is Ok"))
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_out")}; 7z x arx.7z -o{data.get("folder_ext2")} -y', "Everything is Ok"))
       for item in make_files:
           res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "ls {}".format(data.get("folder_ext2")), item))
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'ls {data.get("folder_ext2")}', make_subfolder(0)))
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'ls {data.get("folder_ext2")}/{make_subfolder(0)}', make_subfolder(1)))
       self.save_log(start_time, "log7.txt")
       assert all(res), "test7 FAIL"

   def test_step8(self, start_time):
       self.save_log(start_time, "log8.txt")
       assert ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_out")}; 7z d arx.7z', "Everything is Ok"), "test8 FAIL"

   def test_step9(self, clear_folders, make_files, start_time):
       self.save_log(start_time, "log9.txt")
       res = []
       for item in make_files:
           res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; 7z h {item}', "Everything is Ok"))
           hash = ssh_getout(data.get("ip"), data.get("user"), data.get("passwd"), "cd {}; "
                                                                   "crc32 {}".format(data.get("folder_in"), item)).upper()
           res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; 7z h {item}', hash))
       assert all(res), "test9 FAIL"

   def test_step10(self, start_time):
       res = []
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "echo '{}' | sudo -S dpkg -r"
                                                                         " {}".format(data.get("passwd"), data.get("pkgname")),
                               "Удаляется"))
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "echo '{}' | "
                                                                         "sudo -S dpkg -s {}".format(data.get("passwd"),
                                                                                                     data.get("pkgname")),
                               "Status: deinstall ok"))
       assert all(res), "test10 FAIL"