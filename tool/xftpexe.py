"""
# -*- encoding: utf-8 -*-
# !/usr/bin/python3
@File:     xftpexe.py
@Author:   shenfan
@Time:     2021/3/8 20:44
"""
import wx
import wx.xrc

###########################################################################
## Class FileTransfer
###########################################################################

class FileTransfer ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"文件互传", pos = wx.DefaultPosition, size = wx.Size( 500,600 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
        self.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

        background = wx.BoxSizer( wx.VERTICAL )

        login = wx.StaticBoxSizer( wx.StaticBox( self, wx.ID_ANY, u"远程主机连接信息" ), wx.HORIZONTAL )

        login.SetMinSize( wx.Size( -1,50 ) )
        self.user = wx.StaticText( login.GetStaticBox(), wx.ID_ANY, u"用户", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.user.Wrap( -1 )
        login.Add( self.user, 0, wx.ALL, 5 )

        self.userinput = wx.TextCtrl( login.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        login.Add( self.userinput, 0, wx.ALL, 5 )

        self.password = wx.StaticText( login.GetStaticBox(), wx.ID_ANY, u"密码", wx.DefaultPosition, wx.DefaultSize, 0 )
        self.password.Wrap( -1 )
        login.Add( self.password, 0, wx.ALL, 5 )

        self.passwordinput = wx.TextCtrl( login.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        login.Add( self.passwordinput, 0, wx.ALL, 5 )


        background.Add( login, 0, wx.EXPAND, 5 )

        self.host = wx.StaticText( self, wx.ID_ANY, u"目标主机", wx.Point( 250,-1 ), wx.DefaultSize, 0 )
        self.host.Wrap( -1 )
        self.host.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        background.Add( self.host, 0, wx.ALL, 5 )

        self.hostinput = wx.TextCtrl( self, wx.ID_ANY, wx.EmptyString, wx.Point( 100,-1 ), wx.Size( 300,-1 ), 0 )
        background.Add( self.hostinput, 0, wx.ALL, 5 )

        self.remotedir = wx.StaticText( self, wx.ID_ANY, u"远程目录", wx.Point( 250,-1 ), wx.DefaultSize, 0 )
        self.remotedir.Wrap( -1 )
        self.remotedir.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        background.Add( self.remotedir, 0, wx.ALL, 5 )

        remote_dir_selectChoices = []
        self.remote_dir_select = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.Point( 100,-1 ), wx.Size( 300,-1 ), remote_dir_selectChoices, 0 )
        background.Add( self.remote_dir_select, 0, wx.ALL, 5 )

        self.localdir = wx.StaticText( self, wx.ID_ANY, u"本地目录", wx.Point( 250,-1 ), wx.DefaultSize, 0 )
        self.localdir.Wrap( -1 )
        self.localdir.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        background.Add( self.localdir, 0, wx.ALL, 5 )

        remote_dir_select1Choices = []
        self.remote_dir_select1 = wx.ComboBox( self, wx.ID_ANY, wx.EmptyString, wx.Point( 100,-1 ), wx.Size( 300,-1 ), remote_dir_select1Choices, 0 )
        background.Add( self.remote_dir_select1, 0, wx.ALL, 5 )

        self.download = wx.Button( self, wx.ID_ANY, u"下载", wx.Point( 250,-1 ), wx.DefaultSize, 0 )
        self.download.SetDefault()
        background.Add( self.download, 0, wx.ALL, 5 )

        outputChoices = []
        self.output = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,150 ), outputChoices, 0 )
        background.Add( self.output, 0, wx.ALL, 5 )


        self.SetSizer( background )
        self.Layout()
        self.m_menubar4 = wx.MenuBar( 0 )
        self.SetMenuBar( self.m_menubar4 )

        self.m_statusBar4 = self.CreateStatusBar( 1, 0, wx.ID_ANY )

        self.Centre( wx.BOTH )

        # Connect Events
        self.userinput.Bind(wx.EVT_TEXT,self.mian_input )
        self.passwordinput.Bind(wx.EVT_TEXT, self.mian_input )
        self.hostinput.Bind(wx.EVT_TEXT, self.mian_input )
        self.remote_dir_select.Bind( wx.EVT_COMBOBOX, self.mian_select )
        self.remote_dir_select1.Bind( wx.EVT_COMBOBOX, self.main_select )
        self.download.Bind( wx.EVT_BUTTON, self.main_run )
        self.output.Bind( wx.EVT_LISTBOX, self.mian_outinfo )

    def __del__( self ):
        pass

    # Virtual event handlers, overide them in your derived class
    def mian_input( self, event ):
        pass

    def mian_select( self, event ):
        pass

    def main_select( self, event ):
        pass

    def main_run( self, event ):
        pass

    def mian_outinfo( self, event ):
        pass


class MianWindow(FileTransfer):
    # 咱们给个初始化函数，将文本框初始填有‘主窗口测试’几个字
    # 不能直接覆盖原有__ini__方法，这样会导致窗体启动失败。咱们新建一个，然后再调用
    def init_main_window(self):
        self.mian_input.SetValue('主窗口测试')
    # 将点击按钮清空文本框的,功能写成函数

if __name__ == '__main__':
    app = wx.App()
    # None表示的是此窗口没有上级父窗体。如果有，就直接在父窗体代码调用的时候填入‘self’就好了。
    main_win = MianWindow(None)
    main_win.init_main_window()
    main_win.Show()
    app.MainLoop()





