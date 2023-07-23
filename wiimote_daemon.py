#!/usr/bin/env python

import cwiid
import time
from picamera import *

activeCamera = False
button_timeout = 0.1
button_timeout_long = 0.2

p = Picamera2()
#preview_config = p.configure(p.create_video_configuration({"size":(480,320)}))
#
preview_config = p.create_preview_configuration()
#preview_config["transform"] = libcamera.Transform(vflip=1,hflip=1)
#preview_config["transform"] = libcamera.Transform(hflip=1)
#preview_config["size"] = (480,320)
p.configure(preview_config)

p.controls.FrameDurationLimits = (40000, 40000)
p.controls.Brightness = 0.45
p.controls.Saturation = 0.7
p.controls.Sharpness = 2
p.controls.AwbEnable = True
p.controls.NoiseReductionMode = 1
#print(p.camera_controls)
#time.sleep(15)
print('Camera configuration ready')

def main():
	import uinput as kb
	global button_timeout
	global activeCamera
	global p

	while True:
		try:
			print('\n**\n* Press button 1 + 2 on the Wiimote...\n**\n')
			time.sleep(3)

			wm=cwiid.Wiimote()
			print('\n**\n* Wiimote connected...\n* Press the HOME and + button to disconnect\n**\n')
			wm.led = 6
			wm.rumble = True
			time.sleep(0.25)
			wm.rumble = False
			Rumble = False
			wm.rpt_mode = cwiid.RPT_BTN

			break
		except KeyboardInterrupt:
			exit(0)
		except:
			print('\n**\n* Wiimote not found... retrying\n**\n')
	while True:
		#
		# 2048 - UP DPAD
		# 1024 - DOWN DPAD
		# 512 - RIGHT DPAD
		# 256 - LEFT DPAD
		#
		# 8 - A KEY
		# 4 - B KEY
		#
		# 16 - MINUS KEY
		# 128 - HOME KEY
		# 4096 - PLUS KEY
		#
		# 2 - 1 KEY
		# 1 - 2 KEY
		#
		if wm.state['buttons'] == 2048:
			if not activeCamera:
				with kb.Device([kb.KEY_UP]) as dev:
					dev.emit_combo([kb.KEY_UP])
				time.sleep(button_timeout)

		if wm.state['buttons'] == 1024:
			if not activeCamera:
				with kb.Device([kb.KEY_DOWN]) as dev:
					dev.emit_combo([kb.KEY_DOWN])
				time.sleep(button_timeout)

		if wm.state['buttons'] == 512:
			if not activeCamera:
				with kb.Device([kb.KEY_RIGHT]) as dev:
					dev.emit_combo([kb.KEY_RIGHT])
				time.sleep(button_timeout)

		if wm.state['buttons'] == 256:
			if not activeCamera:
				with kb.Device([kb.KEY_LEFT]) as dev:
					dev.emit_combo([kb.KEY_LEFT])
				time.sleep(button_timeout)

		if wm.state['buttons'] == 4:
			if not activeCamera:
				with kb.Device([kb.KEY_ENTER]) as dev:
					dev.emit_combo([kb.KEY_ENTER])
				time.sleep(button_timeout_long)

#		if wm.state['buttons'] == 8:
#			if activeCamera:
#				cameraSwap(0)
#			time.sleep(button_timeout)

#		if wm.state['buttons'] == 2:
#			if activeCamera:
#				cameraSwap(2)
#			time.sleep(button_timeout_long)

		if wm.state['buttons'] == 8:
			cameraSwap(1)
			time.sleep(button_timeout_long)

		if wm.state['buttons'] == 16:
			Rumble = not Rumble
			wm.rumble = Rumble
			time.sleep(1)

		if wm.state['buttons'] == 4224:
			print('closing Bluetooth connection. Good Bye!')
			time.sleep(button_timeout)
			exit(wm)

def cameraSwap(mode):
	global p
	global activeCamera

	if (mode == 0):
		activeCamera = False
	else:
		activeCamera = not activeCamera

	if activeCamera:
		p.start_preview(Preview.DRM, x=0, y=0, width=720, height=480)
		p.start()
	else:
		p.stop_preview()
		p.stop()

if __name__ == "__main__":
	main()
