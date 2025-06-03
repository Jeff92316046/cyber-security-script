from PIL import Image, ImageSequence

# 開啟原始 GIF
original = Image.open("assets/nyamuchi.gif")

# 儲存處理過的每一幀
frames = []

for frame in ImageSequence.Iterator(original):
    # 轉為灰階
    gray = frame.convert("L")

    # 再轉回 "P" 模式，以符合 GIF 格式
    gray = gray.convert("P")

    frames.append(gray)

# 儲存成新的灰階 GIF
frames[0].save(
    "assets/nyamuchi_gray.gif",
    save_all=True,
    append_images=frames[1:],
    loop=0,
    duration=original.info.get('duration', 100),
    disposal=0
)