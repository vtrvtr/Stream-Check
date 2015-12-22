import pywinauto


def init_wizard():
    try:
        pwa_app = pywinauto.application.Application()
        w_handle = pywinauto.findwindows.find_windows(
            title=u'stdin', class_name='MediaPlayerClassicW')[0]
        Wizard = pwa_app.window_(handle=w_handle)
        return Wizard
    except IndexError:
        raise Exception('App not find')


def get_position(app):
    pos = app.Rectangle()
    return pos.left, pos.top, pos.width(), pos.height()


def check_monitor(y_pos):
    '''Returns True if window is in the first (up) monitor'''
    return True if y_pos < -71 else False


def change_monitor(app, monitor='monitor1', width=1920, height=1080):
    '''monitor to send the window to (def: monitor1)
            monitor1 -> up
            monitor2 -> down
        width of the windows (def: 1920)
        height of the windows (def: 1080)'''
    monitors_pos = {'monitor1': -1080, 'monitor2': 0}
    app = init_wizard()
    app.MoveWindow(x=0, y=monitors_pos[monitor], width=1920, height=1080)


def toggle_visibility(app, action='minimize'):
    '''Minimizes or maximizes windows (def: minimize)
        app: a pywinauto window with a handle
        action: minimize or maximize'''
    try:
        if action == 'minimize':
            app.Minimize()
        elif action == 'maximize':
            app.Maximize()
    except AttributeError:
        raise Exception("A pywinauto window_ is necessary")


