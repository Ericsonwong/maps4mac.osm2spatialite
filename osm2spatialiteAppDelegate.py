#
#  osm2spatialiteAppDelegate.py
#  osm2spatialite
#
#  Created by Daniel Sabo on 1/16/11.
#  Copyright __MyCompanyName__ 2011. All rights reserved.
#

from Foundation import *
from AppKit import *
import os.path
import osm2spatialite

class osm2spatialiteAppDelegate(NSObject):
    mainWindow = objc.IBOutlet()

    inputFilenameField  = objc.IBOutlet()
    outputFilenameField = objc.IBOutlet()
    
    hasProtoBuf = objc.ivar()
    
    importWindow = objc.IBOutlet()
    importWindowCurrentStage        = objc.IBOutlet()
    importWindowCurrentStageDesc    = objc.IBOutlet()
    importWindowCurrentStageTime    = objc.IBOutlet()
    importWindowCurrentStagePercent = objc.IBOutlet()

    def applicationDidFinishLaunching_(self, sender):
        try:
            import fileformat_pb2,osmformat_pb2
            hasProtoBuf = True
        except ImportError:
            hasProtoBuf = False
        
        try:
            import shapely,shapely.geos
        except ImportError:
            title = "Coldn't find geos"
            msg = "You need to install the GEOS framework to use this application."
            alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(title, None, None, None, msg)
            alert.runModal()
            NSApp.terminate_(None)
        print shapely

    @objc.IBAction
    def selectOSMFile_(self, sender):
        panel = NSOpenPanel.alloc().init()
        panel.setTitle_("Select Input File")
        panel.setAllowsOtherFileTypes_(True)
        panel.setCanSelectHiddenExtension_(True)
        filetypes = ["osm"]
        #if self.hasProtoBuf:
        #    filetypes.append("pbf")
        if NSOKButton == panel.runModalForDirectory_file_types_(NSHomeDirectory(), None, filetypes):
            filename = panel.filename()
            self.inputFilenameField.setStringValue_(filename)
    
    @objc.IBAction
    def selectOutputFile_(self, sender):
        panel = NSSavePanel.alloc().init()
        panel.setTitle_("Select Output File")
        panel.setAllowsOtherFileTypes_(True)
        panel.setCanSelectHiddenExtension_(True)
        panel.setAllowedFileTypes_(["osm2spatialite"])
        if NSOKButton == panel.runModal():
            filename = panel.filename()
            if not os.path.splitext(filename)[1]:
                filename = filename + ".osm2spatialite"
            self.outputFilenameField.setStringValue_(filename)
    
    def importReportStatus(self, msg):
        self.performSelectorOnMainThread_withObject_waitUntilDone_("mainThreadUpdate:", msg, False)
        
    def importReportDetails(self, msg):
        self.performSelectorOnMainThread_withObject_waitUntilDone_("mainThreadUpdateDetails:", msg, False)
    
    def importThread_(self, args):
        pool = NSAutoreleasePool.alloc().init()
        
        self.performSelectorOnMainThread_withObject_waitUntilDone_("mainThreadUpdate:", "Hello from the thread", False)
        osm2spatialite.reportStatus = self.importReportStatus
        osm2spatialite.reportDetailedProgress = self.importReportDetails
        db = osm2spatialite.trydb(args["outfile"], True)
        if db:
            osm2spatialite.parseFile(args["infile"], db, config=osm2spatialite.defaultConfig, verbose=True)
            self.performSelectorOnMainThread_withObject_waitUntilDone_("mainThreadImportDone:", args["outfile"], False)
        else:
            self.performSelectorOnMainThread_withObject_waitUntilDone_("mainThreadAbortMsg:", "Could not open DB", False)
    
    def mainThreadUpdate_(self, msg):
        self.importWindowCurrentStage.setStringValue_(msg)
        
    def mainThreadUpdateDetails_(self, msg):
        if "nodes" in msg:
            nodes = msg["nodes"]
        else:
            nodes = 0
            
        if "ways" in msg:
            ways = msg["ways"]
        else:
            nodes = 0
            
        if "relations" in msg:
            relations = msg["relations"]
        else:
            relations = 0
        
        msg = "nodes(%d) ways(%d) relations(%d)" % (nodes, ways, relations)
        self.importWindowCurrentStageDesc.setStringValue_(msg)
    
    def mainThreadImportDone_(self, msg):
        self.mainWindow.makeKeyAndOrderFront_(self)
        self.importWindow.orderOut_(self)
        self.importWindowCurrentStagePercent.stopAnimation_(self)
        
        title = "Import Completed"
        msg = "The database was successfully created:\n" + msg
        alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(title, None, None, None, msg)
        alert.runModal()
    
    def mainThreadAbortMsg_(self, msg):
        self.mainWindow.makeKeyAndOrderFront_(self)
        self.importWindow.orderOut_(self)
        self.importWindowCurrentStagePercent.stopAnimation_(self)
        
        title = "Import failed"
        alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(title, None, None, None, msg)
        alert.runModal()
    
    @objc.IBAction
    def doImport_(self, sender):
        self.mainWindow.orderOut_(self)
        infile = self.inputFilenameField.stringValue()
        outfile = self.outputFilenameField.stringValue()
        threadParams = {
            "infile":infile,
            "outfile":outfile,
            }
        
        NSThread.detachNewThreadSelector_toTarget_withObject_(self.importThread_,self,threadParams)
        self.importWindowCurrentStagePercent.setIndeterminate_(True)
        self.importWindowCurrentStagePercent.startAnimation_(self)
        
        self.importWindow.makeKeyAndOrderFront_(self)
        #FIXME: Validate input filenames