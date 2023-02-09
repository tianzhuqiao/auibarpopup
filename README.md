**AuiToolBarPopup**: show controls on wx.lib.agw.aui.AuiToolBar dropdown window.

<img src="./images/demo.png"></img>

## How to use
```python
class MyPanel(wx.Panel):
    def __init__(self, parent, *args, **kwargs):
        wx.Panel.__init__(self, parent, *args, **kwargs)
        self.tb = aui.AuiToolBar(self, -1, ...)
        ...
        # create the art and set it to the AuiToolBar
        self.toolbarart = AuiToolBarPopupArt(self)
        self.tb.SetArtProvider(self.toolbarart)
        ...
```
