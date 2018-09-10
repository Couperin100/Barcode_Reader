#!/usr/bin/python

import wx


class MessageBox(wx.Panel):
    """This class is for the Message Box"""

    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent)
        self.parent = parent

        wx.StaticBox(self, 0, 'Messages', (5, 5), size=(280, 220))
        self.message_display = wx.TextCtrl(self, 0, "", (18, 30), size=(250, 170),
                                           style=wx.TE_MULTILINE | wx.TE_READONLY)
        self.message_display.SetValue("Please scan the Barcode....\n")

    def update_message(self, barcode):
        """Update"""
        self.message_display.write("Barcode number %s was scanned\n" % barcode)
        self.display = BarcodeBox(self)
        

class BarcodeBox(wx.Panel):
    """This class is for the barcode box"""

    def __init__(self, parent):
        
        wx.Panel.__init__(self, parent)
        self.parent = parent
        """List to carry the barcode"""
        self.callbacks = []

        wx.StaticBox(self, 0, 'Barcode', (5, 5), size=(280, 120))
        self.display = wx.TextCtrl(self, 0, '', (18, 30), size=(170, 22))
        self.display.SetFocus()

        evt = wx.CommandEvent(wx.wxEVT_COMMAND_TEXT_UPDATED)   
        evt.SetEventObject(self.display)
        evt.SetId(self.display.GetId())

        self.display.GetEventHandler().ProcessEvent(evt) 

        clear_button = wx.Button(self, 0, 'Clear', (200, 29))

        self.Bind(wx.EVT_BUTTON, self.clear_btn, clear_button)
        self.Bind(wx.EVT_TEXT, self.barcode_char, self.display)

    def get_barcode(self):
        """Getting the barcode."""
        return self.display.GetValue()

    def barcode_dialog(self):
        """Barcode dialog."""
        dial = wx.MessageDialog(None, 'Barcode is invalid.  Please re-scan...',
                                'Info', wx.OK | wx.ICON_EXCLAMATION)
        dial.ShowModal()

    def barcode_char(self):
        """Barcode conditions."""
        if len(self.get_barcode()) == 12:
            self.run_callbacks()
            self.display.SetFocus()
        if len(self.get_barcode()) > 12:
            self.barcode_dialog(self)

    def run_callbacks(self):
        """Run callbacks."""
        barcode = self.get_barcode()
        for callback in self.callbacks:
            callback(barcode)

    def clear_btn(self):
        """Clear the Barcode Box."""
        self.display.Clear()
        self.display.SetFocus()


class MainWindow(wx.Frame):

    def __init__(self,parent,id):

        wx.Frame.__init__(self,parent,id,'Barcode Reader')
        vert_panel = wx.BoxSizer(wx.VERTICAL)
        mainpanel = wx.BoxSizer(wx.HORIZONTAL)

        message_box = MessageBox(self)
        barcode_box = BarcodeBox(self)

        barcode_box.callbacks.append(message_box.update_message)
        
        mainpanel.Add(barcode_box, 0, wx.ALL|wx.EXPAND, border=10)
        mainpanel.Add(message_box, 0, wx.ALL|wx.EXPAND, border=10)
        
        self.SetBackgroundColour("White")
        self.SetAutoLayout(True)
        vert_panel.Add(mainpanel)
        self.SetSizer(vert_panel)

    def closewindow(self,event):
        self.Destroy()


if __name__ == '__main__':
    app = wx.PySimpleApp()
    frame = MainWindow(parent=None, id=-1)
    frame.SetPosition(wx.Point(0, 0))
    frame.SetSize(wx.Size(635, 300))
    frame.Show()
    app.MainLoop()

