import numpy as np
import colorsys

def get_colors(num_colors):
	colors=[]
	for i in np.arange(0., 360., 360. / num_colors):
		hue = i/360.
		lightness = (50 + np.random.rand() * 10)/100.
		saturation = (90 + np.random.rand() * 10)/100.
		colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
	return colors

color_list = [
	# some example colors
	'#F4561D',
	'#F1911E',
	'#F1BD1A',
	# 16 color list
	'#AD2323',
	'#2A4BD7',
	'#1D6914',
	'#814A19',
	'#8126C0',
	'#A0A0A0',
	'#81C57A',
	'#9DAFFF',
	'#29D0D0',
	'#FF9233',
	'#FFEE33',
	'#E9DEBB',
	'#FFCDF3',
	'#FFFFFF',
	'#575757',
	'#000000'
]