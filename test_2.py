from sshcheckers import ssh_checkout_negative, ssh_checkout
import yaml


with open('config.yaml') as f:
   data = yaml.safe_load(f)


class Testneg:
   def test_nstep1(self, make_folders, make_bad_arx):
       # test neg 1
       assert ssh_checkout_negative(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_out")}; 7z e {make_bad_arx}.{data.get("type")} -o{data.get("folder_ext")} -y', "ERROR:"), "test1 FAIL"


   def test_nstep2(self, make_bad_arx):
       # test neg 2
       assert ssh_checkout_negative(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_out")}; 7z t {make_bad_arx}.{data.get("type")}', "ERROR:"), "test2 FAIL"


   def test_nstep3(self):
       res = []
       res.append(ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), "echo '{}' | sudo -S dpkg -r"
                                                                         " {}".format(data.get("passwd"), data.get("pkgname")),
                               "Удаляется"))
       res.append(ssh_checkout(data["ip"], data["user"], data["passwd"], "echo '{}' | "
                                                                         "sudo -S dpkg -s {}".format(data.get("passwd"), data.get("pkgname")),
                               "Status: deinstall ok"))
       assert all(res), "test3 FAIL"

