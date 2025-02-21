
import os, cv2
import numpy as np

cap = cv2.VideoCapture(0)

ilumitaion_values: str = 'Ñ@#W$9876543210?!abc:;+=-,._   '[::-1]

terminal_res: tuple = os.get_terminal_size()
width, height = terminal_res

linspace_rgb = list(np.linspace(0, 255, len(ilumitaion_values), dtype=np.integer))

if not cap.isOpened():
    print('Could not open the webcam.')
    exit()

def generate_ascii(pixels: object) -> None:

    def get_ilum_value(rgb: tuple) -> str:
        avg: int = np.mean(rgb[:3])
        val: int = min(linspace_rgb, key=lambda x: abs(x - avg))
        return ilumitaion_values[linspace_rgb.index(val)]

    output: str = ''
    for x in range(height):
        for y in range(width):
            output += get_ilum_value(pixels[x, y])

    print(output, end='', flush=True)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    pixels = cv2.resize(frame, terminal_res)
    generate_ascii(pixels)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()