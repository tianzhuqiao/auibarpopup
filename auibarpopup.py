import wx
import wx.lib.agw.aui as aui

class AuiToolBarPopup(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, style=wx.NO_BORDER|
                          wx.FRAME_TOOL_WINDOW|wx.FRAME_NO_TASKBAR|
                          wx.FRAME_FLOAT_ON_PARENT|wx.STAY_ON_TOP)
        self._toolbar = None
        self.tb = aui.AuiToolBar(self, -1, agwStyle=aui.AUI_TB_VERTICAL|
                                 aui.AUI_TB_TEXT|aui.AUI_TB_HORZ_TEXT)
        self.Bind(wx.EVT_ACTIVATE, self.OnActivate)

    def OnTool(self, event):
        item = self.tb.FindTool(event.GetId())
        if item.GetKind() in [aui.ITEM_CHECK, aui.ITEM_RADIO]:
            state = (item.state & aui.AUI_BUTTON_STATE_CHECKED and [True] or [False])[0]
            self._toolbar.ToggleTool(item.GetId(), state)
        self.Cancel()
        event.Skip()

    def OnActivate(self, event):
        if not event.GetActive():
            wnd = wx.FindWindowAtPointer()
            if wnd:
                wnd = wnd[0]
            while wnd:
                if wnd == self:
                    return
                wnd = wnd.GetParent()
            self.Cancel()
        event.Skip()

    def Cancel(self):
        realize = False
        for item in self.tb._items:
            if item.GetKind() == aui.ITEM_CONTROL:
                origin_item = self._toolbar.FindTool(item.window.GetId())
                if origin_item.sizer_item and not origin_item.sizer_item.IsShown():
                    item.window.Show(False)
                item.window.Reparent(self._toolbar)
                realize = True
        if realize:
            # add controls back to the original toolbar, so realize it;
            # however, the client size will set to be the min size (of all
            # items); call SetClientSize() does not work since it will trigger
            # OnSize, which call Realize() again and set the client size to min
            # size again... The following "workaround" seems working
            sz = self._toolbar.GetClientSize()
            self._toolbar.Realize()
            if self._toolbar.GetAuiManager():
                self._toolbar.GetAuiManager().Update()
            self._toolbar.SetClientSize(sz)
        # refresh the toolbar; otherwise, the status of the radio buttons may
        # not be correct.
        self._toolbar.Refresh()
        self.tb.ClearTools()
        wx.CallAfter(self.Hide)

    def UpdateItems(self, wnd, items):
        items_added = 0
        self._toolbar = wnd
        self.Unbind(wx.EVT_TOOL)
        self.tb.ClearTools()

        agw_flag_wnd = wnd.GetAGWWindowStyleFlag()
        agw_flag = aui.AUI_TB_VERTICAL|aui.AUI_TB_TEXT|aui.AUI_TB_HORZ_TEXT
        if agw_flag_wnd & aui.AUI_TB_PLAIN_BACKGROUND:
            agw_flag |= aui.AUI_TB_PLAIN_BACKGROUND
        self.tb.SetAGWWindowStyleFlag(agw_flag)

        for item in items:
            tool = None
            if item.GetKind() == aui.ITEM_LABEL:
                tool = self.tb.AddLabel(item.GetId(), item.GetLabel())
            elif item.GetKind() == aui.ITEM_SEPARATOR:
                if items_added > 0:
                    tool = self.tb.AddSeparator()
            elif item.GetKind() == aui.ITEM_CONTROL:
                item.window.Reparent(self.tb)
                if not item.window.IsShown():
                    item.window.Show(True)
                tool = self.tb.AddControl(item.window, item.GetLabel())
            elif item.GetKind() == aui.ITEM_CHECK:
                tool = self.tb.AddCheckTool(item.GetId(), item.GetLabel(),
                                            item.GetBitmap(), item.GetDisabledBitmap())
                if item.state & aui.AUI_BUTTON_STATE_CHECKED:
                    tool.state |= aui.AUI_BUTTON_STATE_CHECKED
            elif item.GetKind() == aui.ITEM_RADIO:
                tool = self.tb.AddRadioTool(item.GetId(), item.GetLabel(),
                                            item.GetBitmap(), item.GetDisabledBitmap())
                if item.state & aui.AUI_BUTTON_STATE_CHECKED:
                    tool.state |= aui.AUI_BUTTON_STATE_CHECKED
            elif item.GetKind() == aui.ITEM_NORMAL:
                tool = self.tb.AddSimpleTool(item.GetId(), item.GetLabel(),
                                             item.GetBitmap())
                self.tb.SetToolDropDown(tool.GetId(), wnd.GetToolDropDown(tool.GetId()))
            if tool:
                tool.SetAlignment(wx.EXPAND)
                items_added += 1

        self.tb.Realize()
        self.SetClientSize(self.tb.GetMinSize())
        self.Bind(wx.EVT_TOOL, self.OnTool)

class AuiToolBarPopupArt(aui.AuiDefaultToolBarArt):
    def __init__(self, frame):
        aui.AuiDefaultToolBarArt.__init__(self)
        self.popup = AuiToolBarPopup(frame)

    def ShowDropDown(self, wnd, items):
        """
        Shows the drop down window menu for overflow items.

        :param `wnd`: an instance of :class:`wx.Window`;
        :param list `items`: a list of the overflow toolbar items.
        """
        # find out where to put the popup menu of window items
        pt = wx.GetMousePosition()
        pt = wnd.ScreenToClient(pt)

        # find out the screen coordinate at the bottom of the tab ctrl
        cli_rect = wnd.GetClientRect()
        pt.y = cli_rect.y + cli_rect.height
        self.popup.Position = wnd.ClientToScreen(pt)
        self.popup.UpdateItems(wnd, items)
        self.popup.Show()
        self.popup.Raise()
        return -1
