import csv
import struct
import sys

from PIL import Image, ImageDraw

images = []

csv.field_size_limit(sys.maxsize)

format_descriptor = bytes.fromhex("1B 24 04 01 02 59 55 59 32 00 00 10 00 80 00 00 AA 00 38 9B 71 10 01 00 00 00 00")
print(len(format_descriptor))
frame_descriptor = bytes.fromhex("26 24 05 01 00 F0 00 41 01 00 40 19 01 00 C0 4B 03 00 08 07 00 2A 2C 0A 00 03 2A 2C 0A 00 40 42 0F 00 40 4B 4C 00 1E 24 05 02 00 00 05 D0 02 00 00 C2 01 00 00 C2 01 00 20 1C 00 40 4B 4C 00 01 40 4B 4C 00 0B 24 06 02 02 00 01 00 00 00 00 26 24 07 01 00 F0 00 41 01 00 40 19 01 00 C0 4B 03 00 08 07 00 2A 2C 0A 00 03 2A 2C 0A 00 40 42 0F 00 40")

bpp = format_descriptor[21]
format_guid = format_descriptor[5:21].hex()
width, height = struct.unpack_from("<xxxxxHH", frame_descriptor)

def to_rgb(y, u, v):
    r = (22987 * (v - 128)) >> 14
    g = (-5636 * (u - 128) - 11698 * (v - 128)) >> 14
    b = (29049 * (u - 128)) >> 14
    r = min(255, max(0, y + r))
    g = min(255, max(0, y + g))
    b = min(255, max(0, y + b))
    return (r, g, b)

print(bpp, format_guid, width, height)
with open("body_temp_cam.csv", "r") as f:
    reader = csv.reader(f)
    cols = {}
    i = 0
    last_data = None
    for row in reader:
        if row[0].startswith("#"):
            if len(row) > 2:
                row[0] = row[0][2:]
                for j, col in enumerate(row):
                    cols[col] = j
        else:
            data = bytes.fromhex(row[cols["Data"]])
            if len(data) == 154080:
                hist = {}
                im = Image.new('RGB', (240, 321))
                for z in range(len(data)):
                    if z % 4 != 0:
                        continue
                    # u = data[z]
                    # y1 = data[z + 1]
                    # v = data[z + 2]
                    # y2 = data[z + 3]
                    y1 = data[z]
                    u = data[z + 1]
                    y2 = data[z + 2]
                    v = data[z + 3]

                    x = z // 2 % 240
                    y = z // 2 // 240
                    if y < 320:
                        im.putpixel((x, y), to_rgb(y1, u, v))
                        im.putpixel((x + 1, y), to_rgb(y2, u, v))
                    elif y == 320:
                        print(len(images) + 1, data[z:z+5], struct.unpack("h", data[z:z+2]))
                        break
                images.append(im)
                im.save('thermal{:03d}.bmp'.format(len(images)))
                # if diff_count > 0:
                #     print(i, row[3], len(data), data[:9].hex())
                #     # print(hist)
                #     i += 1
                last_data = data

images[0].save('thermal.webp',
               save_all=True,
               lossless=True,
               append_images=images[1:],
               optimize=False,
               duration=40,
               loop=0)
