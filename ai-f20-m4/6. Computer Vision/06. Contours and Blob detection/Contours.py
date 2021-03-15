import cv2
import matplotlib.pyplot as plt
import numpy as np
path_coins = 'ai-f20-m4/6. Computer Vision/06. Contours and Blob detection/img/coins{}.jpg'
color_coins = cv2.imread(path_coins.format('5'), cv2.IMREAD_COLOR)
print(color_coins)
rgb_coins = cv2.cvtColor(color_coins, cv2.COLOR_BGR2RGB)

plt.figure(figsize= (12,8))
plt.imshow(rgb_coins)
plt.show()
