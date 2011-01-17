#
#  main.py
#  osm2spatialite
#
#  Created by Daniel Sabo on 1/16/11.
#  Copyright __MyCompanyName__ 2011. All rights reserved.
#

#import modules required by application
import objc
import Foundation
import AppKit

from PyObjCTools import AppHelper

# import modules containing classes required to start application and load MainMenu.nib
import osm2spatialiteAppDelegate

# pass control to AppKit
AppHelper.runEventLoop()
