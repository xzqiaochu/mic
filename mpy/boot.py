from Maix import MIC_ARRAY as mic
# import lcd

ID = 0x01

mic.init()
brightness = [0 for _ in range(12)]
mic.set_led(brightness, (0, 0, 0))
# lcd.init()

while True:
    imga = mic.get_map()
    msg = [0xA5, ID]
    s = 0
    for i in range(16 * 16):
        data = imga[i]
        msg.append(data)
        s = s + data
    msg.append(s % 0x100)
    msg.append(0x5A)
    #print(len(msg))
    for data in msg:
        print("%c" % data, end = "")

    brightness = mic.get_dir(imga)
    mic.set_led(brightness, (255, 0, 0))

    # imgb = imga.resize(160,160)
    # imgc = imgb.to_rainbow(1)
    # lcd.display(imgc)
mic.deinit()
