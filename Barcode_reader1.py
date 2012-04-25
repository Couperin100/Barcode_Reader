#!/usr/bin/python

import wx
import pdb

class Messagebox(wx.Panel):
    """This code is for the Message Box"""

    def __init__(self,parent):
        
        wx.Panel.__init__(self,parent)
        self.parent = parent

        messagebox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wx.StaticBox(self, 0, 'Messages',(5,5), size=(280,220))
        self.message_display = wx.TextCtrl(self,0,"",(18,30),size=(250,170),
                                           style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.message_display.SetValue("Please scan the Barcode....\n" )
        
        
    def Update_Message(self, barcode):
        self.message_display.write("Barcode number %s was scanned\n" % barcode)
        self.display = Barcodebox(self)
        

class Barcodebox(wx.Panel):
    """This code is for the barcode box"""

    def __init__(self,parent):
        
        wx.Panel.__init__(self,parent)
        self.parent = parent
        """List to carry the barcode"""
        self.callbacks = []
        
        messagebox_sizer = wx.BoxSizer(wx.HORIZONTAL)
        wx.StaticBox(self, 0, 'Barcode',(5,5), size=(280,120))
        self.display = wx.TextCtrl(self, 0,'',(18,30), size=(170,22))
        self.display.SetFocus()
        #self.display.SetMaxLength(12)

        evt = wx.CommandEvent(wx.wxEVT_COMMAND_TEXT_UPDATED)   
        evt.SetEventObject(self.display)
        evt.SetId(self.display.GetId())

        self.display.GetEventHandler().ProcessEvent(evt) 

        clear_button = wx.Button(self, 0,'Clear',(200,29))

        self.Bind(wx.EVT_BUTTON,self.clear_btn, clear_button)
        self.Bind(wx.EVT_TEXT,self.Barcode_char,self.display)

    def Get_Barcode(self):
        return self.display.GetValue()

    def Barcode_Dialog(self,event):
        dial = wx.MessageDialog(None, 'Barcode is invalid.  Please re-scan...', 'Info', wx.OK|wx.ICON_EXCLAMATION)
        dial.ShowModal()

    def Barcode_char(self,event):
        
        if len(self.Get_Barcode()) == 12:
            self.run_callbacks()
            self.display.SetFocus()
        if len(self.Get_Barcode()) > 12:
            self.Barcode_Dialog(self)
            
            
    def run_callbacks(self):
        barcode = self.Get_Barcode()
        for callback in self.callbacks:
            callback(barcode)
                                
        
    def clear_btn(self,event):
        """Clear the Barcode Box"""
        self.display.Clear()
        self.display.SetFocus()
        
class MainWindow(wx.Frame):

    def __init__(self,parent,id):

        wx.Frame.__init__(self,parent,id,'Barcode Reader')
        vert_panel = wx.BoxSizer(wx.VERTICAL)
        mainpanel = wx.BoxSizer(wx.HORIZONTAL)
        #main1 = wx.BoxSizer(wx.HORIZONTAL)
        
        message_box = Messagebox(self)
        barcode_box = Barcodebox(self)
        
        barcode_box.callbacks.append(message_box.Update_Message)
    
        #crap_box = Messagebox(self)
        #crap_box1 = Messagebox1(self)
        
        mainpanel.Add(barcode_box, 0, wx.ALL|wx.EXPAND, border=10)
        mainpanel.Add(message_box, 0, wx.ALL|wx.EXPAND, border=10)
        #main1.Add(crap_box, 0, wx.ALL|wx.EXPAND, border=10)
        #main1.Add(crap_box1, 0, wx.ALL|wx.EXPAND, border=10)
        
        self.SetBackgroundColour("White")
        self.SetAutoLayout(True)
        vert_panel.Add(mainpanel)
        #vert_panel.Add(main1)
        self.SetSizer(vert_panel)


    def closewindow(self,event):
        self.Destroy()
        
if __name__=='__main__':
    app=wx.PySimpleApp()
    frame = MainWindow(parent=None,id=-1)
    frame.SetPosition(wx.Point(0,0))
    frame.SetSize(wx.Size(635,300))
    frame.Show()
    app.MainLoop()

