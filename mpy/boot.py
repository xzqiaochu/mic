from Maix import MIC_ARRAY as mic
# import lcd

f = open('id.txt', 'r')
ID = int(f.read())
f.close()

mic.init()
mic.set_led([0 for _ in range(12)], (0, 0, 0))
# lcd.init()

while True:
    imga = mic.get_map()
    msg = [0xA5, ID]
    s = 0
    valid = False
    for i in range(16 * 16):
        data = imga[i]
        if data != 0:
            valid = True
        msg.append(data)
        s = s + data
    msg.append(s % 0x100)
    msg.append(0x5A)
    if valid:
        for data in msg:
            print("%c" % data, end = "")

    mic.set_led(mic.get_dir(imga), (255, 0, 0))

    # imgb = imga.resize(160,160)
    # imgc = imgb.to_rainbow(1)
    # lcd.display(imgc)
mic.deinit()
