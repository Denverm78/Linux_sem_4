import pytest
from sshcheckers import ssh_checkout
import random, string
import yaml
from datetime import datetime


with open('config.yaml') as f:
   data = yaml.safe_load(f)


@pytest.fixture()
def make_folders():
   return ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'mkdir {data.get("folder_in")} {data.get("folder_out")} {data.get("folder_ext")} {data.get("folder_ext2")}', "")


@pytest.fixture()
def clear_folders():
   return ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'rm -rf {data.get("folder_in")}/* {data.get("folder_out")}/* {data.get("folder_ext")}/* {data.get("folder_ext2")}/*', "")


@pytest.fixture()
def make_files():
   list_of_files = []
   for i in range(data["count"]):
       filename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
       if ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; dd if=/dev/urandom of={filename} bs=1M count=1 iflag=fullblock', ""):
           list_of_files.append(filename)
   return list_of_files


@pytest.fixture()
def make_subfolder():
   testfilename = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
   subfoldername = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
   if not ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; mkdir {subfoldername}', ""):
       return None, None
   if not ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}/{subfoldername}; dd if=/dev/urandom of={testfilename} bs=1M count=1 iflag=fullblock', ""):
       return subfoldername, None
   else:
       return subfoldername, testfilename


@pytest.fixture()
def make_bad_arx():
   ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'cd {data.get("folder_in")}; 7z a {data.get("folder_out")}/arxbad -t{data.get("type")}', "Everything is Ok")
   ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'truncate -s 1 {data.get("folder_out")}/arxbad.{data.get("type")}', "Everything is Ok")
   yield "arxbad"
   ssh_checkout(data.get("ip"), data.get("user"), data.get("passwd"), f'rm -f {data.get("folder_out")}/arxbad.{data.get("type")}', "")


@pytest.fixture(autouse=True)
def print_time():
   print(f'Start: {datetime.now().strftime("%H:%M:%S.%f")}')
   yield print(f'Stop: {datetime.now().strftime("%H:%M:%S.%f")}')


@pytest.fixture()
def start_time():
   return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


