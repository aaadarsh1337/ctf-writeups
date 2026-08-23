import zlib

data = open("configdata.deflate", "rb").read()
out = zlib.decompress(data, -15)
open("payload.exe", "wb").write(out)

print("Written payload.exe:", len(out), "bytes")
