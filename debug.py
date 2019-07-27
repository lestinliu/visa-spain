import subprocess

from visa import Visa

visa = Visa(None)
visa.enable_vpn("Germany")