#!d:/virtualenv/py-deezer/Scripts/python.exe

from __future__ import print_function

from pydeezer import Deezer
from pydeezer.constants import track_formats
import os
import sys
import re
from pause import pause
if sys.platform == 'win32':
    import win32api, win32con, win32gui, win32console
    from dcmd import dcmd
    from ctypes import windll, byref, wintypes
os.environ.update({'PYTHONIOENCODING':'UTF-8'})
from configset import configset
import argparse
import clipboard
import bitmath
import traceback
from make_colors import make_colors
from pydebugger.debug import debug
from pywget import wget
from datetime import datetime
from xnotify.notify import notify
import shutil
import progressbar
import time
try:
    from pause import pause
except:
    pass    
if sys.version_info.major == 2:
    pass
else:
    raw_input = input
debug("cls")
# import multiprocessing

cookies = {}
class LoadHandler(object):
    def OnLoadingStateChange(self, browser, is_loading, **_):
        if is_loading:
            print("Page loading complete - start visiting cookies")
            manager = cef.CookieManager.GetGlobalManager()
            # Must keep a strong reference to the CookieVisitor object
            # while cookies are being visited.
            self.cookie_visitor = CookieVisitor()

            # Visit all cookies
            result = manager.VisitAllCookies(self.cookie_visitor)

            if not result:
                print("Error: could not access cookies\n")

            # To visit cookies only for a given url uncomment the
            # code below.
            """
            url = "http://www.html-kit.com/tools/cookietester/"
            http_only_cookies = False
            result = manager.VisitUrlCookies(url, http_only_cookies,
                                             self.cookie_visitor)
            if not result:
                print("Error: could not access cookies")
            """

class CookieVisitor(object):
    def Visit(self, cookie, count, total, delete_cookie_out):
        """This callback is called on the IO thread."""
        print("Cookie {count}/{total}: '{name}', '{value}'".format(count=count+1, total=total, name=cookie.GetName(), value=cookie.GetValue()))
        # Set a cookie named "delete_me" and it will be deleted.
        # You have to refresh page to see whether it succeeded.
        cookies.update({cookie.GetName():cookie.GetValue().split("\n")[0]})

        #if cookie.GetName() == '_pk_cvar.1.5294':
        # if cookie.GetName() == 'remember'
        if cookie.GetName() == 'arl':
            print("start Shutdown ...")
            cef.Shutdown()
            print("Shutdown Process ...")
            #if cookie.GetValue():
            #cef.Shutdown()

        #if cookie.GetName() == "delete_me":
            # 'delete_cookie_out' arg is a list passed by reference.
            # Set its '0' index to True to delete the cookie.
        #	delete_cookie_out[0] = True
        #	print("Deleted cookie: {name}".format(name=cookie.GetName()))

        # Return True to continue visiting more cookies
        cef.Shutdown()
        return True


class Deez(object):
    # thread = None
    
    error = False
    prefix = '{variables.task} >> {variables.subtask}'
    variables =  {'task': '--', 'subtask': '--'}
    max_value = 60
    bar = progressbar.ProgressBar(max_value = max_value, prefix = prefix, variables = variables)
    nbar = 0
    task = make_colors("Connection Error", 'lw', 'lr', ['blink'])
    subtask = make_colors("Re-Connecting", 'b', 'lg', ['blink']) + " "
    ARL = "4659ecf4e9e46931714cbf470afd5242fdf97505c7f0e89aecc9442caa056064c9a538693acb37292467d76a2039e4e6b38e0d118fe018625d5252f38db315c46bf17d45cd1442acaf15006d9ef9d42aaf385a71c937b6fafa342bb2bb0dfa6e"
    deezer = None
    if ARL:
        debug(ARL = ARL)
        while 1:

            try:
                deezer = Deezer(arl = ARL)
                task = make_colors("Connection", 'lw', 'lr', ['blink'])
                subtask = make_colors("Success", 'b', 'lg', ['blink']) + " "
                bar.max_value = 1
                bar.update(nbar, task = task, subtask = subtask)
                bar.finish()
                break
            except:
                tp, vl, tr = sys.exc_info()
                if vl.__class__.__name__ == "ConnectionError":
                    if nbar == max_value:
                        nbar = 1
                    bar.update(nbar, task = task, subtask = subtask)
                else:
                    traceback.format_exc()
                    bar.finish()
                    error = True
                    break
                nbar+=1
                time.sleep(1)
            if error:
                sys.exit(make_colors("ERROR CONNECTION AFTER {} Tries !".format(str(max_value)), 'lw', 'lr'))

    config = configset()
    CD = None
    LOGO = os.path.join(os.path.dirname(__file__), 'logo.png')
    if not ARL:
        ALR = config.get_config('AUTH', 'arl', "4659ecf4e9e46931714cbf470afd5242fdf97505c7f0e89aecc9442caa056064c9a538693acb37292467d76a2039e4e6b38e0d118fe018625d5252f38db315c46bf17d45cd1442acaf15006d9ef9d42aaf385a71c937b6fafa342bb2bb0dfa6e")

    def __init__(self, arl = None):
        super(Deez, self)
        self.arl = arl
        if self.arl:
            self.deezer = Deezer(arl = self.arl)

    def browser_login(self):
        from cefpython3 import cefpython as cef
        br_WindowInfo = cef.WindowInfo()
        if sys.platform == 'win32':
            parent = self.create_window()
            br_WindowInfo.SetAsChild(parent, [0, 0, 500, 500])
        else:
            br_WindowInfo.SetAsChild(0, [0, 0, 500, 500])
    
        settings = {
                "debug": True,
                "log_severity": cef.LOGSEVERITY_INFO,
                "log_file": os.path.join(os.path.dirname(__file__), "deez_debug.log"),
            }
        cef.Initialize(settings = settings)
        browser = cef.CreateBrowserSync(br_WindowInfo, url="https://www.deezer.com/", window_title="Deezer Login")
        browser.SetClientHandler(LoadHandler())
        cef.MessageLoop()
        print("Shutdown Complete")
        # del browser
        print("cookies =", cookies)
        #pause()
        cef.Shutdown()    

    def create_window(self):
        def OnDestroy(hwnd, message, wparam, lparam):
            win32gui.PostQuitMessage(0)
            return True
    
        win32gui.InitCommonControls()
        hinst = win32api.GetModuleHandle(None)
        #hinst = win32gui.dllhandle
        className = 'deez_login'
        message_map = {
                win32con.WM_DESTROY: OnDestroy,
            }
        wc = win32gui.WNDCLASS()
        wc.style = win32con.WS_OVERLAPPED | win32con.CS_HREDRAW | win32con.CS_VREDRAW
        wc.lpfnWndProc = message_map
        wc.lpszClassName = className
        try:
            win32gui.RegisterClass(wc)
        except:
            pass
        style = win32con.WS_MAXIMIZEBOX | win32con.WS_MAXIMIZEBOX | win32con.WS_BORDER
        hwnd = win32gui.CreateWindow(
                className,
                'Seedr Browser',
                style,
                        win32con.CW_USEDEFAULT,
                            win32con.CW_USEDEFAULT,
                            525,
                            530,
                            0,
                            0,
                            hinst,
                            None
            )
        win32gui.UpdateWindow(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST,0,0,530,530,0)
        win32gui.MoveWindow(hwnd, win32api.GetSystemMetrics(0)/3, win32api.GetSystemMetrics(1)/9, 530, 530, True)
        win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
        return hwnd

    @classmethod
    def find(cls, query, ftype="artist"):
        '''
        	ftype: "artist | album | track | playlist" (str)
        '''
        if not cls.deezer:
            print(make_colors("Invalid ARL !", 'lw', 'lr'))
            return False

        result = False
        if ftype == 'artist':
            debug(ftype = ftype)
            while 1:
                try:
                    result = cls.deezer.search_artists(query)
                    break
                except:
                    pass
        elif ftype == 'album':
            result = cls.deezer.search_albums(query)
        elif ftype == 'track':
            result = cls.deezer.search_tracks(query)
        elif ftype == 'playlist':
            result = cls.deezer.search_playlists(query)
        else:
            print(make_colors("Invalid ftype !", 'lw' ,'lr'))
            return False
        debug(result = result)
        return result
    
    @classmethod
    def format_number(cls, number, length = 10):
        number = str(number).strip()
        zeros = len(str(length)) - len(number)
        r = ("0" * zeros) + str(number)
        if len(r) == 1:
            return "0" + r
        return r

    @classmethod
    def re_numbering_files(cls, download_path, fformat = 'mp3', album_artist = None):
        if fformat:
            if "." == fformat[0]:
                fformat = fformat[1:]
        from mutagen.easyid3 import EasyID3
        def check_length(length):
            if isinstance(length, int):
                length = str(length).strip()
            if len(str(length)) == 1:
                length = "0" + str(length)
            return length

        def change_cd_track(cd, length = None):
            if isinstance(cd, int):
                cd = str(cd).strip()
            if "/" in cd:
                fr, to = cd.split("/")
                if len(str(fr)) == 1:
                    fr = "0" + str(fr)
                if len(str(to)) == 1:
                    to = "0" + str(to)
                if length and str(length).isdigit():
                    cd = fr + "/" + check_length(length)
                else:
                    cd = fr + "/" + to
            else:
                if len(str(cd)) == 1:
                    cd = "0" + str(cd)
                if length and str(length).isdigit():
                    cd = cd + "/" + check_length(length)
                else:
                    cd = cd + "/" + cd
            return cd

        def check_track_number(download_path, search_tracks_number):
            search_tracks_number = re.findall("\d+\.", search_tracks_number)
            list_track_files = os.listdir(download_path)
            track_number_found = []
            track_number_found_files = []
            for f in list_track_files:
                f = re.sub("\n|\r|\t", f)
                num = re.findall("\d+\.", f)
                if num and cls.format_number(search_tracks_number) == num[0]:
                    track_number_found.append(num[0])
                    track_number_found_files.append(f)
            return track_number_found, track_number_found_files

        list_track_files = os.listdir(download_path)
        nt = 1
        for f in list_track_files:
            f = re.sub("\n|\r|\t", "", f)
            if f.endswith("." + fformat):
                tags = EasyID3(os.path.join(download_path, f))
                tags['tracknumber'] = change_cd_track(str(nt), len(list_track_files))
                tags['discnumber'] = change_cd_track("1")
                if album_artist:
                    tags['albumartist'] = album_artist
                name = re.sub("\d+\. ", "", f, 1)
                tags.save()
                os.rename(os.path.join(download_path, f), os.path.join(download_path, cls.format_number(nt) + ". " + name))
                if os.path.isfile(os.path.splitext(os.path.join(download_path, f))[0] + ".jpg"):
                    os.rename(os.path.splitext(os.path.join(download_path, f))[0] + ".jpg", os.path.splitext(os.path.join(download_path, cls.format_number(nt) + ". " + name))[0] + ".jpg")
                if os.path.isfile(os.path.splitext(os.path.join(download_path, f))[0] + ".png"):
                    os.rename(os.path.splitext(os.path.join(download_path, f))[0] + ".png", os.path.splitext(os.path.join(download_path, cls.format_number(nt) + ". " + name))[0] + ".png")
                nt += 1

    @classmethod
    def download(cls, tracks, numbers = None, fformat = 'mp3', download_path = None, overwrite = False, disco = None, single_only = False, dont_overwrite = False, all_singles_on_one_folder = False):
        # os.environ.update({'DEBUG':'1'})
        debug(single_only = single_only)
        debug(numbers = numbers)
        debug(disco = disco)
        error = False
        download_path0 = download_path
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        print(make_colors("SAVE TO", 'lw', 'bl') + ": " + make_colors(download_path, 'lw', 'm'))

        debug(disco_type = disco.get('TYPE'))
        if disco and single_only:
            if not int(disco.get('TYPE')) == 0:
                return False
            while 1:
                try:
                    tracks = cls.deezer.get_album_tracks(disco['ALB_ID'])
                    break
                except:
                    pass
        elif single_only and not disco:
            return False
        debug(len_tracks = len(tracks))
        if not numbers:
            numbers = list(range(len(tracks) + 1))[1:]
            debug(numbers = numbers)
        debug(numbers = numbers)
        album_id = disco['ALB_ID']
        debug(album_id = album_id)
        for i in numbers:
            debug(i = i)
            try:
                int(i)
            except:
                return False
            track_id = tracks[int(i) - 1].get('SNG_ID')
            debug(track_id = track_id)
            
            while 1:
                try:
                    track_detail = cls.deezer.get_track(track_id)
                    album_detail = cls.deezer.get_album(album_id)
                    # debug(track_detail = track_detail)
                    break
                except:
                    pass
            # debug(track_detail = track_detail)
            track_info = track_detail["info"]
            debug(track_info = track_info)
            tags_separated_by_comma = track_detail["tags"]
            debug(tags_separated_by_comma = tags_separated_by_comma)
            #url_download = cls.deezer.get_track_download_url(track, quality=track_formats.MP3_320)
            #debug(url_download = url_download[0])
            debug(tags_separated_by_comma_title = tags_separated_by_comma['title'])
            discnumber = tags_separated_by_comma.get('discnumber')
            if not cls.CD == discnumber:
                download_path = download_path0
                if int(discnumber) > 1:
                    if not os.path.isdir(os.path.join(download_path, 'CD01')) and not cls.CD:
                        print(make_colors("create directory:", 'lw', 'lr') + " " + make_colors(os.path.join(download_path, 'CD01'), 'lw', 'bl'))
                        os.makedirs(os.path.join(download_path, 'CD01'))
                        list_files_mp3 = list(filter(lambda k: k.endswith("." + fformat), os.listdir(download_path)))
                        list_files_lrc = list(filter(lambda k: k.endswith(".lrc"), os.listdir(download_path)))
                        for fl in list_files_mp3:
                            if os.path.isfile(os.path.join(os.path.join(download_path, 'CD01'), fl)):
                                os.remove(os.path.join(os.path.join(download_path, 'CD01'), fl))
                            shutil.move(os.path.join(download_path, fl), os.path.join(download_path, 'CD01'))
                        for fl in list_files_lrc:
                            if os.path.isfile(os.path.join(os.path.join(download_path, 'CD01'), fl)):
                                os.remove(os.path.join(os.path.join(download_path, 'CD01'), fl))
                            shutil.move(os.path.join(download_path, fl), os.path.join(download_path, 'CD01'))
                    if not os.path.isdir(os.path.join(download_path, 'CD0' + str(discnumber))):
                        print(make_colors("create directory:", 'lw', 'lr') + " " + make_colors(os.path.join(download_path, 'CD0' + str(discnumber)), 'lw', 'bl'))
                        os.makedirs(os.path.join(download_path, 'CD0' + str(discnumber)))
                    download_path = os.path.join(download_path, 'CD0' + str(discnumber))
                    cls.CD = discnumber

                
            name = cls.format_number(tracks[int(i) - 1].get('TRACK_NUMBER'), len(tracks)) + ". " + tags_separated_by_comma['title']# + ".mp3"
            FILE_3 = track_detail.get('info').get('DATA')['SNG_TITLE']
            # track_detail.get('info').get('DATA').update({'SNG_TITLE': tags_separated_by_comma['title']})
            debug(name = name)
            debug(track_detail = track_detail.get('info').get('DATA').keys())
            debug(FILESIZE_AAC_64 = track_detail.get('info').get('DATA')['FILESIZE_AAC_64'])
            debug(FILESIZE_MP3_64 = track_detail.get('info').get('DATA')['FILESIZE_MP3_64'])
            debug(FILESIZE_MP3_128 = track_detail.get('info').get('DATA')['FILESIZE_MP3_128'])
            debug(FILESIZE_MP3_256 = track_detail.get('info').get('DATA')['FILESIZE_MP3_256'])
            debug(FILESIZE_MP3_320 = track_detail.get('info').get('DATA')['FILESIZE_MP3_320'])
            debug(FILESIZE_MP4_RA1 = track_detail.get('info').get('DATA')['FILESIZE_MP4_RA1'])
            debug(FILESIZE_MP4_RA2 = track_detail.get('info').get('DATA')['FILESIZE_MP4_RA2'])
            debug(FILESIZE_MP4_RA3 = track_detail.get('info').get('DATA')['FILESIZE_MP4_RA3'])
            debug(FILESIZE_FLAC = track_detail.get('info').get('DATA')['FILESIZE_FLAC'])
            debug(FILESIZE = track_detail.get('info').get('DATA')['FILESIZE'])
            #name = os.path.join(download_path, name)
            #wget.download(url_download[0], out=name)
            
            if fformat == 'mp3':
                while 1:
                    try:
                        debug(name = name)
                        debug(FILE_1 = os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3"))
                        debug(FILE_2 =os.path.join(download_path, name + ".mp3"))
                        debug(FILE_3 = FILE_3)
                        debug(CHECK_FILE_1 = os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3")))    
                        debug(CHECK_FILE_2 = os.path.isfile(os.path.join(download_path, name + ".mp3")))
                        # pause()
                        if os.path.isfile(os.path.join(download_path, name + ".mp3")) and dont_overwrite:
                            pass
                        elif os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3")) and dont_overwrite:
                            pass
                        elif os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3")) and not overwrite:
                            q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                            if q == 'y' or q == 'Y':
                                if all_singles_on_one_folder:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                                track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                            elif q == 'n' or q == 'N':
                                error = "pass"
                                break
                            elif q == 'x' or q == 'q':
                                error = "exit"
                                break
                            else:
                                break

                        elif os.path.isfile(os.path.join(download_path, name + ".mp3")) and not overwrite:
                            q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                            if q == 'y' or q == 'Y':
                                if all_singles_on_one_folder:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                                track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                            elif q == 'n' or q == 'N':
                                error = "pass"
                                break
                            elif q == 'x' or q == 'q':
                                error = "exit"
                                break
                            else:
                                break
                        
                        elif os.path.isfile(os.path.join(download_path, name + ".mp3")) and overwrite:
                            if all_singles_on_one_folder:
                                cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                            track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                        else:
                            debug("downloading ...")
                            if all_singles_on_one_folder:
                                cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                            track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)

                        debug(NAME_1 = os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat))
                        debug(NAME_2 = os.path.join(download_path, name + "."+ fformat))
                        debug(NAME_3 = cls.format_number(tracks[int(i) - 1].get('TRACK_NUMBER'), len(tracks)) + ". " + tracks[int(i) - 1].get('SNG_TITLE') + ".mp3")

                        try:
                            if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat)):
                                os.rename(os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat), os.path.join(download_path, name + "."+ fformat))
                                print(make_colors("RENAME:", 'lw', 'lr') + " " + make_colors(tags_separated_by_comma['title'] + "." + fformat, 'lw', 'bl') + ' --> ' + make_colors(name + "."+ fformat, 'b', 'lg'))
                        except:
                            print("NAME 1:", os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat))
                            print("NAME 2:", os.path.join(download_path, name + "."+ fformat))
                            print("NAME 3:", cls.format_number(tracks[int(i) - 1].get('TRACK_NUMBER'), len(tracks)) + ". " + tracks[int(i) - 1].get('SNG_TITLE') + ".mp3")
                            # traceback.format_exc()
                        if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + "." + 'lrc')):
                            os.rename(os.path.join(download_path, tags_separated_by_comma['title'] + "." + 'lrc'), os.path.join(download_path, name + "."+ 'lrc'))
                            print(make_colors("RENAME:", 'lw', 'lr') + " " + make_colors(tags_separated_by_comma['title'] + "." + 'lrc', 'lw', 'bl') + ' --> ' + make_colors(name + "."+ 'lrc', 'b', 'lg'))
                        break
                    except:
                        pass
            elif fformat == 'flac':
                while 1:
                    try:
                        if os.path.isfile(os.path.join(download_path, name + ".flac")) and dont_overwrite:
                            return True
                        elif os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".flac")) and dont_overwrite:
                            return True
                        elif os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".flac")) and not overwrite:
                            q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                            if q == 'y' or q == 'Y':
                                if all_singles_on_one_folder:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                                track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                            elif q == 'n' or q == 'N':
                                error = "pass"
                                break
                            elif q == 'x' or q == 'q':
                                error = "exit"
                                break
                            else:
                                break
                        elif os.path.isfile(os.path.join(download_path, name + ".flac")) and not overwrite:
                            q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                            if q == 'y' or q == 'Y':
                                if all_singles_on_one_folder:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                                track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                            elif q == 'n' or q == 'N':
                                error = "pass"
                                break
                            elif q == 'x' or q == 'q':
                                error = "exit"
                                break
                            else:
                                break
                        
                        elif os.path.isfile(os.path.join(download_path, name + ".flac")) and overwrite:
                            if all_singles_on_one_folder:
                                cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                            track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                        else:
                            if all_singles_on_one_folder:
                                cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id, album_detail = album_detail)
                            track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                        try:
                            if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat)):
                                os.rename(os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat), os.path.join(download_path, name + "."+ fformat))
                                print(make_colors("RENAME:", 'lw', 'lr') + " " + make_colors(tags_separated_by_comma['title'] + "." + fformat, 'lw', 'bl') + ' --> ' + make_colors(name + "."+ fformat, 'b', 'lg'))
                        except:
                            print("NAME 1:", os.path.join(download_path, tags_separated_by_comma['title'] + "." + fformat))
                            print("NAME 2:", os.path.join(download_path, name + "."+ fformat))
                            print("NAME 3:", cls.format_number(tracks[int(i) - 1].get('TRACK_NUMBER'), len(tracks)) + ". " + tracks[int(i) - 1].get('SNG_TITLE') + ".mp3")
                            traceback.format_exc()
                        if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + "." + 'lrc')):
                            os.rename(os.path.join(download_path, tags_separated_by_comma['title'] + "." + 'lrc'), os.path.join(download_path, name + "."+ 'lrc'))
                            print(make_colors("RENAME:", 'lw', 'lr') + " " + make_colors(tags_separated_by_comma['title'] + "." + 'lrc', 'lw', 'bl') + ' --> ' + make_colors(name + "."+ 'lrc', 'b', 'lg'))
                        break
                    except:
                        pass
        if error == "pass":
            return error
        elif error == "exit":
            sys.exit()
        return True
    
    @classmethod
    def set_config(cls, q):
        q_return = q
        DOWNLOAD_ORIGINAL_ALBUM_ONLY = False
        INTO_ARTIST_FOLDER = False
        INTO_SINGLE_FOLDER = False
        DOWNLOAD_SINGLE_ONLY = False
        DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = True
        album_numbers = None
        if q[-1] == 'o':
            if q[-2:] == 'so':
                DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = True
                DOWNLOAD_SINGLE_ONLY = True
                INTO_SINGLE_FOLDER = True
                if q[:-2]:
                    album_numbers, _ = cls.split_number(q[:-2])
                    q_return = q[:-2]
            elif q[-2:] == 'So':
                DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = True
                DOWNLOAD_SINGLE_ONLY = True
                INTO_ARTIST_FOLDER = True
                if q[:-2]:
                    album_numbers, _ = cls.split_number(q[:-2])
                    q_return = q[:-2]
            else:
                DOWNLOAD_ORIGINAL_ALBUM_ONLY = True
                if q[:-1]:
                    album_numbers, _ = cls.split_number(q[:-1])
                    q_return = q[:-1]
        elif q[-1] == 's': #download all single track in one folder "SINGLE"
            DOWNLOAD_SINGLE_ONLY = True
            INTO_SINGLE_FOLDER = True
            if q[:-1]:
                album_numbers, _ = cls.split_number(q[:-1])
                q_return = q[:-1]
        elif q[-1] == 'S': #download all single track in one folder artist
            DOWNLOAD_SINGLE_ONLY = True
            INTO_ARTIST_FOLDER = True
            if q[:-1]:
                album_numbers, _ = cls.split_number(q[:-1])
                q_return = q[:-1]
        else:
            album_numbers, _ = cls.split_number(q)

        debug(DOWNLOAD_ORIGINAL_ALBUM_ONLY = DOWNLOAD_ORIGINAL_ALBUM_ONLY)
        debug(INTO_SINGLE_FOLDER = INTO_SINGLE_FOLDER)
        debug(INTO_ARTIST_FOLDER = INTO_ARTIST_FOLDER)
        debug(DOWNLOAD_SINGLE_ONLY = DOWNLOAD_SINGLE_ONLY)
        debug(DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY)
        debug(q_return = q_return)
        debug(album_numbers = album_numbers)
        return DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY, q_return, album_numbers

    @classmethod
    def set_config_artist(cls, q):
        just_artist = False
        just_artist_disco = False
        just_origin = False
        just_singles = False
        just_single_disco = False
        just_others = False
        just_other_disco = False

        download_album_artist = False #o
        download_album_artist_with_appereance = False #a
        download_album_artist_disco = False #A
        download_singles = False
        download_single_disco = False
        download_others = False
        download_other_disco = False
        download_into_artist_folder = False
        
        q_return = q
        
        if q[-1] == 'o' and not q[-2:] == 'do':
            just_origin = True
            if q[:-1].isdigit():
                q_return = q[:-1]
        elif (q[-1] == 'a' or q[-2:] == 'aa') and not q[-2:] == 'da':
            just_artist = True
            if q[-2:] == 'aa':
                if q[:-2].isdigit():
                    q_return = q[:-1]    
            else:
                if q[:-1].isdigit():
                    q_return = q[:-1]
        elif q[-1] == 'A' and not q[-2:] == 'dA':
            just_artist_disco = True
            if q[:-1].isdigit():
                q_return = q[:-1]
        elif q[-1] == 's' and not q[-2:] == 'ds' and not q[-3:] == 'dss':
            just_singles = True
            if q[:-1].isdigit():
                q_return = q[:-1]
        elif q[-1] == 'S' and not q[-2:] == 'dS' and not q[-3:] == 'dsS':
            just_single_disco = True
            if q[:-1].isdigit():
                q_return = q[:-1]
        elif q[-1] == 'v' and not q[-2:] == 'dv':
            just_others = True
            if q[:-1].isdigit():
                q_return = q[:-1]
        elif q[-1] == 'V' and not q[-2:] == 'dV':
            just_other_disco = True
            if q[:-1].isdigit():
                q_return = q[:-1]
        elif q[-2:] == 'do':
            download_album_artist = True
            if q[:-2].isdigit():
                q_return = q[:-2]
        elif q[-2:] == 'da':
            download_album_artist_with_appereance = True
            if q[:-2].isdigit():
                q_return = q[:-2]
        elif q[-2:] == 'dA':
            download_album_artist_disco = True
            if q[:-2].isdigit():
                q_return = q[:-2]
        elif q[-2:] == 'ds':
            download_singles = True
            debug(download_singles = download_singles)
            if q[:-2].isdigit():
                q_return = q[:-2]
            debug(q_return = q_return)
        elif q[-3:] == 'dss':
            download_singles = True
            download_into_artist_folder = True
            if q[:-3].isdigit():
                q_return = q[:-3]
            debug(q_return = q_return)
        elif q[-2:] == 'dS':
            download_single_disco = True
            if q[:-2].isdigit():
                q_return = q[:-2]
        elif q[-3:] == 'dsS':
            download_single_disco = True
            download_into_artist_folder = True
            if q[:-3].isdigit():
                q_return = q[:-3]
        elif q[-2:] == 'dv':
            download_others = True
            if q[:-2].isdigit():
                q_return = q[:-2]
        elif q[-2:] == 'dV':
            download_other_disco = True
            if q[:-2].isdigit():
                q_return = q[:-2]

        return just_artist, just_artist_disco, just_origin, just_singles, just_single_disco, just_others, just_other_disco, download_album_artist, download_album_artist_with_appereance, download_album_artist_disco, download_singles, download_single_disco, download_others, download_other_disco, download_into_artist_folder, q_return
        

    # @classmethod
    # def clean_config(cls):
    #     ALL_AS_ORGARTIST = False
    #     ALL_SINGLES_AS_ORGARTIST = False
    #     DOWNLOAD_SINGLE_ONLY = False
    #     DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST = False
    #     return ALL_AS_ORGARTIST, ALL_SINGLES_AS_ORGARTIST, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST

    # set_config.clean = clean_config

    @classmethod
    def split_number(cls, x):
        q = None
        track_number = None

        debug(x = x)
        if "-" in x:
            fr, to = x.split("-")
            fr = fr.strip()
            to = to.strip()

            if fr[-1] =='s' and not fr[:-1] == 'sS':
                fr = fr[:-1]
            elif fr[-2:] =='sS' or fr[-2:] =='aa':
                fr = fr[:-2]
            elif fr[-1] =='a' or fr[-1] =='A' or fr[-1] =='v' or fr[-1] =='V' or fr[-1] =='o':
                fr = fr[:-1]

            if to[-1] =='s' and not to[:-1] == 'sS':
                to = to[:-1]
                q = to[-1]
            elif to[-2:] =='sS' or to[-2:] =='aa':
                to = to[:-2]
                q = to[-2:]
            elif to[-1] =='a' or to[-1] =='A' or to[-1] =='v' or to[-1] =='V' or to[-1] =='o':
                to = to[:-1]
                q = to[-1]

            track_number = list(range(int(fr), int(to)+1))
        return track_number, q

    @classmethod
    def normalization_folder(cls, folder):
        folder = re.sub("\: ", " - ", folder)
        folder = re.sub("\?|\*", " ", folder)
        folder = re.sub("\:", "", folder)
        folder = re.sub("\.\.\.", "", folder)
        folder = re.sub("\.\.\.", "", folder)
        folder = re.sub(" / ", "", folder)
        folder = re.sub("/", "", folder)
        return folder

    @classmethod
    def create_download_path(cls, id, download_path, is_single = False, original_artist = False, single_on_artist_folder = False):
        '''
            parameter:
                id = (int) album_id
                download_path = (str) directory path
                is_single = (str) change download_path to: os.path.join(download_path, "SINGLES") and for earch directory inside: download_path += " [single]"
                original_artist = (bool) check if single_on_artist_folder for True or False
                single_on_artist_folder = (bool) Download all tracks into direct Just artist folder

            return:
                (str) download_path
        '''

        debug(download_path = download_path)
        debug(original_artist = original_artist)
        debug(single_on_artist_folder = single_on_artist_folder)
        if original_artist and not single_on_artist_folder:
            download_path = os.path.join(download_path, original_artist, "SINGLES")
        elif original_artist and single_on_artist_folder:
            download_path = os.path.join(download_path, original_artist)
        else:
            while 1:
                try:
                    album_detail = cls.deezer.get_album(id)
                    break
                except:
                    pass
            while 1:
                try:
                    cover_data = cls.deezer.get_album_poster(album_detail, 1200)
                    break
                except:
                    pass
            artist_data = album_detail.get('artist')
            artist = artist_data.get('name')
            release_date = album_detail.get('release_date')
            release = datetime.strptime(release_date, '%Y-%m-%d')
            release_year = release.year
        
            if not os.path.isdir(os.path.join(download_path, artist)):
                os.makedirs(os.path.join(download_path, artist))
            download_path = os.path.join(download_path, artist)
            if is_single:
                download_path = os.path.join(download_path, "SINGLES")
            # folder_name = artist + " - " + album_detail.get('title') + " (" + str(release_year) + ")"
            folder_name = "(" + str(release_date) + ") " + album_detail.get('title')
            folder_name = cls.normalization_folder(folder_name)
            download_path = os.path.join(download_path, folder_name)

            if is_single:
                download_path += " [single]"
            if not os.path.isdir(download_path):
                try:
                    os.makedirs(download_path)
                except:
                    pass
            
            cls.create_image(download_path, cover_data, album_detail = album_detail, id = id)
        
        if not os.path.isdir(download_path):
            try:
                os.makedirs(download_path)
            except:
                pass
        
        debug(download_path = download_path)
        return download_path

    @classmethod
    def detect_input(cls, data_input):
        is_artist = False
        is_album = False
        data = None
        if "artist" in data_input:
            data = re.sub("artist:|artist", "", data_input, re.I).strip()
            is_artist = True
        elif "album" in data_input:
            data = re.sub("album:|album", "", data_input, re.I).strip()
            is_album = True
        else:
            data = data_input
        debug(data = data)
        debug(is_album = is_album)
        debug(is_artist = is_artist)
        return data, is_artist, is_album

    @classmethod
    def create_image(cls, download_path, cover_data = None, filename = None, id = None, album_detail = None):
        cover_name = 'Cover'
        poster_name = 'Poster'
        artist_pic = "Artist"

        if not cover_data and id:
            if not album_detail:
                while 1:
                    try:
                        album_detail = cls.deezer.get_album(id)
                        break
                    except:
                        pass
            while 1:
                try:
                    cover_data = cls.deezer.get_album_poster(album_detail, 1200)
                    break
                except:
                    pass
        if not album_detail and id:
            while 1:
                try:
                    album_detail = cls.deezer.get_album(id)
                    break
                except:
                    pass
        artist_data = album_detail.get('artist')
        while 1:
            try:
                artist_picture_data = cls.deezer.get_artist_poster(cls.deezer.get_artist(artist_data.get('id')), 1000)
                break
            except:
                pass
        if cover_data:
            if filename:
                if filename.lower().endswith('.mp3') or filename.lower().endswith('.flac'):
                    filename = re.sub("\.mp3|\.flac", "", filename, re.I)
                cover = filename + "." + cover_data.get('ext')    
            else:
                cover = cover_name + "." + cover_data.get('ext')
                poster = poster_name + "." + cover_data.get('ext')
                artist_pic = "Artist" + "." + artist_picture_data.get('ext')
                
                cover = os.path.join(download_path, cover)
                poster = os.path.join(download_path, poster)
                artist_pic = os.path.join(download_path, artist_pic)

                with open(u"{}".format(poster), 'wb') as poster_file:
                    poster_file.write(cover_data.get('image'))
                with open(u"{}".format(artist_pic), 'wb') as artist_pic_file:
                    artist_pic_file.write(artist_picture_data.get('image'))
                
            with open(u"{}".format(cover), 'wb') as cover_file:
                cover_file.write(cover_data.get('image'))
        
    @classmethod
    def print_nav(cls, q, default = "Select Number:", ntype = 1):
        if not q:
            if ntype == 1: #ARTIST
                print(
                    make_colors("n = Select discography of Artist", 'b', 'lw') + ", " +\
                    
                    make_colors("[n]a = Select show Album with Appereance of Artist Only", 'b', 'lg') + ", " +\
                    make_colors("[n]A = Select show Album with Appereance of Artist from Discography (default)", 'b', 'lg') + ", " +\
                    make_colors("[n]o = Select show Album of Artist Only", 'b', 'lc') + ", " +\
                    make_colors("[n]s = Select show Single of Artist Only", 'b', 'ly') + ", " +\
                    make_colors("[n]S = Select show Single of Artist Only from Discography", 'b', 'ly') + ", " +\
                    make_colors("[n]v = Select show Appereance of Artist Only", 'lw', 'm') + ", " +\
                    make_colors("[n]V = Select show Appereance of Artist from Discography", 'lw', 'm') + ", " +\

                    make_colors("[n]da = Direct download Album with Appereance of Artist Only", 'b', 'lg') + ", " +\
                    make_colors("[n]dA = Direct download Album with Appereance of Artist from Discography", 'b', 'lg') + ", " +\
                    make_colors("[n]do = Direct download Album from Original Artist Only", 'b', 'lc') + ", " +\
                    make_colors("[n]ds = Direct download Single Album of Artist Only", 'b', 'ly') + ", " +\
                    make_colors("[n]dS = Direct download Single Album of Artist Only from Discography", 'b', 'ly') + ", " +\
                    make_colors("[n]dss = Direct download Single Album of Artist into \"SINGLES\" folder", 'b', 'ly') + ", " +\
                    make_colors("[n]dsS = Direct download Single Album of Artist from Discography into artist folder", 'b', 'ly') + ", " +\
                    make_colors("[n]dv = Direct download Appereance of Artist Only", 'lw', 'm') + ", " +\
                    make_colors("[n]dV = Direct download Appereance of Artist from Discography", 'lw', 'm') + ", " +\
                    
                    make_colors("x|q|exit|quit = Exit/Quit", 'lr')
                )
            elif ntype == 2: #ALBUM
                print(
                    make_colors("n = Select album number to download", 'b', 'lw') + ", " +\
                    make_colors("a = Download All Albums ", 'lw', 'lr') + ", " +\
                    make_colors("a[o] = Download All Albums From Original Artist Only", 'lw', 'lr') + ", " +\
                    make_colors("a[s] = Download All Single Albums Tracks into \"SINGLES\" folder", 'lw', 'lr') + ", " +\
                    make_colors("a[S] = Download All Single Albums Tracks int save in Artist Folder", 'lw', 'lr') + ", " +\
                    # make_colors("a[sS] = Download All Single Albums Tracks int save in Artist Folder", 'lw', 'lr') + ", " +\
                    make_colors("n1,nx,n1-nx = Download All Albums in range", 'lw', 'lr') + ", " +\
                    make_colors("aa = Select show Album with Appereance of Artist", 'b', 'lg') + ", " +\
                    make_colors("A = Select show Album with Appereance of Artist from Discography", 'lr', 'ly') + ", " +\
                    make_colors("o = Select show Album of Artist Only", 'b', 'lc') + ", " +\
                    make_colors("s = Select show Single of Artist Only", 'b', 'ly') + ", " +\
                    make_colors("S = Select show Single of Artist Only from Discography", 'b', 'ly') + ", " +\
                    make_colors("v = Select show Appereance of Artist Only", 'lw', 'm') + ", " +\
                    make_colors("V = Select show Appereance of Artist from Discography", 'lw', 'm') + ", " +\
                    make_colors("x|q|exit|quit = Exit/Quit", 'lr')
                )

            elif ntype == 3: #TRACK
                print(
                    make_colors("n = Select track number to download", 'b', 'lw') + ", " +\
                    make_colors("a = Download All tracks ", 'lw', 'lr') + ", " +\
                    make_colors("n1,nx,n1-nx = Download All tracks in range", 'lw', 'lr') + ", " +\
                    make_colors("aa = Select show Album with Appereance of Artist", 'b', 'lg') + ", " +\
                    make_colors("A = Select show Album with Appereance of Artist from Discography", 'lr', 'ly') + ", " +\
                    make_colors("o = Select show Album of Artist Only", 'b', 'lc') + ", " +\
                    make_colors("s = Select show Single of Artist Only", 'b', 'ly') + ", " +\
                    make_colors("S = Select show Single of Artist Only from Discography", 'b', 'ly') + ", " +\
                    make_colors("v = Select show Appereance of Artist Only", 'lw', 'm') + ", " +\
                    make_colors("V = Select show Appereance of Artist from Discography", 'lw', 'm') + ", " +\
                    make_colors("x|q|exit|quit = Exit/Quit", 'lr')
                    # aa, sA, o, s, sS, v, sV
                )
        
            q = raw_input(make_colors(default, 'lw', 'bl') + " ")
        if q:
            q = str(q).strip()
        if q == 'x' or q == 'exit' or q == 'q' or q == 'quit':
            sys.exit(make_colors("Exit ...", 'lw', 'lr'))
        return q

    @classmethod
    def create_and_download(cls, disco, ORGARTIST, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, album_numbers = None, q = None):
        debug(ORGARTIST = ORGARTIST)
        debug(album_numbers = album_numbers)
        def download(id, ORGARTIST, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE):
            if not DOWNLOAD_IS_SINGLE and DOWNLOAD_SINGLE_ONLY:
                return False
            while 1:
                try:
                    tracks = cls.deezer.get_album_tracks(id)
                    break
                except:
                    pass
            debug(len_tracks = len(tracks))    
            debug(ORGARTIST = ORGARTIST)
            download_path = cls.create_download_path(id, download_path, DOWNLOAD_SINGLE_ONLY, ORGARTIST, INTO_ARTIST_FOLDER)
            debug(download_path = download_path)
            cls.download(tracks, None, fformat, download_path, overwrite, d, DOWNLOAD_SINGLE_ONLY, dont_overwrite, INTO_ARTIST_FOLDER|INTO_SINGLE_FOLDER)
            return True

        if q:
            id = disco[q - 1]['ALB_ID']
            download(id, ORGARTIST, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE)
        else:
            if not album_numbers:
                for d in disco:
                    DOWNLOAD_IS_SINGLE = False
                    if int(d.get('TYPE')) == 0:
                        DOWNLOAD_IS_SINGLE = True

                    id = d.get('ALB_ID')
                    download(id, ORGARTIST, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE)
                    
            else:
                for ds in album_numbers:
                    DOWNLOAD_IS_SINGLE = False
                    id = disco[int(ds) - 1].get('ALB_ID')
                    download(id, ORGARTIST, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE)
                
        if ORGARTIST or INTO_ARTIST_FOLDER:
            cls.re_numbering_files(download_path, ORGARTIST)

    @classmethod
    def filter_disco(cls, disco, artist_name):
        disco_filter = []
        for ds in disco:
            # debug(ART_NAME = ds.get('ART_NAME'))
            # debug(artist_name = artist_name)
            if ds.get('ART_NAME') == artist_name:
                disco_filter.append(ds)
        return disco_filter

    @classmethod
    def print_disco_album(cls, result, query, print_list_album, download_path, ftype, fformat, overwrite, dont_overwrite):
        disco = []
        for dc in result:
            while 1:
                try:
                    album_detail = cls.deezer.get_album(dc['id'])
                    break
                except:
                    pass
            # debug(album_detail_key = album_detail.keys())
            dc.update({'DIGITAL_RELEASE_DATE': album_detail['release_date']})
            dc.update({'ALB_ID': dc['id']})

            disco.append(dc)

        # debug(disco = disco)
        debug(len_disco = len(disco))
        if not disco:
            return cls.download_interactive(query, download_path, ftype, fformat, overwrite = overwrite, dont_overwrite = dont_overwrite)
        disco = sorted(disco, key = lambda k: k['DIGITAL_RELEASE_DATE'], reverse = True)
        debug(d_keys = disco[0].keys())
        n = 1
        if print_list_album:
            print(make_colors("DISCOGRAPHY:", 'lw', 'g') + " ")
            for d in disco:
                album_artist_name = d.get('artist').get('name')
                album_artist_name = make_colors("{0} album".format(album_artist_name), 'lw', 'lr')
                debug(TYPE = d.get('type'))
                IS_SINGLE = ""
                # if not d.get('type') == 'album':
                #     IS_SINGLE = " " + make_colors("[SINGLE]", 'b', 'lg')
                
                print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('title'), 'lw', 'bl') + " / " + album_artist_name + IS_SINGLE + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                n += 1
            # if cls.thread:
            #     cls.thread.terminate()
            # cls.thread = multiprocessing.Process(target = notify, args = ('Deez', 'Deez', 'ready to select album', 'Ready to Select Album !', None, None, None, cls.LOGO, True, True, True, None, None, True))
            # cls.thread.start()
            notify('Deez', 'Deez', 'ready to select album', 'Ready to Select Album !', None, None, None, cls.LOGO, True, True, True, None, None, True)
        q = cls.print_nav(None, "Select Number:", 2)
        q, is_artist, is_album = cls.detect_input(q)
        if is_artist:
            return cls.download_interactive(q, download_path, 'artist', fformat, None, True, overwrite, None, None, True, dont_overwrite)
        return disco, q

    @classmethod
    def download_interactive(cls, query, download_path = None, ftype='artist', fformat='mp3', q = None, print_list_artist = True, overwrite = False, q1 = None, q2 = None, print_list_album = True, dont_overwrite = False, result = [], disco = None, album_numbers = None):
        DIRECT_DOWNLOAD = False
        if print_list_artist:
            q = None
        if not result:
            result = cls.find(query, ftype)

        ORGARTIST = query

        if not download_path:
            download_path = os.getcwd()
        download_path0 = download_path
        debug(q = q)
        if result:
            n = 1
            if ftype == 'artist':
                if print_list_artist:
                    for i in result:
                        print(cls.format_number(n, len(result)) +  ". " + make_colors(i.get('name'), 'lw', 'bl') + "[" + make_colors("{0} album".format(i.get('nb_album')), 'bl', 'ly') + "]")
                        n +=1
                q = cls.print_nav(q)
                debug(q = q)
                if q:
                    q = str(q).strip()
                else:
                    sys.exit()
                debug(q = q)
                q, is_artist, is_album = cls.detect_input(q)
                if is_album:
                    return cls.download_interactive(q, download_path, 'album', fformat, None, print_list_artist, overwrite, None, None, print_list_album, dont_overwrite, result, disco, album_numbers)
                
                just_artist, just_artist_disco, just_origin, just_singles, just_single_disco, just_others, just_other_disco, download_album_artist, download_album_artist_with_appereance, download_album_artist_disco, download_singles, download_single_disco, download_others, download_other_disco, download_into_artist_folder, q = cls.set_config_artist(q)

                debug(just_singles = just_singles)
                debug(q = q)

            elif ftype == 'album':
                disco, q = cls.print_disco_album(result, query, print_list_album, download_path, ftype, fformat, overwrite, dont_overwrite)

            if q[-1:] == 'd':
                q = q[:-1]
                DIRECT_DOWNLOAD = True
            if q and q.isdigit():
                debug(q = q)
                debug(len_result = len(result))
                if int(q) <= len(result):
                    debug(q = q)
                    debug(ftype = ftype)
                    n = 1
                    if ftype == 'artist':
                        id = result[int(q) - 1].get('id')
                        artist_name = result[int(q) - 1].get('name')
                        ORGARTIST = artist_name
                        debug(id = id)
                        #id = 81238
                        if not disco:
                            while 1:
                                try:
                                    if not just_artist and not just_origin and not just_singles and not just_others and not download_album_artist and not download_singles and not download_others:
                                        disco = cls.deezer.get_artist_discography(id)
                                        if just_artist_disco or download_album_artist_disco:
                                            disco_t = disco
                                            disco = []
                                            for p in disco_t:
                                                if p.get('ART_NAME') == artist_name:
                                                    disco.append(p)
                                        elif just_single_disco or download_single_disco:
                                            disco_t = disco
                                            disco = []
                                            for p in disco_t:
                                                if int(p.get('TYPE')) == 0:
                                                    disco.append(p)
                                        elif just_other_disco or download_other_disco:
                                            disco_t = disco
                                            disco = []
                                            for p in disco_t:
                                                if not int(p.get('TYPE')) == 0 or not p.get('ART_NAME') == artist_name:
                                                    disco.append(p)
                                    else:
                                        disco = cls.deezer.get_artist(id)['ALBUMS']['data']
                                        if just_origin or download_album_artist:
                                            disco_t = disco
                                            disco = []
                                            for p in disco_t:
                                                if p.get('ART_NAME') == artist_name:
                                                    disco.append(p)
                                        elif just_singles or download_singles:
                                            disco_t = disco
                                            disco = []
                                            debug(len_disco_t = len(disco_t))
                                            for p in disco_t:
                                                debug(album_type = p.get('TYPE'))
                                                if int(p.get('TYPE')) == 0:
                                                    disco.append(p)
                                            debug(len_disco = len(disco))
                                            # pause()
                                        elif just_others or download_others:
                                            disco_t = disco
                                            disco = []
                                            for p in disco_t:
                                                if not int(p.get('TYPE')) == 0 or not p.get('ART_NAME') == artist_name:
                                                    disco.append(p)
                                        
                                    break
                                except:
                                    traceback.format_exc()
                        
                        if download_album_artist_with_appereance or download_album_artist_disco:
                            q1 = 'all'
                            print_list_album = False
                        elif download_album_artist:
                            q1 = 'ao'
                        elif download_singles:# or  or download_others or download_other_disco:
                            q1 = 'as'
                        elif download_single_disco:
                            q1 = 'aS'

                        # debug(disco = disco)
                        debug(len_disco = len(disco))
                        if not disco:
                            return cls.download_interactive(query, download_path, ftype, fformat, overwrite = overwrite, dont_overwrite = dont_overwrite)
                        disco = sorted(disco, key = lambda k: k['DIGITAL_RELEASE_DATE'], reverse = True)
                        debug(d_keys = disco[0].keys())
                        if print_list_album:
                            print(make_colors("DISCOGRAPHY:", 'lw', 'g') + " ")
                            for d in disco:
                                album_artist_name = d.get('ART_NAME')
                                if artist_name == album_artist_name:
                                    album_artist_name = make_colors("{0} album".format(d.get('ART_NAME')), 'lw', 'lr')
                                else:
                                    if album_artist_name == "Various Artists":
                                        album_artist_name = make_colors("{0} album".format(d.get('ART_NAME')), 'lw', 'm')
                                    else:    
                                        album_artist_name = make_colors("{0} album".format(d.get('ART_NAME')), 'b', 'y')
                                if int(d.get('TYPE')) == 0:
                                    IS_SINGLE = " " + make_colors("[SINGLE]", 'b', 'lg')
                                else:
                                    IS_SINGLE = ""
                                print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('ALB_TITLE'), 'lw', 'bl') + " / " + album_artist_name + IS_SINGLE + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                                n += 1
                            # if cls.thread:
                            #     cls.thread.terminate()
                            # cls.thread = multiprocessing.Process(target = notify, args = ('Deez', 'Deez', 'ready to select album', 'Ready to Select Album !', None, None, None, cls.LOGO, True, True, True, None, None, True))
                            # cls.thread.start()
                            notify('Deez', 'Deez', 'ready to select album', 'Ready to Select Album !', None, None, None, cls.LOGO, True, True, True, None, None, True)
                    # q1 = raw_input(make_colors("Select Number:", 'lw', 'm') + " ")
                    debug(q = q)
                    if ftype == 'album':
                        q1 = q
                    if not q1:
                        q1 = cls.print_nav(None, "Select Number:", 2)
                    debug(q1 = q1)
                    q1, is_artist, is_album = cls.detect_input(q1)
                    debug(q1 = q1)
                    if q1[-1:] == 'd' and not is_artist and not is_album:
                        q1 = q1[:-1]
                        DIRECT_DOWNLOAD = True
                    if is_album and not ftype == 'album':
                        return cls.download_interactive(q1, download_path, 'album', fformat, None, print_list_artist, overwrite, None, None, print_list_album, dont_overwrite, result, disco, album_numbers)
                    elif is_artist and not ftype == 'artist':
                        return cls.download_interactive(q1, download_path, 'artist', fformat, None, print_list_artist, overwrite, None, None, print_list_album, dont_overwrite, result, disco, album_numbers)
                    if q1:
                        q1 = str(q1).strip()
                    if q1 == 'q' or q1 == 'x':
                        sys.exit()

                    if q1 and q1.isdigit():
                        DOWNLOAD_IS_SINGLE = False
                        debug(q1 = q1)
                        debug(len_disco = len(disco))
                        if int(q1) <= len(disco):
                            n = 1
                            id = disco[int(q1) - 1].get('ALB_ID')
                            if ftype == 'artist':
                                if int(disco[int(q1) - 1].get('TYPE')) == 0:
                                    DOWNLOAD_IS_SINGLE = True
                            elif ftype == 'album':
                                debug(TYPE = disco[int(q1) - 1].get('type'), debug = True)
                            #     if not disco[int(q1) - 1].get('type') == 'album':
                            #         DOWNLOAD_IS_SINGLE = True
                            while 1:
                                try:
                                    tracks = cls.deezer.get_album_tracks(id)
                                    break
                                except:
                                    pass
                            if not DIRECT_DOWNLOAD:
                                nt = 1
                                for track in tracks:
                                    if fformat == 'flac':
                                        print(make_colors(cls.format_number(str(nt), len(tracks)), 'lc') + " " + make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE_FLAC'))).MB)) + " mb", 'lw', 'm') + "]")
                                    else:
                                        print(make_colors(cls.format_number(str(nt), len(tracks)), 'lc') + " " + make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE'))).MB)) + " mb", 'lw', 'm') + "]")
                                        nt += 1
                            # if cls.thread:
                            #     cls.thread.terminate()
                            # cls.thread = multiprocessing.Process(target = notify, args = ('Deez', 'Deez', 'ready to download album', 'Ready to Download Album !', None, None, None, cls.LOGO, True, True, True, None, None, True))
                            # cls.thread.start()
                            else:
                                q2 = 'all'
                        notify('Deez', 'Deez', 'ready to download album', 'Ready to Download Album !', None, None, None, cls.LOGO, True, True, True, None, None, True)
                        # debug(tracks = tracks)
                        debug(q2 = q2)
                        # pause()
                        debug(len_tracks = len(tracks))
                        if not q2:
                            q2 = cls.print_nav(None, "Select Number to download: ", 2)
                        q2, is_artist, is_album = cls.detect_input(q2)
                        if is_album and not ftype == 'album':
                            return cls.download_interactive(q2, download_path, 'album', fformat, None, print_list_artist, overwrite, None, None, print_list_album, dont_overwrite, result, disco, album_numbers)
                        elif is_artist and not ftype == 'artist':
                            return cls.download_interactive(q2, download_path, 'artist', fformat, None, print_list_artist, overwrite, None, None, print_list_album, dont_overwrite, result, disco, album_numbers)
                        debug(q2 = q2)
                        if q2:
                            download_path = cls.create_download_path(id, download_path, DOWNLOAD_IS_SINGLE)
                        download_single_only = False
                        if ftype == 'artits':
                            if just_singles or just_single_disco:
                                download_single_only = True
                        if q2 and q2 == 'all' or q2 == 'a':
                            cls.download(tracks, None, fformat, download_path, overwrite, disco[int(q1) - 1], download_single_only, dont_overwrite)

                        elif "-" in q2 or "," in q2:
                            download_single_only = False
                            if ftype == 'artits':
                                if just_singles or just_single_disco:
                                    download_single_only = True
                            if "," in q2:
                                track_number_1 = re.split(",", q2)
                                debug(track_number_1 = track_number_1)
                                track_number_1 = list(filter(None, track_number_1))
                                debug(track_number_1 = track_number_1)
                                for i in track_number_1:
                                    if "-" in i:
                                        track_number, _ = cls.split_number(i)
                                        cls.download(tracks, track_number, fformat, download_path, overwrite, disco[int(q1) - 1], download_single_only, dont_overwrite)
                                    else:
                                        cls.download(tracks, [i], fformat, download_path, overwrite, disco[int(q1) - 1], download_single_only, dont_overwrite)
                            elif "-" in q2:
                                track_number, _ = cls.split_number(q2)
                                debug(track_number = track_number)
                                cls.download(tracks, track_number, fformat, download_path, overwrite, disco[int(q1) - 1], download_single_only, dont_overwrite)

                        else:
                            # track_id = tracks[int(q2) - 1].get('SNG_ID')
                            debug(q2 = q2)
                            if q2 and str(q2).isdigit():
                                download_status = cls.download(tracks, [int(q2)], fformat, download_path, overwrite, disco[int(q1) - 1], download_single_only, dont_overwrite)
                                if download_status == "pass":
                                    return cls.download_interactive(query, download_path0, ftype, fformat, q, False, overwrite, q1, q2, False, dont_overwrite)
                            else:
                                if q2:
                                    if q1 == 'aa' or q1 == 'A' or q1 == 'o' or q1 == 's' or q1 == 'S' or q1 == 'v' or q1 == 'V': 
                                        return cls.download_interactive(query, download_path0, ftype, fformat, q1 + q2, False, dont_overwrite)        
                                    else:
                                        return cls.download_interactive(q2, download_path0, ftype, fformat, None, overwrite = overwrite, dont_overwrite = dont_overwrite)

                                # else:
                                    return cls.download_interactive(query, download_path0, ftype, fformat, None, overwrite = overwrite, dont_overwrite = dont_overwrite)

                        # if cls.thread:
                        #     cls.thread.terminate()
                        # cls.thread = multiprocessing.Process(target = notify, args = ('Deez', 'Deez', 'finish', 'All Download Finished !', None, None, None, cls.LOGO, True, True, True, None, None, True))
                        # cls.thread.start()
                        notify('Deez', 'Deez', 'finish', 'All Download Finished !', None, None, None, cls.LOGO, True, True, True, None, None, True)

                    elif q1 and len(q1) < 6 and 'all' in q1 or 'a' in q1 or q1 == 'all' or q1 == 'a':
                        DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY, _, _ = cls.set_config(q1)
                        if DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY:
                            disco = cls.filter_disco(disco, ORGARTIST)
                            debug(len_disco = len(disco))
                        debug(ORGARTIST = ORGARTIST)
                        cls.create_and_download(disco, ORGARTIST, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path0)
                        DOWNLOAD_ORIGINAL_ALBUM_ONLY = INTO_SINGLE_FOLDER = INTO_ARTIST_FOLDER = DOWNLOAD_SINGLE_ONLY = DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = None
                        # pause()

                    elif "-" in q1 or "," in q1:
                        DOWNLOAD_IS_SINGLE = False
                        
                        if "," in q1:
                            album_numbers = re.split(",", q1)
                            debug(album_numbers = album_numbers)
                            album_numbers = list(filter(None, album_numbers))
                            debug(album_numbers = album_numbers)
                            for ds in album_numbers:
                                if "-" in ds:
                                    # ALL_AS_ORGARTIST, ALL_SINGLES_AS_ORGARTIST, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST, _, album_numbers1 = cls.set_config(ds.strip().split("-")[-1])
                                    DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY, _, album_numbers1 = cls.set_config(ds.strip().split("-")[-1])
                                    if DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY:
                                        disco = cls.filter_disco(disco, ORGARTIST)
                                    if not album_numbers1:
                                        album_numbers1, _ = cls.split_number(ds)
                                    debug(album_numbers = album_numbers1)
                                    cls.create_and_download(cls, disco, query, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path0, album_numbers1)

                                    # for dss in album_numbers1:
                                    #     id1 = disco[int(dss) - 1].get('ALB_ID')
                                    #     if isinstance(ORGARTIST, bool):
                                    #         ORGARTIST = query
                                        
                                    #     if (disco[int(dss) - 1].get('ART_NAME').lower() == ORGARTIST.lower() and not DOWNLOAD_SINGLE_ONLY) or DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST:
                                    #         ORGARTIST = disco[int(dss) - 1].get('ART_NAME')
                                    #         try:
                                    #             os.rename(os.path.join(download_path, query), os.path.join(download_path, ORGARTIST))
                                    #         except:
                                    #             pass

                                    #     if disco[int(dss) - 1].get('TYPE') == '0' or disco[int(dss) - 1].get('TYPE') == 0:
                                    #         DOWNLOAD_IS_SINGLE = True    
                                        
                                    #     while 1:
                                    #         try:
                                    #             tracks = cls.deezer.get_album_tracks(id1)
                                    #             break
                                    #         except:
                                    #             pass

                                    #     if DOWNLOAD_SINGLE_ONLY and not ALL_SINGLES_AS_ORGARTIST:
                                    #         ORGARTIST = ''
                                    #     download_path = cls.create_download_path(id1, download_path0, DOWNLOAD_IS_SINGLE, ORGARTIST, ALL_SINGLES_AS_ORGARTIST)
                                    #     cls.download(tracks, fformat = fformat, download_path = download_path, overwrite = overwrite, disco = disco[int(dss) - 1], single_only = DOWNLOAD_SINGLE_ONLY, dont_overwrite = dont_overwrite)

                                    # if ALL_SINGLES_AS_ORGARTIST:
                                    #     cls.re_numbering_files(download_path, ORGARTIST)
                                    DOWNLOAD_ORIGINAL_ALBUM_ONLY = INTO_SINGLE_FOLDER = INTO_ARTIST_FOLDER = DOWNLOAD_SINGLE_ONLY = DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = None
                                else:
                                    # ALL_AS_ORGARTIST, ALL_SINGLES_AS_ORGARTIST, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST, qx, album_numbers1 = cls.set_config(ds)
                                    DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY, qx, _ = cls.set_config(ds)
                                    if DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY:
                                        disco = cls.filter_disco(disco, ORGARTIST)
                                    cls.create_and_download(cls, disco, query, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path0, None, qx)

                                    # id = disco[int(qx) - 1].get('ALB_ID')
                                    # if ds[-1] == 'o':
                                    #     ALL_AS_ORGARTIST = True
                                    #     id = disco[int(ds[:-1]) - 1].get('ALB_ID')
                                    # elif ds[-1] == 's':
                                    #     ALL_SINGLES_AS_ORGARTIST = True
                                    #     id = disco[int(ds[:-1]) - 1].get('ALB_ID')
                                    # elif ds[-1] == 'S' and not ds[-2:] == 'sS':
                                    #     DOWNLOAD_SINGLE_ONLY = True
                                    #     ORGARTIST = False
                                    #     id = disco[int(ds[:-1]) - 1].get('ALB_ID')
                                    # elif ds[-2:] == 'sS':
                                    #     DOWNLOAD_SINGLE_ONLY = True
                                    #     DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST = True
                                    #     ALL_SINGLES_AS_ORGARTIST = False
                                    #     id = disco[int(ds[:-2]) - 1].get('ALB_ID')
                                    # else:
                                    #     id = disco[int(ds) - 1].get('ALB_ID')

                                    DOWNLOAD_ORIGINAL_ALBUM_ONLY = INTO_SINGLE_FOLDER = INTO_ARTIST_FOLDER = DOWNLOAD_SINGLE_ONLY = DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = None

                        elif "-" in q1:
                            DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY, _, album_numbers = cls.set_config(q1.strip().split("-")[-1])
                            if DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY:
                                disco = cls.filter_disco(disco, ORGARTIST)
                            if not album_numbers:
                                album_numbers, _ = cls.split_number(q1)
                            debug(album_numbers = album_numbers)
                            cls.create_and_download(cls, disco, query, DOWNLOAD_ORIGINAL_ALBUM_ONLY, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path0, album_numbers1)
                            DOWNLOAD_ORIGINAL_ALBUM_ONLY = INTO_SINGLE_FOLDER = INTO_ARTIST_FOLDER = DOWNLOAD_SINGLE_ONLY = DOWNLOAD_SINGLE_ORIGINAL_ARTIST_ONLY = None
                            # DOWNLOAD_IS_SINGLE = False
                            # ALL_AS_ORGARTIST, ALL_SINGLES_AS_ORGARTIST, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST, _, album_numbers = cls.set_config(q1.strip().split("-")[-1])
                            
                            # if not album_numbers:
                            #     album_numbers = cls.split_number(q1)
                            # debug(album_numbers = album_numbers)
                            # for ds in album_numbers:
                            #     DOWNLOAD_IS_SINGLE = False
                            #     id = disco[int(ds) - 1].get('ALB_ID')
                                
                            #     if isinstance(ORGARTIST, bool):
                            #         ORGARTIST = query
                            #     if (disco[int(ds) - 1].get('ART_NAME').lower() == ORGARTIST.lower() and not DOWNLOAD_SINGLE_ONLY) or DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST:
                            #         ORGARTIST = disco[int(ds) - 1].get('ART_NAME')
                            #         try:
                            #             os.rename(os.path.join(download_path, query), os.path.join(download_path, ORGARTIST))
                            #         except:
                            #             pass
                                
                            #     if disco[int(ds) - 1].get('TYPE') == '0' or disco[int(ds) - 1].get('TYPE') == 0:
                            #         DOWNLOAD_IS_SINGLE = True    
                                
                            #     while 1:
                            #         try:
                            #             tracks = cls.deezer.get_album_tracks(id)
                            #             break
                            #         except:
                            #             pass
                                        
                            #     if DOWNLOAD_SINGLE_ONLY and not ALL_SINGLES_AS_ORGARTIST:
                            #         ORGARTIST = ''
                            #     download_path = cls.create_download_path(id, download_path0, DOWNLOAD_IS_SINGLE, ORGARTIST, ALL_SINGLES_AS_ORGARTIST)
                            #     cls.download(tracks, fformat = fformat, download_path = download_path, overwrite = overwrite, disco = disco[int(ds) - 1], single_only = DOWNLOAD_SINGLE_ONLY, dont_overwrite = dont_overwrite)
                            
                            #     if ALL_SINGLES_AS_ORGARTIST or DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST:
                            #         cls.re_numbering_files(download_path, ORGARTIST)
                            #     ALL_AS_ORGARTIST, ALL_SINGLES_AS_ORGARTIST, DOWNLOAD_SINGLE_ONLY, DOWNLOAD_SINGLE_ONLY_AND_ALL_SINGLES_AS_ORGARTIST = cls.clean_config()
                            
                    else:
                        debug(q = q)
                        debug(q1 = q1)
                        if q1:
                                # download_interactive(cls, query, download_path = None, ftype='artist', fformat='mp3', q = None, print_list_artist = True, overwrite = False, q1 = None, q2 = None, print_list_album = True, dont_overwrite = False, result = [], disco = None, album_numbers = None):
                            if q1 == 'aa' or q1 == 'A' or q1 == 'o' or q1 == 's' or q1 == 'S' or q1 == 'v' or q1 == 'V': 
                                return cls.download_interactive(query, download_path0, ftype, fformat, q + q1, False, overwrite, dont_overwrite = dont_overwrite)
                            else:
                                return cls.download_interactive(q1, download_path0, ftype, fformat, None, overwrite = overwrite, dont_overwrite = dont_overwrite)
                        else:
                            return cls.download_interactive(query, download_path0, ftype, fformat, None, overwrite = overwrite, dont_overwrite = dont_overwrite)

            else:
                debug(q = q)
                if q == 'aa' or q == 'A' or q == 'o' or q == 's' or q == 'S' or q == 'v' or q == 'V': 
                    return cls.download_interactive(query, download_path0, ftype, fformat, q, False)        
                else:
                    if not q:
                        return cls.download_interactive(query, download_path0, ftype, fformat, None, True, overwrite = overwrite, dont_overwrite = dont_overwrite)
                    else:        
                        return cls.download_interactive(q, download_path0, ftype, fformat, None, True, overwrite = overwrite, dont_overwrite = dont_overwrite)
        else:
            print(make_colors('Not Found !', 'lw', 'lr', ['blink']))
            sys.exit()
        return cls.download_interactive(query, download_path0, ftype, fformat, overwrite = overwrite, dont_overwrite = dont_overwrite)

    @classmethod
    def usage(cls):
        parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
        parser.add_argument('query', action = 'store', help = 'Search For Artist')
        parser.add_argument('-s', '--search-for', action = 'store', help = 'artist (default) | album')
        parser.add_argument('-p', '--download-path', action = 'store', help = 'Save download to')
        parser.add_argument('-t', '--type', action = 'store', help = 'mp3 or flac, default = mp3', default = 'mp3')
        parser.add_argument('-o', '--overwrite', action = 'store_true', help = "Overwrite if file exists")
        parser.add_argument('-do', '--dont-overwrite', action = 'store_true', help = "Dont Overwrite if file exists")
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            cls.download_interactive(args.query, args.download_path, args.search_for, args.type, overwrite = args.overwrite, dont_overwrite = args.dont_overwrite)
            
def usage():
    Deez.usage()
        
if __name__ == '__main__':    
    #Deez.download_interactive(sys.argv[1])
    Deez.usage()
    #print(Deez.format_number(sys.argv[1]))

    