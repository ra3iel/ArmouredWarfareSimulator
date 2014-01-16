#!/usr/bin/env python
# coding=utf-8

import wx
import threading
import SocketServer
import sys
import ServerGui
import Server
import loginServer
import os
import sys
sys.path.append(os.getcwd())
try:
    import wmi
except ImportError:
    #Unix system
    try:
        import netifaces
    except ImportError:
        None
from Errors import *
import messages
import sqlite3
import pickle

class inProgress(ServerGui.FillerFrame):
    def __init__(self, parent):
        ServerGui.FillerFrame.__init__(self, parent)

    def stopEvent( self, event ):
        raise AHHHHHHHHHHH("NOOOOOOO")
        self.Show(False)



class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass
            
class serverForm(ServerGui.Mainframe):
    """Initialise the main GUI for server setup."""
    def __init__(self, parent):
        try:
            ServerGui.Mainframe.__init__(self,parent)
        except:
            print("GUI failed __init__")
        self.interfaceChoice.Clear()
        self.parent = parent
        self.opSys = self.getOperatingSystem()
        self.loginThread()
	self.toClose = False

    def loginThread(self):
        loginServer.main()

    def getOperatingSystem(self):
        try:
            self.testval = sys.winver
            #No exception thrown, we must be on windows
            for nic in wmi.WMI ().Win32_NetworkAdapterConfiguration (IPEnabled=1):
                self.interfaceChoice.Append(nic.caption[11:])
            return "Win"
        except AttributeError:
            #We're running on unix system
            for ifaceName in netifaces.interfaces():
                self.interfaceChoice.Append(ifaceName)
            return "Unix"
    def changeInterface(self,event):
        if self.opSys ==  "Unix":
            ints = netifaces.interfaces()
            selected_int = ints[self.interfaceChoice.GetCurrentSelection()]
            try:
                self.ipBox.Value = netifaces.ifaddresses(selected_int)[2][0]['addr']
            except Exception:
                self.ipBox.Value = "Not connected"
        elif self.opSys == "Win":
            ints = [nic for nic in wmi.WMI ().Win32_NetworkAdapterConfiguration (IPEnabled=1)]
            self.ipBox.Value = ints[self.interfaceChoice.GetCurrentSelection()].IPAddress[0]

    def startServer(self,event):
        self.statusLab.SetLabel("Game instance is running")
        self.startServerThread()
        try:
            f = open("Stats.dat", "r")
            ex = pickle.load(f)
            messages.Info(self.parent, "Game has finished")
            self.statusLab.SetLabel("No game instance running")
            try:
                self.processEndOfGame(ex)
            except Exception as ex:
                #No stats to process
                print "Error processing: " + str(ex)
        except IOError:
            # No file
            pass
        
    def stopServer(self,event):
        self.statusLab.SetLabel("No game instance running")
        try:
            del self.server
            print("Server shutdown")
        except Exception:
            print ("Server not running")

    def beginTheSatanHailing(self):
	print "Beginning the server..."
        while not self.toClose:
		#print self.toClose
                a = self.server.handle_request()
                #All glory to overlord satan
                #print str(a)
	#print "Eh closing server eh"
	
    
    def watchTheServerIntently(self):
	s = Server.TankServer
        while True:
            if s.connected == 0:
		#print "ALL HAVE DISCONNECTED. \nPlan to close server."
		self.toClose = True
		break
	#print "Exiting monitor thread"
        
    def startServerThread(self):
        HOST = self.ipBox.Value
        PORT = int(self.portBox.Value)
        ### Goddammit this is hard to get right ###
        try:
            self.Show(False)
            messages.ServerRun(self.parent)
            self.server = SocketServer.ThreadingTCPServer((HOST,PORT), Server.TankServer)
            self.endEvent = threading.Event()
	    self.server.timeout = 3
            Server.TankServer.Event = self.endEvent
            print ("Server running on "+str(HOST)+":"+str(PORT))
            self.watch = threading.Thread(target=self.watchTheServerIntently)
	    #print "Created thread"
	    self.watch.start()
	    #print "Started monitoring thread. Starting server."
	    self.beginTheSatanHailing()
            try:
                #messages.ServerRun(self.parent)
                print "Closing server"
                Server.TankServer.toClose = False
                #print "Set to close"
                self.Show(True)
                #print "Shown"
                #print "Server stopped"
            except Exception as ex:
                print "ER ER ER " + str(ex)
                messages.Info(self.parent, "SERVER CLOSING WITH MESSAGE: " + str(ex.message))
                self.stopServer(None)
	except Exception as ex:
            #This is literally the only error that appears here
            print ("Port is not free")
            print ("Technical information: "+str(ex))
	    import sys
	    sys.exit()

    def filler(self):
        app = wx.App(False)
        self.frame = inProgress(None)
        self.frame.Show(True)
        #print "Form init"
        app.MainLoop()


    def processEndOfGame(self, stats):
        conn = sqlite3.Connection("LoginDatabase")
        cur = conn.cursor()
        #print "Running update on data: " + str(stats)
        for player in stats:
            #print "Update info: " + str(player)
            username = player[-1]
            tankName = player[-2]
            xpGained = player[2]
            #print "Got stats needed"
            playerId = cur.execute("SELECT UserId FROM UserInfo WHERE Username = ?", [username]).fetchone()
            playerId = playerId[0]
            #print "Got playerId " + str(playerId)
            currentXp = int(cur.execute("SELECT "+tankName+" FROM UserProgress WHERE UserId  = ?", [playerId]).fetchone()[0])
            #print "Init sql queries done"
            currentXp += xpGained
            cur.execute("UPDATE UserProgress SET "+tankName+" = ? WHERE UserId = ?", [currentXp, playerId])
            #print "UPDATED ID "+str(playerId)+" TO XP "+str(currentXp)
        conn.commit()
        conn.close()
        os.remove("Stats.dat")


def main():
	app = wx.App(False)
	frame = serverForm(None)
	frame.Show(True)
	app.MainLoop()
