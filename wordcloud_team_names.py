from os import path
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator



# Read the whole text.
text = open('names.txt').read()

# read the mask image
# taken from
kcbs_mask = np.array(Image.open('mask.png'))

wc = WordCloud(background_color="white", max_words=2000, mask=kcbs_mask)
# generate word cloud
wc.generate(text)

fire_coloring = np.array(Image.open("fire.png"))
image_colors = ImageColorGenerator(fire_coloring)

# store to file
wc.to_file('wordcloud.png')

# show
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(wc.recolor(color_func=image_colors), interpolation="bilinear")
plt.axis("off")
plt.figure()
plt.imshow(fire_coloring, cmap=plt.cm.gray, interpolation="bilinear")
plt.axis("off")
plt.show()
