from pytapo import Tapo
tapo = Tapo("10.109.68.15", "same_shield.1h@icloud.com", "mateo1234", "mateo1234")
print("Connected!")
print(tapo.getDeviceInfo())
