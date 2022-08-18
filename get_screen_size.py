import os

def get_ss():
	try:
		cmd = 'wmic desktopmonitor get screenheight, screenwidth'
		size_tuple = tuple(map(int,os.popen(cmd).read().split()[-2::]))
	except:
		try:
			cmd = "wmic path Win32_VideoController get CurrentVerticalResolution,CurrentHorizontalResolution"
			size_tuple = tuple(map(int,os.popen(cmd).read().split()[-2::]))
		except:
			screen = os.popen("xrandr -q -d :0").readlines()[0]
			width = screen.split()[7]
			height = screen.split()[9][:-1]
			size_tuple = tuple(height, width)

	return size_tuple