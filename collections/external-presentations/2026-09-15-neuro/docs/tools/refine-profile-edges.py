"""Remove blue studio spill only along the local segmentation boundary."""
from pathlib import Path
import sys
import numpy as np
from PIL import Image, ImageFilter
for p in Path(sys.argv[1]).glob('*-transparent.png'):
    im = Image.open(p).convert('RGBA')
    a = np.asarray(im).astype(float)
    alpha = a[:, :, 3] / 255
    radius = max(3, int(im.width * .035) | 1)
    inner = np.asarray(im.getchannel('A').filter(ImageFilter.MinFilter(radius))).astype(float) / 255
    boundary = inner < .98
    r,g,b = a[:,:,0],a[:,:,1],a[:,:,2]
    blue = np.clip((b-r-18)/32,0,1)*np.clip((g-r-4)/22,0,1)*np.clip((b-65)/35,0,1)
    a[:,:,3] = 255 * alpha * (1-blue*boundary)
    Image.fromarray(a.clip(0,255).astype('uint8')).save(p)
