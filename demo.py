import wx
import wx.lib.agw.aui as aui
import wx.py as py
from auibarpopup import *

ID_TOOL_START = wx.ID_HIGHEST + 1

class MyPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.toolbarart = AuiToolBarPopupArt(self)
        sizer = wx.BoxSizer(wx.VERTICAL)
        tb = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                            agwStyle=aui.AUI_TB_OVERFLOW|aui.AUI_TB_TEXT|
                            aui.AUI_TB_HORZ_TEXT|aui.AUI_TB_PLAIN_BACKGROUND)
        tb.SetToolBitmapSize(wx.Size(16, 16))
        tb_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        tb.AddSimpleTool(ID_TOOL_START+200, "Item 1", tb_bmp1)
        tb.AddCheckTool(ID_TOOL_START+201, "Toggle", tb_bmp1, wx.NullBitmap)
        tb.AddRadioTool(ID_TOOL_START+202, "Radio 0", tb_bmp1, wx.NullBitmap)
        tb.AddRadioTool(ID_TOOL_START+203, "Radio 1", tb_bmp1, wx.NullBitmap)
        tb.AddSeparator()
        tb.AddSimpleTool(ID_TOOL_START+204, "Item 5", tb_bmp1)
        tb.AddSimpleTool(ID_TOOL_START+205, "Item 6", tb_bmp1)
        tb.AddSimpleTool(ID_TOOL_START+206, "Item 7", tb_bmp1)
        tb.AddSimpleTool(ID_TOOL_START+207, "Item 8", tb_bmp1)
        tb.SetArtProvider(self.toolbarart)
        tb.Realize()
        sizer.Add(tb, 0, wx.EXPAND)
        ns = {}
        ns['wx'] = wx
        ns['app'] = wx.GetApp()
        ns['frame'] = parent
        shell = py.shell.Shell(self, -1, locals=ns)
        sizer.Add(shell, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Bind(wx.EVT_TOOL, self.OnTool)

    def OnTool(self, event):
        print('ID %d called in panel'%(event.GetId()))

class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'AuiToolBarPopup Demo', size=(300, 432))
        self._mgr = aui.AuiManager()

        # tell AuiManager to manage this frame
        self._mgr.SetManagedWindow(self)
        self.toolbarart = AuiToolBarPopupArt(self)

        self._mgr.AddPane(MyPanel(self), aui.AuiPaneInfo().Name("test1").
                          Caption("Pane Caption").CenterPane())

        tb = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                            agwStyle=aui.AUI_TB_OVERFLOW|aui.AUI_TB_TEXT|
                            aui.AUI_TB_HORZ_TEXT|aui.AUI_TB_PLAIN_BACKGROUND)
        tb.SetToolBitmapSize(wx.Size(16, 16))
        tb_bmp1 = wx.ArtProvider.GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, wx.Size(16, 16))
        tb.AddSimpleTool(ID_TOOL_START+0, "Item 1", tb_bmp1)
        tb.AddCheckTool(ID_TOOL_START+1, "Toggle", tb_bmp1, wx.NullBitmap)
        tb.AddSeparator()
        tb.AddRadioTool(ID_TOOL_START+2, "Radio 0", tb_bmp1, wx.NullBitmap)
        tb.AddRadioTool(ID_TOOL_START+3, "Radio 1", tb_bmp1, wx.NullBitmap)
        tb.AddSeparator()
        tb.AddSimpleTool(ID_TOOL_START+4, "Item 5", tb_bmp1)
        tb.AddSimpleTool(ID_TOOL_START+5, "Item 6", tb_bmp1)
        tb.AddSimpleTool(ID_TOOL_START+6, "Item 7", tb_bmp1)
        tb.AddSimpleTool(ID_TOOL_START+7, "Item 8", tb_bmp1)

        choice = wx.Choice(tb, -1, choices=["One choice", "Another choice"])
        tb.AddControl(choice)
        cmb = wx.ComboBox(tb, -1, choices=["Option 1", "Option 2", "Option 3"])
        tb.AddControl(cmb)
        spin = wx.SpinCtrl(tb, -1)
        tb.AddControl(spin)

        tb.SetToolDropDown(ID_TOOL_START+6, True)
        tb.Realize()
        tb.SetArtProvider(self.toolbarart)
        self._mgr.AddPane(tb, aui.AuiPaneInfo().Name("tb").Caption("tb").
                          ToolbarPane().Floatable(False).Top())

        tb2 = aui.AuiToolBar(self, -1, wx.DefaultPosition, wx.DefaultSize,
                             agwStyle=aui.AUI_TB_OVERFLOW|aui.AUI_TB_TEXT|
                             aui.AUI_TB_HORZ_TEXT|aui.AUI_TB_PLAIN_BACKGROUND)
        tb2.SetToolBitmapSize(wx.Size(16, 16))
        tb2.AddSimpleTool(ID_TOOL_START+100, "Item 1", tb_bmp1)
        tb2.AddSimpleTool(ID_TOOL_START+101, "Item 2", tb_bmp1)
        tb2.AddSimpleTool(ID_TOOL_START+102, "Item 3", tb_bmp1)
        tb2.AddSimpleTool(ID_TOOL_START+103, "Item 4", tb_bmp1)
        tb2.AddSeparator()
        statictext = wx.StaticText(tb2, -1, "StaticText")
        tb2.AddControl(statictext)
        slider = wx.Slider(tb2, 100, 25, 1, 100, size=(250, -1), style=wx.SL_HORIZONTAL)
        tb2.AddControl(slider)
        search = wx.SearchCtrl(tb2, size=(200, -1), style=wx.TE_PROCESS_ENTER)
        tb2.AddControl(search)
        tb2.Realize()
        tb2.SetArtProvider(self.toolbarart)
        self._mgr.AddPane(tb2, aui.AuiPaneInfo().Name("tb2").Caption("tb2").
                          ToolbarPane().Floatable(False).Top().Row(1))
        self._mgr.Update()
        self.Bind(wx.EVT_TOOL, self.OnTool)
        self.Bind(aui.EVT_AUITOOLBAR_TOOL_DROPDOWN, self.OnDropDownToolbarItem,
                  id=ID_TOOL_START+6)

    def OnTool(self, event):
        print('ID %d called'%(event.GetId()))

    def OnDropDownToolbarItem(self, event):
        if event.IsDropDownClicked():
            tb = event.GetEventObject()
            print("drop down, ID:%d"%(event.GetId()))
            tb.SetToolSticky(event.GetId(), True)

            # create the popup menu
            menuPopup = wx.Menu()
            bmp = wx.ArtProvider.GetBitmap(wx.ART_QUESTION, wx.ART_OTHER, wx.Size(16, 16))

            m1 = wx.MenuItem(menuPopup, 10001, "Drop Down Item 1")
            m1.SetBitmap(bmp)
            menuPopup.Append(m1)

            m2 = wx.MenuItem(menuPopup, 10002, "Drop Down Item 2")
            m2.SetBitmap(bmp)
            menuPopup.Append(m2)

            m3 = wx.MenuItem(menuPopup, 10003, "Drop Down Item 3")
            m3.SetBitmap(bmp)
            menuPopup.Append(m3)

            m4 = wx.MenuItem(menuPopup, 10004, "Drop Down Item 4")
            m4.SetBitmap(bmp)
            menuPopup.Append(m4)

            # line up our menu with the button
            rect = tb.GetToolRect(event.GetId())
            pt = tb.ClientToScreen(rect.GetBottomLeft())
            pt = self.ScreenToClient(pt)

            self.PopupMenu(menuPopup, pt)

            # make sure the button is "un-stuck"
            tb.SetToolSticky(event.GetId(), False)

class RunApp(wx.App):
    def __init__(self):
        wx.App.__init__(self, redirect=False)

    def OnInit(self):
        frame = MainFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        self.frame = frame
        return True

def main():
    app = RunApp()
    app.MainLoop()

if __name__ == '__main__':
    main()
