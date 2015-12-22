import pywinauto
import warnings


class WindowsPosition():
    def __init__(self):
        try:
            pwa_app = pywinauto.application.Application()
            w_handle = pywinauto.findwindows.find_windows(
                title=u'stdin', class_name='MediaPlayerClassicW')[0]
            self.app = pwa_app.window_(handle=w_handle)
            self.y_pos = self.app.Rectangle().top
            self.x_pos = self.app.Rectangle().left
            self.width = self.app.Rectangle().width()
            self.height =self.app.Rectangle().height()
        except IndexError:
            warnings.warn('App not find')

    def move(self, monitor='monitor1', new_width=1920, new_height=1080):
        '''monitor to send the window to (def: monitor1)
                monitor1 -> up
                monitor2 -> down
            width of the windows (def: 1920)
            height of the windows (def: 1080)'''
        monitors_pos = {'monitor1': -1080, 'monitor2': 0}
        try:
            self.app.MoveWindow(x=0, y=monitors_pos[monitor], width=new_width, height=new_height)
        except AttributeError:
            warnings.warn('No windows to move')

    def toggle_visibility(app, action='minimize'):
        '''Minimizes or maximizes windows (def: minimize)
            app: a pywinauto window with a handle
            action: minimize or maximize'''
        try:
            if action.lower() == 'minimize':
                self.app.Minimize()
            elif action.lower() == 'maximize':
                self.app.Maximize()
        except AttributeError:
            raise Exception("A pywinauto window_ is necessary")