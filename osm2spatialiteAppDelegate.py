#
#  osm2spatialiteAppDelegate.py
#  osm2spatialite
#
#  Created by Daniel Sabo on 1/16/11.
#  Copyright __MyCompanyName__ 2011. All rights reserved.
#

from Foundation import *
from AppKit import *
import copy
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
    
    requiredTagsArrayController = objc.IBOutlet()
    userTagsArrayController = objc.IBOutlet()
    editTagsWindow = objc.IBOutlet()
    userTagsTable = objc.IBOutlet()
    
    requiredTags = objc.ivar()
    userTags = objc.ivar()

    def applicationDidFinishLaunching_(self, sender):
        defaults = NSUserDefaults.standardUserDefaults()
        
        try:
            import OSMPBFParser
            self.hasProtoBuf = True
        except ImportError:
            self.hasProtoBuf = False
        
        try:
            import shapely,shapely.geos
        except ImportError:
            title = "Coldn't find geos"
            msg = "You need to install the GEOS framework to use this application."
            alert = NSAlert.alertWithMessageText_defaultButton_alternateButton_otherButton_informativeTextWithFormat_(title, None, None, None, msg)
            alert.runModal()
            NSApp.terminate_(None)
        
        self.willChangeValueForKey_("requiredTags")
        self.requiredTags = [{"tag":tag} for tag in osm2spatialite.defaultConfig["tags"]]
        self.didChangeValueForKey_("requiredTags")
        
        self.willChangeValueForKey_("userTags")
        userTags = defaults.arrayForKey_("userTags")
        
        if not userTags:
            self.userTags = []
        else:
            self.userTags = [{"tag":tag} for tag in userTags]
        
        self.didChangeValueForKey_("userTags")
        
        #self.addObserver_forKeyPath_options_context_(self, "userTags", NSKeyValueObservingOptionNew, None)
    
    def observeValueForKeyPath_ofObject_change_context_(self, keyPath, object, change, context):
        pass
    
    @objc.IBAction
    def selectOSMFile_(self, sender):
        panel = NSOpenPanel.alloc().init()
        panel.setTitle_("Select Input File")
        panel.setAllowsOtherFileTypes_(True)
        panel.setCanSelectHiddenExtension_(True)
        filetypes = ["osm"]
        if self.hasProtoBuf:
            filetypes.append("pbf")
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
        
        config = copy.deepcopy(osm2spatialite.defaultConfig)
        if "tags" in args:
            config["tags"] = args["tags"][:]
        
        self.performSelectorOnMainThread_withObject_waitUntilDone_("mainThreadUpdate:", "Hello from the thread", False)
        osm2spatialite.reportStatus = self.importReportStatus
        osm2spatialite.reportDetailedProgress = self.importReportDetails
        db = osm2spatialite.trydb(args["outfile"], True)
        if db:
            osm2spatialite.parseFile(args["infile"], db, config=config, verbose=True)
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
        
        tags = list()
        
        for tag in self.requiredTags:
            tags.append(tag["tag"])
        for tag in self.userTags:
            tags.append(tag["tag"])
        
        threadParams = {
            "infile":infile,
            "outfile":outfile,
            "tags":tags
            }
        
        NSThread.detachNewThreadSelector_toTarget_withObject_(self.importThread_,self,threadParams)
        self.importWindowCurrentStagePercent.setIndeterminate_(True)
        self.importWindowCurrentStagePercent.startAnimation_(self)
        
        self.importWindow.makeKeyAndOrderFront_(self)
        #FIXME: Validate input filenames
    
    @objc.IBAction
    def showTagsWindow_(self, sender):
        self.mainWindow.orderOut_(self)
        self.editTagsWindow.makeKeyAndOrderFront_(self)
    
    @objc.IBAction
    def addUserTag_(self, sender):
        self.userTagsArrayController.addObject_({"tag":""})
        self.userTagsTable.reloadData()
        newRowNum = self.userTagsArrayController.selectionIndex()
        self.userTagsTable.editColumn_row_withEvent_select_(0, newRowNum, None, True)
    
    @objc.IBAction
    def closeTagsWindow_(self, sender):
        self.requiredTagsArrayController.commitEditing()
        self.userTagsArrayController.commitEditing()
        self.editTagsWindow.orderOut_(self)
        self.mainWindow.makeKeyAndOrderFront_(self)
        
        
        newTags = list()
        required = [x["tag"] for x in self.requiredTags]
        for value in self.userTags:
            tag = value["tag"]
            if tag not in required and tag != "":
                newTags.append(value)
                
        
        defaults = NSUserDefaults.standardUserDefaults()
        defaults.setObject_forKey_([tag["tag"] for tag in newTags], "userTags")
        
        self.willChangeValueForKey_("userTags")
        self.userTags = newTags
        self.didChangeValueForKey_("userTags")