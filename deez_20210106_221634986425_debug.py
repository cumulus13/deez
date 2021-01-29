#!d:/virtualenv/py-deezer/Scripts/python.exe

from __future__ import print_function

from pydeezer import Deezer
from pydeezer.constants import track_formats
import os
import sys
import re
from tagger2 import Tagger
import mutagen
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
try:
    from pydebugger.debug import debug
except:
    def debug(*args, **kwargs):
        return None
# from pywget import wget
from datetime import datetime
from xnotify.notify import notify
import shutil
import progressbar
import time
if __name__ == '__main__':
    import sleeper
else:
    from . import sleeper
from unidecode import unidecode

if sys.version_info.major == 2:
    pass
else:
    raw_input = input

try:
    from pause import pause
except:
    def pause(*args, **kwargs):
        raw_input("Enter to continue")

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
    DOWNLOAD_ORIGINAL = False #download all album(official/single)
    DOWNLOAD_DISCOGRAPHY = False #download all album(Discography)
    DOWNLOAD_SINGLE_ORIGINAL_ONLY = False #download all single album only from original album artist only
    DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = False #download all single album only from artit discography
    DOWNLOAD_INTO_ARTIST_FOLDER = False #download all Single track into Artist folder only (auto create)
    DOWNLOAD_INTO_SINGLE_FOLDER = False #download all Single track into "SINGLE" folder only (auto create)
    DOWNLOAD_VARIOUS_ORIGINAL = False #show all various artist album only from original album artist only
    DOWNLOAD_VARIOUS_DISCOGRAPHY = False #show all various artist album only from artit discography
    IS_SINGLE = False

    SHOW_ORIGINAL_ALBUM = False #show all album(official/single)
    SHOW_DISCOGRAPHY = False #show all album(Discography)
    SHOW_SINGLE_ORIGINAL_ARTIST_ONLY = False #show all single album only from original album artist only
    SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY = False #show all single album only from artit discography
    SHOW_VARIOUS_ORIGINAL = False #show all various artist album only from original album artist only
    SHOW_VARIOUS_DISCOGRAPHY = False #show all various artist album only from artit discography

    DOWNLOAD_ALL = False

    DIRECT_DOWNLOAD = False

    QUERY = ''

    Q_SEARCH = ''

    DOWNLOAD_PATH = os.getcwd()
    FFORMAT = "mp3"
    OVERWRITE = False
    DONT_OVERWRITE = False
    ORGARTIST = ''
    FTYPE = 'artist'

    configname = os.path.join(os.path.dirname(__file__), 'deez.ini')
    config = configset(configname)
    config.write_config('download', 'sleep', "")
    error = False
    prefix = '{variables.task} >> {variables.subtask}'
    variables =  {'task': '--', 'subtask': '--'}
    max_value = 60
    bar = progressbar.ProgressBar(max_value = max_value, prefix = prefix, variables = variables)
    nbar = 0
    task = make_colors("Connection Error", 'lw', 'lr', ['blink'])
    subtask = make_colors("Re-Connecting", 'b', 'lg', ['blink']) + " "
    ARL = config.get_config('AUTH', 'arl', "4659ecf4e9e46931714cbf470afd5242fdf97505c7f0e89aecc9442caa056064c9a538693acb37292467d76a2039e4e6b38e0d118fe018625d5252f38db315c46bf17d45cd1442acaf15006d9ef9d42aaf385a71c937b6fafa342bb2bb0dfa6e")

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

    CD = None
    LOGO = os.path.join(os.path.dirname(__file__), 'logo.png')
    
    def __init__(self, arl = None):
        super(Deez, self)
        if arl:
            self.ARL = arl
            self.deezer = Deezer(arl = arl)

    def browser_login(self, debugx = True, pausex = True):
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
        #pause(pausex)
        cef.Shutdown()    

    def create_window(self, debugx = True, pausex = True):
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
    def find(cls, query, ftype="artist", debugx = True, pausex = True):
        '''
        	ftype: "artist | album | track | playlist" (str)
        '''
        if not cls.deezer:
            print(make_colors("Invalid ARL !", 'lw', 'lr'))
            return False

        result = False
        debug(query = query, debug = debugx)
        debug(ftype = ftype)
        if ftype == 'artist':
            while 1:
                try:
                    result = cls.deezer.search_artists(query)
                    break
                except:
                    pass
        elif ftype == 'album':
            while 1:
                try:
                    result = cls.deezer.search_albums(query)
                    break
                except:
                    pass
        elif ftype == 'track':
            while 1:
                try:
                    result = cls.deezer.search_tracks(query)
                    break
                except:
                    pass
        elif ftype == 'playlist':
            while 1:
                try:
                    result = cls.deezer.search_playlists(query)
                    break
                except:
                    pass
        else:
            print(make_colors("Invalid ftype !", 'lw' ,'lr'))
        debug(len_result = len(result))
        return result
    
    @classmethod
    def format_number(cls, number, length = 10, debugx = True, pausex = True):
        number = str(number).strip()
        zeros = len(str(length)) - len(number)
        r = ("0" * zeros) + str(number)
        if len(r) == 1:
            return "0" + r
        return r

    @classmethod
    def re_tag(cls, musicfile, more = False):
        f = Tagger(musicfile)
        try:
            album = f.album.text
            f.comment.text = "From Album: {}\n{}".format(album, "LICFACE (licface@yahoo.com)")
            if more:
                f.album.text = "SINGLES (more)"
            else:
                f.album.text = "SINGLES"
            f.save()
        except:
            f = mutagen.File(musicfile)
            album = None
            comment = None
            for i in f.keys():
                if "TPE2" in i:
                    album = f.get(i)
                    break
            for i in in f.keys():
                if "COMM" in i:
                    comment = f.get(i)
                    break
            if not album:
                from mutagen.id3 import TPE2
                if more:
                    album = TPE2(text = "SINGLE (more)")
                else:
                    album = TPE2(text = "SINGLE")
                if comment:
                    comment.text = "{}".format("LICFACE (licface@yahoo.com)")
                else:
                    from mutagen.id3 import COMM
                    comment = COMM(text = "From Album: {}".format("LICFACE (licface@yahoo.com)"), lang="eng")
                    f.update({"COMM:Eng":comment})
                f.update({'TPE2':album})
            else:
                if comment:
                    comment.text = "From Album: {}\n{}".format(album.text, "LICFACE (licface@yahoo.com)")
                else:
                    from mutagen.id3 import COMM
                    comment = COMM(text = "From Album: {}\n{}".format(album.text, "LICFACE (licface@yahoo.com)"), lang="eng")
                    f.update({"COMM:Eng":comment})
            f.save()

    @classmethod
    def re_numbering_files(cls, download_path, album_artist = None, fformat = 'mp3', list_track_mp3 = None, debugx = True, pausex = True):
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
            #list_track_mp3 = list(filter(lambda k: k.endswith(".mp3"), list_track_files))
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
        if not list_track_mp3:
            list_track_mp3 = list(filter(lambda k: k.endswith(".mp3"), list_track_files))
        debug(list_track_files = list_track_files)
        debug(list_track_mp3 = list_track_mp3)
        nt = 1
        for f in list_track_mp3:
            f = re.sub("\n|\r|\t", "", f)
            debug(f = f)
            debug(fformat = fformat)
            if f.endswith("." + fformat):
                try:
                    tags = EasyID3(os.path.join(download_path, f))
                    debug(tags = tags)
                    tags['tracknumber'] = change_cd_track(str(nt), len(list_track_mp3))
                    tags['discnumber'] = change_cd_track("1")
                    try:
                        tags['composer']
                    except:
                        try:
                            tags.update({'composer':tags['artist']})
                        except:
                            if album_artist:
                                tags.update({'composer':album_artist})
                    # official_url
                    debug(album_artist = album_artist)
                    if album_artist:
                        tags['albumartist'] = album_artist
                    tags.save()
                except:
                    traceback.format_exc()
                name = re.sub("\d+\. ", "", f, 1)
                debug(name = name)
                debug(IS_FILE_f = os.path.join(download_path, f))
                debug(IS_FILE_image = os.path.splitext(os.path.join(download_path, f))[0] + ".jpg")
                while 1:
                    try:
                        os.rename(os.path.join(download_path, f), os.path.join(download_path, cls.format_number(nt) + ". " + name))
                        break
                    except:
                        tp, vl, tb = sys.exc_info()
                        if vl.__class__.__name__ == "PermissionError":
                            time.sleep(1)
                        else:
                            traceback.format_exc()
                            break
                if os.path.isfile(os.path.splitext(os.path.join(download_path, f))[0] + ".jpg"):
                    while 1:
                        try:
                            os.rename(os.path.splitext(os.path.join(download_path, f))[0] + ".jpg", os.path.splitext(os.path.join(download_path, cls.format_number(nt) + ". " + name))[0] + ".jpg")
                            break
                        except:
                            tp, vl, tb = sys.exc_info()
                            if vl.__class__.__name__ == "PermissionError":
                                time.sleep(1)
                            else:
                                traceback.format_exc()
                                break                    
                if os.path.isfile(os.path.splitext(os.path.join(download_path, f))[0] + ".png"):
                    while 1:
                        try:
                            os.rename(os.path.splitext(os.path.join(download_path, f))[0] + ".png", os.path.splitext(os.path.join(download_path, cls.format_number(nt) + ". " + name))[0] + ".png")
                            break
                        except:
                            tp, vl, tb = sys.exc_info()
                            if vl.__class__.__name__ == "PermissionError":
                                time.sleep(1)
                            else:
                                traceback.format_exc()
                                break                                        
                nt += 1

    @classmethod
    def downloader(cls, track_detail, filename, fformat, download_path, quality = track_formats.MP3_320, nmax = 600, debugx = True, pausex = True):
        # filename = name + "."+ fformat
        # download_track(track, download_dir, quality=None, fallback=True, filename=None, renew=False, with_metadata=True, with_lyrics=True, tag_separator=', ', **kwargs)
        filename = filename + fformat
        thread = multiprocessing.Process(target = track_detail["download"], args = (download_path, quality, True, filename))
        # track_detail["download"](download_path, quality=quality, filename = filename + fformat)
        print("STATUS0:", thread.is_alive())
        n = 0
        while 1:
            if thread.is_alive():
                print("STATUS:", thread.is_alive())
                print("n:", n)
                if n == n_max or n > n_max:
                    thread.terminate()
                    thread = multiprocessing.Process(target = track_detail["download"], args = (download_path, quality, True, filename))
                else:
                    n+=1
            else:
                break

    @classmethod
    def download(cls, tracks, numbers = None, fformat = 'mp3', download_path = None, overwrite = False, dont_overwrite = False, download_all_single = False, nmax = 600, debugx = True, pausex = True):
        # os.environ.update({'DEBUG':'1'})
        SLEEP = None
        debug(numbers = numbers)
        # debug(disco = disco)
        error = False
        download_path0 = download_path
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        print(make_colors("SAVE TO", 'lw', 'bl') + ": " + make_colors(download_path, 'lw', 'm'))

        debug(len_tracks = len(tracks))
        if not numbers:
            numbers = list(range(len(tracks) + 1))[1:]
            debug(numbers = numbers)
        debug(numbers = numbers)
        # album_id = disco['ALB_ID']
        # debug(album_id = album_id)
        
        for i in numbers:
            album_id = tracks[int(i) - 1].get('ALB_ID')
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
            #         album_detail = cls.deezer.get_album(album_id)
            #         # debug(track_detail = track_detail)
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
            debug(name = name, debug = True)
            debug(TRACK_NUMBER_INFO = track_detail.get('info').get('DATA').get('TRACK_NUMBER'), debug = True)
            debug(DISK_NUMBER_INFO = track_detail.get('info').get('DATA').get('DISK_NUMBER'), debug = True)
            debug(TRACK_NUMBER_TAGS = track_detail.get('tags').get('tracknumber'), debug = True)
            debug(DISK_NUMBER_TAGS = track_detail.get('tags').get('discnumber'), debug = True)
            debug(download_all_single = download_all_single, debug = True)

            if download_all_single:
                track_detail.get('info').get('DATA').update({'TRACK_NUMBER':str(cls.format_number(i, len(tracks)))})
                track_detail.get('info').get('DATA').update({'DISK_NUMBER':"01"})
                track_detail.get('info').get('DATA').update({'COMMENT':"From Album: " + track_detail.get('info').get('DATA').get('ALB_TITLE')})
                track_detail.get('tags').update({'tracknumber':str(cls.format_number(i, len(tracks))) + "/" + str(cls.format_number(len(tracks), len(tracks)))})
                track_detail.get('tags').update({'discnumber':"01"})
                track_detail.get('tags').update({'comment':"From Album: " + track_detail.get('tags').get('album')})

                # track_detail.get('info').get('DATA').update({'SNG_TITLE': tags_separated_by_comma['title']})
            if download_all_single:
                name = cls.format_number(i, len(tracks)) + ". " + tags_separated_by_comma['title']
            name = cls.normalization_folder(name)
            # print("NAME:", name)
            debug(name = name, debug = True)
            debug(TRACK_NUMBER_INFO = track_detail.get('info').get('DATA').get('TRACK_NUMBER'), debug = True)
            debug(DISK_NUMBER_INFO = track_detail.get('info').get('DATA').get('DISK_NUMBER'), debug = True)
            debug(TRACK_NUMBER_TAGS = track_detail.get('tags').get('tracknumber'), debug = True)
            debug(DISK_NUMBER_TAGS = track_detail.get('tags').get('discnumber'), debug = True)
            debug(i = i, debug = True)
            # pause()
            debug(track_detail = track_detail.get('info').get('DATA').keys())
            # debug(FILESIZE_AAC_64 = track_detail.get('info').get('DATA')['FILESIZE_AAC_64'])
            # debug(FILESIZE_MP3_64 = track_detail.get('info').get('DATA')['FILESIZE_MP3_64'])
            # debug(FILESIZE_MP3_128 = track_detail.get('info').get('DATA')['FILESIZE_MP3_128'])
            # debug(FILESIZE_MP3_256 = track_detail.get('info').get('DATA')['FILESIZE_MP3_256'])
            # debug(FILESIZE_MP3_320 = track_detail.get('info').get('DATA')['FILESIZE_MP3_320'])
            # debug(FILESIZE_MP4_RA1 = track_detail.get('info').get('DATA')['FILESIZE_MP4_RA1'])
            # debug(FILESIZE_MP4_RA2 = track_detail.get('info').get('DATA')['FILESIZE_MP4_RA2'])
            # debug(FILESIZE_MP4_RA3 = track_detail.get('info').get('DATA')['FILESIZE_MP4_RA3'])
            # debug(FILESIZE_FLAC = track_detail.get('info').get('DATA')['FILESIZE_FLAC'])
            # debug(FILESIZE = track_detail.get('info').get('DATA')['FILESIZE'])
            #name = os.path.join(download_path, name)
            #wget.download(url_download[0], out=name)
            
            if fformat == 'mp3':
                while 1:
                    try:
                        debug(name = name)
                        debug(FILE_1 = os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3"))
                        debug(FILE_2 = os.path.join(download_path, name + ".mp3"))
                        debug(FILE_3 = track_detail.get('info').get('DATA')['SNG_TITLE'])
                        debug(CHECK_FILE_1 = os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3")))    
                        debug(CHECK_FILE_2 = os.path.isfile(os.path.join(download_path, name + ".mp3")))
                        # pause(pausex)
                        if os.path.isfile(os.path.join(download_path, name + ".mp3")) and dont_overwrite:
                            pass
                        elif os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3")) and dont_overwrite:
                            pass
                        else:
                            if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".mp3")) and not overwrite:
                                q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                                if q == 'y' or q == 'Y':
                                    if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                        cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                    track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                                    cls.re_tag(os.path.join(download_path, name + "." + fformat))
                                    # def downloader(cls, track_detail, filename, fformat, download_path, quality = track_formats.MP3_320, nmax = 600):
                                    # cls.downloader(track_detail, name, fformat, download_path, track_formats.MP3_320, nmax)
                                    if SLEEP and str(SLEEP).isdigit():
                                        sleeper.sleep(SL=int(SLEEP))
                                    elif cls.config.get_config('download', 'sleep'):
                                        sleeper.sleep('download', 'sleep')
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
                                    if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                        cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                    track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                                    cls.re_tag(os.path.join(download_path, name + "." + fformat))
                                    # cls.downloader(track_detail, name, fformat, download_path, track_formats.MP3_320, nmax)
                                    if SLEEP and str(SLEEP).isdigit():
                                        sleeper.sleep(SL=int(SLEEP))
                                    elif cls.config.get_config('download', 'sleep'):
                                        sleeper.sleep('download', 'sleep')
                                elif q == 'n' or q == 'N':
                                    error = "pass"
                                    break
                                elif q == 'x' or q == 'q':
                                    error = "exit"
                                    break
                                else:
                                    break
                            
                            elif os.path.isfile(os.path.join(download_path, name + ".mp3")) and overwrite:
                                if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                                cls.re_tag(os.path.join(download_path, name + "." + fformat))
                                # cls.downloader(track_detail, name, fformat, download_path, track_formats.MP3_320, nmax)
                                if SLEEP and str(SLEEP).isdigit():
                                    sleeper.sleep(SL=int(SLEEP))
                                elif cls.config.get_config('download', 'sleep'):
                                    sleeper.sleep('download', 'sleep')
                            else:
                                debug("downloading ...")
                                if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                track_detail["download"](download_path, quality=track_formats.MP3_320, filename = name + "."+ fformat)
                                cls.re_tag(os.path.join(download_path, name + "." + fformat))
                                # cls.downloader(track_detail, name, fformat, download_path, track_formats.MP3_320, nmax)
                                if SLEEP and str(SLEEP).isdigit():
                                    sleeper.sleep(SL=int(SLEEP))
                                elif cls.config.get_config('download', 'sleep'):
                                    sleeper.sleep('download', 'sleep')
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
                            traceback.format_exc()
                        if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + "." + 'lrc')):
                            os.rename(os.path.join(download_path, tags_separated_by_comma['title'] + "." + 'lrc'), os.path.join(download_path, name + "."+ 'lrc'))
                            print(make_colors("RENAME:", 'lw', 'lr') + " " + make_colors(tags_separated_by_comma['title'] + "." + 'lrc', 'lw', 'bl') + ' --> ' + make_colors(name + "."+ 'lrc', 'b', 'lg'))
                        break
                    except:
                        traceback.format_exc()
            elif fformat == 'flac':
                while 1:
                    try:
                        if os.path.isfile(os.path.join(download_path, name + ".flac")) and dont_overwrite:
                            return True
                        elif os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".flac")) and dont_overwrite:
                            return True
                        else:
                            if os.path.isfile(os.path.join(download_path, tags_separated_by_comma['title'] + ".flac")) and not overwrite:
                                q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                                if q == 'y' or q == 'Y':
                                    if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                        cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                    track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                                    # cls.downloader(track_detail, name, fformat, download_path, track_formats.FLAC, nmax)
                                    if SLEEP and str(SLEEP).isdigit():
                                        sleeper.sleep(SL=int(SLEEP))
                                    elif cls.config.get_config('download', 'sleep'):
                                        sleeper.sleep('download', 'sleep')
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
                                    if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                        cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                    track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                                    # cls.downloader(track_detail, name, fformat, download_path, track_formats.FLAC, nmax)
                                    if SLEEP and str(SLEEP).isdigit():
                                        sleeper.sleep(SL=int(SLEEP))
                                    elif cls.config.get_config('download', 'sleep'):
                                        sleeper.sleep('download', 'sleep')
                                elif q == 'n' or q == 'N':
                                    error = "pass"
                                    break
                                elif q == 'x' or q == 'q':
                                    error = "exit"
                                    break
                                else:
                                    break
                            
                            elif os.path.isfile(os.path.join(download_path, name + ".flac")) and overwrite:
                                if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                                # cls.downloader(track_detail, name, fformat, download_path, track_formats.FLAC, nmax)
                                if SLEEP and str(SLEEP).isdigit():
                                    sleeper.sleep(SL=int(SLEEP))
                                elif cls.config.get_config('download', 'sleep'):
                                    sleeper.sleep('download', 'sleep')
                            else:
                                if cls.DOWNLOAD_INTO_SINGLE_FOLDER or cls.DOWNLOAD_INTO_ARTIST_FOLDER:
                                    cls.create_image(download_path, filename = os.path.join(download_path, name), id = album_id)
                                track_detail["download"](download_path, quality=track_formats.FLAC, filename = name + "."+ fformat)
                                # cls.downloader(track_detail, name, fformat, download_path, track_formats.FLAC, nmax)
                                if SLEEP and str(SLEEP).isdigit():
                                    sleeper.sleep(SL=int(SLEEP))
                                elif cls.config.get_config('download', 'sleep'):
                                    sleeper.sleep('download', 'sleep')

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
        cls.clean_config()
        return True
    
    @classmethod
    def print_config_help(cls, debugx = True, pausex = True):
        make_colors("[n]o")
        make_colors("[n]so")
        make_colors("[n]do")
        make_colors("[n]dso")
        make_colors("[n]vo")
        make_colors("[n]dvo")

        make_colors("[n]s")
        make_colors("[n]ds")
        make_colors("[n]ss")
        make_colors("[n]dss")

        make_colors("[n]O")
        make_colors("[n]sO")
        make_colors("[n]dO")
        make_colors("[n]dsO")
        make_colors("[n]vO")
        make_colors("[n]dvO")

        make_colors("[n]dsoa")
        make_colors("[n]dsOa")
        make_colors("[n]dsoA")
        make_colors("[n]dsOA")
        make_colors("[n]dvoa")
        make_colors("[n]dvOA")

    @classmethod
    def set_config(cls, q, debugx = True, pausex = True):
        import inspect
        q_number = q
        album_numbers = None

        def print_set_config(data):
            value = getattr(cls, data)
            if not value:
                value = make_colors(str(value), 'lw', 'bl')
            else:
                value = make_colors(str(value), 'lw', 'lr')
            print(make_colors(str(data), 'lw', 'bl') + " "* (40 - len(str(data))) + " = " + value)
        
        if q[-1:] == 'o':
            if q[-2:] == 'so':
                q_number = cls.split_number(q[:-2])
                if q_number or q == 'so':
                    cls.IS_SINGLE = True
                    cls.SHOW_SINGLE_ORIGINAL_ARTIST_ONLY = True

            elif q[-2:] == 'do':
                q_number = cls.split_number(q[:-2])
                if q_number or q == 'do':
                    cls.DOWNLOAD_ORIGINAL = True #download all album(official/single)

            elif q[-3:] == 'dso':
                q_number = cls.split_number(q[:-3])
                if q_number or q == 'dso':
                    cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY = True #download all single album only from original album artist only
                    cls.IS_SINGLE = True
            elif q[-2:] == 'vo':
                q_number = cls.split_number(q[:-2])
                if q_number or q == 'vo':
                    cls.SHOW_VARIOUS_ORIGINAL = True #show all various artist album only from original album artist only
                
            elif q[-3:] == 'dvo':
                q_number = cls.split_number(q[:-3])
                if q_number or q == 'dvo':
                    cls.DOWNLOAD_VARIOUS_ORIGINAL = True #show all various artist album only from original album artist only
                
            else:
                q_number = cls.split_number(q[:-1])
                if q_number or q == 'o':
                    cls.SHOW_ORIGINAL_ALBUM = True #show all album(official/single)
        
        elif q[-1:] == 'O':
            if q[-2:] == 'sO':
                cls.IS_SINGLE = True
                cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY = True
                q_number = cls.split_number(q[:-2])
            elif q[-2:] == 'dO':
                cls.DOWNLOAD_DISCOGRAPHY = True #download all album(official/single)
                q_number = cls.split_number(q[:-2])
            elif q[-3:] == 'dsO':
                cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = True #download all single album only from original album artist only
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-3])
            elif q[-2:] == 'vO':
                cls.SHOW_VARIOUS_DISCOGRAPHY = True #show all various artist album only from original album artist only
                q_number = cls.split_number(q[:-2])
            elif q[-3:] == 'dvO':
                cls.DOWNLOAD_VARIOUS_DISCOGRAPHY = True #show all various artist album only from original album artist only
                q_number = cls.split_number(q[:-3])
            else:
                cls.SHOW_DISCOGRAPHY = True #show all album(official/single)
                q_number = cls.split_number(q[:-1])

        elif q[-1:] == 's':
            if q == 's':
                cls.IS_SINGLE = True
                cls.SHOW_SINGLE_ORIGINAL_ARTIST_ONLY = True #show all album(official/single)
                q_number = cls.split_number(q[:-1])
            elif q[-2:] == 'ds':
                cls.IS_SINGLE = True
                cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY = True
                q_number = cls.split_number(q[:-2])
            elif q[-2:] == 'ss':
                cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY = True
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-2])
            elif q[-3:] == 'dss':
                cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = True
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-3])
            elif q == 'ss':
                cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY = True
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-2])
            else:
                cls.IS_SINGLE = True
                cls.SHOW_SINGLE_ORIGINAL_ARTIST_ONLY = True #show all album(official/single)
                q_number = cls.split_number(q[:-1])
        
        elif q[-1:] == 'a':
            if q[-3:] == 'dsa':
                cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY = True #download all single album only from original album artist only
                cls.DOWNLOAD_INTO_SINGLE_FOLDER = True #download all Single track into "SINGLE" folder only (auto create)
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-3])
            elif q[-4:] == 'dsoa':
                cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY = True #download all single album only from original album artist only
                cls.DOWNLOAD_INTO_SINGLE_FOLDER = True #download all Single track into "SINGLE" folder only (auto create)
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-4])
            elif q[-4:] == 'dvoa':
                cls.DOWNLOAD_VARIOUS_ORIGINAL = True #show all various artist album only from original album artist only
                cls.DOWNLOAD_INTO_SINGLE_FOLDER = True #download all Single track into Artist folder only (auto create)
                q_number = cls.split_number(q[:-4])
            elif q[-4:] == 'dsOa':
                cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = True #download all single album only from original album artist only
                cls.DOWNLOAD_INTO_SINGLE_FOLDER = True #download all Single track into "SINGLE" folder only (auto create)
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-4])
            elif q[-4:] == 'dvOa':
                cls.DOWNLOAD_VARIOUS_DISCOGRAPHY = True #show all various artist album only from original album artist only
                cls.DOWNLOAD_INTO_SINGLE_FOLDER = True #download all Single track into Artist folder only (auto create)
                q_number = cls.split_number(q[:-4])
            elif q == 'a':
                cls.DOWNLOAD_ALL = True
                q_number = cls.split_number(q[:-1])
        
        elif q[-1:] == 'A':
            if q[-4:] == 'dsoA':
                cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY = True #download all single album only from original album artist only
                cls.DOWNLOAD_INTO_ARTIST_FOLDER = True #download all Single track into "SINGLE" folder only (auto create)
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-4])
            elif q[-4:] == 'dvoA':
                cls.DOWNLOAD_VARIOUS_ORIGINAL = True #show all various artist album only from original album artist only
                cls.DOWNLOAD_INTO_ARTIST_FOLDER = True #download all Single track into Artist folder only (auto create)
                q_number = cls.split_number(q[:-4])
            elif q[-4:] == 'dsOA':
                cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = True #download all single album only from original album artist only
                cls.DOWNLOAD_INTO_ARTIST_FOLDER = True #download all Single track into "SINGLE" folder only (auto create)
                cls.IS_SINGLE = True
                q_number = cls.split_number(q[:-4])
            elif q[-4:] == 'dvOA':
                cls.DOWNLOAD_VARIOUS_DISCOGRAPHY = True #show all various artist album only from original album artist only
                cls.DOWNLOAD_INTO_ARTIST_FOLDER = True #download all Single track into Artist folder only (auto create)
                q_number = cls.split_number(q[:-4])
            elif q == 'A':
                cls.DOWNLOAD_ALL = True
                q_number = cls.split_number(q[:-1])
        
        elif q[-1:] == 'v':
            if q == 'v':
                cls.SHOW_VARIOUS_ORIGINAL = True #show all various artist album only from original album artist only
                q_number = cls.split_number(q[:-1])
            elif q[-2:] == 'dv':
                cls.DOWNLOAD_VARIOUS_ORIGINAL = True #download all album(official/single)
                cls.DOWNLOAD_VARIOUS_DISCOGRAPHY = True #download all album(official/single)
                q_number = cls.split_number(q[:-2])
        
        elif q[-1:] == 'd':
            q_number = cls.split_number(q[:-1])
            if q_number:
                cls.DIRECT_DOWNLOAD = True

        print_set_config("DOWNLOAD_ORIGINAL")
        print_set_config("DOWNLOAD_DISCOGRAPHY")
        print_set_config("DOWNLOAD_SINGLE_ORIGINAL_ONLY")
        print_set_config("DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY")
        print_set_config("DOWNLOAD_INTO_ARTIST_FOLDER")
        print_set_config("DOWNLOAD_INTO_SINGLE_FOLDER")
        print_set_config("DOWNLOAD_VARIOUS_ORIGINAL")
        print_set_config("DOWNLOAD_VARIOUS_DISCOGRAPHY")
        print_set_config("IS_SINGLE")
        print_set_config("SHOW_ORIGINAL_ALBUM")
        print_set_config("SHOW_DISCOGRAPHY")
        print_set_config("SHOW_SINGLE_ORIGINAL_ARTIST_ONLY")
        print_set_config("SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY")
        print_set_config("SHOW_VARIOUS_ORIGINAL")
        print_set_config("SHOW_VARIOUS_DISCOGRAPHY")
        print_set_config("DOWNLOAD_ALL")
        print_set_config("DIRECT_DOWNLOAD")
        debug(q_number = q_number, debug = debugx)
        if isinstance(q_number, list) and len(q_number) > 0:
            q_number = q_number[0]
        debug(q_number = q_number, debug = debugx)
        return q_number
            
    @classmethod
    def split_number(cls, x, debugx = True, pausex = True):
        numbers = []
        debug(x = x)
        if "-" in x:
            fr, to = x.split("-")
            fr = fr.strip()
            if str(to).isdigit():
                to = to.strip() + 1
            if str(fr).isdigit() and str(to).isdigit():
                return list(range(int(fr), int(to)))
            elif str(fr).isdigit() and not str(to).isdigit():
                numbers.append(int(fr))
            elif not str(fr).isdigit() and str(to).isdigit():
                numbers.append(int(to))
            return numbers
        elif "," in x:
            list_coma_numbers = x.split(",")
            for i in list_coma_numbers:
                if "-" in i:
                    fr, to = i.split("-")
                    fr = fr.strip()
                    if str(to).isdigit():
                        to = int(to.strip()) + 1
                    if str(fr).isdigit() and str(to).isdigit():
                        numbers += list(range(int(fr), int(to)))
                    elif str(fr).isdigit() and not str(to).isdigit():
                        numbers.append(int(fr))
                    elif not str(fr).isdigit() and str(to).isdigit():
                        numbers.append(int(to))
                else:
                    numbers.append(int(x.strip()))
            return list(set(numbers))
        else:
            if str(x).strip().isdigit():
                return [int(str(x).strip())]
        
        return numbers

    @classmethod
    def normalization_folder(cls, folder, debugx = True, pausex = True):
        folder = re.sub("\: ", " - ", folder)
        folder = re.sub("\?|\*", " ", folder)
        folder = re.sub("\:", "", folder)
        folder = re.sub("\.\.\.", "", folder)
        folder = re.sub("\.\.\.", "", folder)
        folder = re.sub(" / ", " - ", folder)
        folder = re.sub("/", "-", folder)
        folder = unidecode(folder)
        return folder

    @classmethod
    def clean_config(cls, debugx = True, pausex = True):
        cls.DOWNLOAD_ORIGINAL = False #download all album(official/single)
        cls.DOWNLOAD_DISCOGRAPHY = False #download all album(Discography)
        cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY = False #download all single album only from original album artist only
        cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = False #download all single album only from artit discography
        cls.DOWNLOAD_INTO_ARTIST_FOLDER = False #download all Single track into Artist folder only (auto create)
        cls.DOWNLOAD_INTO_SINGLE_FOLDER = False #download all Single track into "SINGLE" folder only (auto create)
        cls.DOWNLOAD_VARIOUS_ORIGINAL = False #show all various artist album only from original album artist only
        cls.DOWNLOAD_VARIOUS_DISCOGRAPHY = False #show all various artist album only from artit discography
        cls.IS_SINGLE = False

        cls.SHOW_ORIGINAL_ALBUM = False #show all album(official/single)
        cls.SHOW_DISCOGRAPHY = False #show all album(Discography)
        cls.SHOW_SINGLE_ORIGINAL_ARTIST_ONLY = False #show all single album only from original album artist only
        cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY = False #show all single album only from artit discography
        cls.SHOW_VARIOUS_ORIGINAL = False #show all various artist album only from original album artist only
        cls.SHOW_VARIOUS_DISCOGRAPHY = False #show all various artist album only from artit discography

        cls.DOWNLOAD_ALL = False

        cls.DOWNLOAD_PATH = os.getcwd()
        cls.FFORMAT = "mp3"
        cls.ORGARTIST = ''
        cls.FTYPE = 'artist'

    @classmethod
    def create_download_path(cls, id, download_path, is_single = False, original_artist = False, single_on_artist_folder = False, single_on_single_folder = False, debugx = True, pausex = True):
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

        if original_artist and single_on_artist_folder:
            download_path = os.path.join(download_path, original_artist)
        elif original_artist and single_on_single_folder:
            download_path = os.path.join(download_path, original_artist, "SINGLES")
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
            if is_single or cls.IS_SINGLE:
                download_path = os.path.join(download_path, "SINGLES")
            # folder_name = artist + " - " + album_detail.get('title') + " (" + str(release_year) + ")"
            folder_name = "(" + str(release_date) + ") " + album_detail.get('title')
            folder_name = cls.normalization_folder(folder_name)
            download_path = os.path.join(download_path, folder_name)

            if is_single and not cls.IS_SINGLE:
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
    def detect_input(cls, data_input, debugx = True, pausex = True):
        is_artist = False
        is_album = False
        data = None
        if str(data_input).isdigit():
            return data_input, False, False
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
    def create_image(cls, download_path, cover_data = None, filename = None, id = None, album_detail = None, debugx = True, pausex = True):
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
    def print_nav(cls, q = None, debugx = True, pausex = True):
        if not q:
            print(
                make_colors("n", 'b', 'lc') + "[" + make_colors("o", 'b', 'y') + make_colors("O", 'b', 'ly') + make_colors("d", 'b', 'lg') + make_colors("s", 'lw', 'bl') + make_colors("S", 'lw', 'lb') + make_colors("ss", 'lg', 'bl') + make_colors("a", 'lw', 'lr') + make_colors("A", 'lw', 'r') + make_colors("v", 'lw', 'm') + make_colors("V", 'lw', 'lm')
                )
            print(
                make_colors("n = Select discography of Artist", 'lr', 'lw') + ", " +\
                make_colors("a = Download all or download tracks into 'SINGLES' folder", 'lw', 'lg') + ", " +\
                make_colors("A = Download all or download tracks into artist folder", 'lr', 'ly') + ", " +\
                make_colors("s = Single of Artist Original or fro Discography", 'b', 'ly') + ", " +\
                make_colors("d = Download artists, albums, or tracks ", 'b', 'ly') + ", " +\
                make_colors("o = Select show Album of Artist Only", 'b', 'lc') + ", " +\
                make_colors("O = Select show Album of Artist Discography Only", 'b', 'lc') + ", " +\
                make_colors("v = Select show Appereance of Artist Original or from Discography", 'lw', 'm') + ", " +\
                make_colors("n1,nx,n1-nx = Download separated", 'lw', 'lr') + ", " +\
                make_colors("x|q|exit|quit = Exit/Quit", 'lr')
            )
                
            q = raw_input(make_colors("Select Number:", 'lw', 'bl') + " ")
        if q:
            q = str(q).strip()
        if q == 'x' or q == 'exit' or q == 'q' or q == 'quit':
            sys.exit(make_colors("Exit ...", 'lw', 'lr'))
        return q

    @classmethod
    def create_and_download(cls, disco, ORGARTIST, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, IS_SINGLE, fformat, overwrite, dont_overwrite, download_path, album_numbers = None, q = None, debugx = True, pausex = True):
        download_path0 = download_path
        debug(ORGARTIST = ORGARTIST)
        debug(album_numbers = album_numbers)
        DOWNLOAD_IS_SINGLE = False
        def download(id, ORGARTIST, DOWNLOAD_ORIGINAL, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, IS_SINGLE, fformat, overwrite, dont_overwrite, download_path, disco):
            while 1:
                try:
                    tracks = cls.deezer.get_album_tracks(id)
                    break
                except:
                    pass
            debug(len_tracks = len(tracks))    
            debug(ORGARTIST = ORGARTIST)
            # create_download_path(cls, id, download_path, is_single = False, original_artist = False, single_on_artist_folder = False, single_on_single_folder = False):
            download_path = cls.create_download_path(id, download_path, IS_SINGLE, ORGARTIST, INTO_ARTIST_FOLDER, INTO_SINGLE_FOLDER)
            debug(download_path = download_path)
            cls.download(tracks, None, fformat, download_path, overwrite, disco, DOWNLOAD_SINGLE_ONLY, dont_overwrite, INTO_ARTIST_FOLDER, INTO_SINGLE_FOLDER)
            return download_path

        if q:
            debug(q = q)
            q = int(q)
            id = disco[q - 1]['ALB_ID']
            download_path = download(id, ORGARTIST, DOWNLOAD_ORIGINAL, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE, disco[q - 1])
        else:
            if not album_numbers:
                for d in disco:
                    DOWNLOAD_IS_SINGLE = False
                    if int(d.get('TYPE')) == 0:
                        DOWNLOAD_IS_SINGLE = True

                    id = d.get('ALB_ID')
                    download_path1 = download(id, ORGARTIST, DOWNLOAD_ORIGINAL, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE, d)
                    if download_path1:
                        download_path0 = download_path1
                    
            else:
                for ds in album_numbers:
                    DOWNLOAD_IS_SINGLE = False
                    id = disco[int(ds) - 1].get('ALB_ID')
                    download_path1 = download(id, ORGARTIST, DOWNLOAD_ORIGINAL, INTO_SINGLE_FOLDER, INTO_ARTIST_FOLDER, DOWNLOAD_SINGLE_ONLY, fformat, overwrite, dont_overwrite, download_path, DOWNLOAD_IS_SINGLE, disco[int(ds) - 1])
                    if download_path1:
                        download_path0 = download_path1
        debug(ORGARTIST = ORGARTIST)    
        debug(INTO_ARTIST_FOLDER = INTO_ARTIST_FOLDER)
        debug(INTO_SINGLE_FOLDER = INTO_SINGLE_FOLDER)
        debug(download_path0 = download_path0)
        # pause(pausex)
        if ORGARTIST or INTO_ARTIST_FOLDER:
            cls.re_numbering_files(download_path0, ORGARTIST)
        # pause(pausex)

    @classmethod
    def check_config_artist(cls, ftype, artist_id = None, disco = None, artist_name = None, debugx = True, pausex = True):
        if cls.SHOW_ORIGINAL_ALBUM and ftype == 'artist' and artist_id:
            if not disco:
                disco1 = cls.deezer.get_artist(artist_id)
            else:
                disco1 = disco
            cls.SHOW_DISCOGRAPHY = False
            if not artist_name and artist_id:
                artist_name = disco1.get('DATA').get('ART_NAME')
            if cls.SHOW_SINGLE_ORIGINAL_ARTIST_ONLY and not cls.SHOW_VARIOUS_ORIGINAL:
                disco = cls.filter_disco(disco1.get('ALBUMS').get('data'), artist_name, True)
            elif cls.SHOW_VARIOUS_ORIGINAL and not cls.SHOW_SINGLE_ORIGINAL_ARTIST_ONLY:
                disco = cls.filter_disco(disco1.get('ALBUMS').get('data'), artist_name, False, True)
            else:
                if not disco:
                    disco = disco1.get('ALBUMS').get('data')

        elif cls.SHOW_DISCOGRAPHY and ftype == 'artist' and artist_id:
            if not disco:
                disco = cls.deezer.get_artist_discography(artist_id)
            cls.SHOW_ORIGINAL_ALBUM = False
            if not artist_name and artist_id:
                artist_name = cls.deezer.get_artist(artist_id).get('DATA').get('ART_NAME')
            if cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY and not cls.SHOW_VARIOUS_DISCOGRAPHY:
                disco = cls.filter_disco(disco, artist_name, True)
            elif cls.SHOW_VARIOUS_DISCOGRAPHY and not cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY:
                disco = cls.filter_disco(disco, artist_name, False, True)

        return disco

    @classmethod
    def filter_disco(cls, disco, artist_name = False, single = False, various = False, debugx = True, pausex = True):
        debug(len_disco = len(disco))
        debug(artist_name = artist_name)
        debug(single = single)
        debug(cls_IS_SINGLE = cls.IS_SINGLE)
        debug(various = various)
        disco_filter = []
        for ds in disco:
            # debug(ART_NAME = ds.get('ART_NAME'))
            # debug(artist_name = artist_name)
            if artist_name:
                if single or cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY or cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY:
                    if ds.get('TYPE') == '0' or ds.get('type') == '0' or ds.get('TYPE') == 0 or ds.get('type') == 0:
                        disco_filter.append(ds)
                else:
                    if ds.get('ART_NAME') == artist_name:
                        disco_filter.append(ds)
                    elif various or cls.SHOW_VARIOUS_ORIGINAL or cls.SHOW_VARIOUS_DISCOGRAPHY:
                        if ds.get('ART_NAME') != artist_name:
                            disco_filter.append(ds)
                    else:
                        disco_filter.append(ds)
            else:
                # debug(ds_get_TYPE = ds.get('TYPE'))
                # debug(ds_get_type = ds.get('type'))
                if single or cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY or cls.SHOW_SINGLE_DISCOGRAPHY_ARTIST_ONLY:
                    if ds.get('TYPE') == '0' or ds.get('type') == '0' or ds.get('TYPE') == 0 or ds.get('type') == 0:
                        disco_filter.append(ds)
                elif various or cls.SHOW_VARIOUS_DISCOGRAPHY or cls.SHOW_VARIOUS_ORIGINAL:
                    debug(ds_keys = ds.keys())
                    debug(ds_get_ARTISTS = ds.get('ARTISTS'))
                    debug(ds_get_ART_NAME = ds.get('ART_NAME'))
                    if "various artists" in ds.get('ART_NAME').lower():
                        disco_filter.append(ds)
                    else:
                        try:
                            if "various artists" in ds.get('artist').get('name').lower():
                                disco_filter.append(ds)
                        except:
                            pass
                    
        debug(len_disco_filter = len(disco_filter))
        # ORGARTIST = cls.ORGARTIST
        # cls.clean_config()
        # cls.ORGARTIST = ORGARTIST
        if disco_filter:
            return disco_filter
        else:
            return disco

    @classmethod
    def print_disco_album(cls, disco, ftype, print_list = True, orgartist = None, debugx = True, pausex = True):
        debug(cls_ORGARTIST = cls.ORGARTIST)
        pause(pausex)
        if orgartist:
            cls.ORGARTIST = orgartist
        artist_id = None
        debug(len_disco = len(disco))
        disco1 = []
        if ftype == 'album':
            for dc in disco:
                while 1:
                    try:
                        debug(dc_keys = dc.keys())
                        
                        album_detail = cls.deezer.get_album(dc['id'])
                        # debug(album_detail = album_detail)
                        # if cls.SHOW_ORIGINAL_ALBUM or cls.DOWNLOAD_ORIGINAL:
                        dc.update({'DIGITAL_RELEASE_DATE': album_detail['release_date']})
                        dc.update({'ALB_ID': dc['id']})
                        dc.update({'ART_NAME': dc['artist']['name']})                            
                        break
                    except:
                        traceback.format_exc()
            
                disco1.append(dc)
        if disco1:
            disco = disco1
        # debug(disco = disco)
        debug(len_disco = len(disco))
        pause(pausex)
        if not disco:
            return cls.download_interactive(cls.QUERY)
        # filter_disco(cls, disco, artist_name = False, single = False, various = False):
        disco = cls.filter_disco(disco)
        disco = sorted(disco, key = lambda k: k['DIGITAL_RELEASE_DATE'], reverse = True)
        # debug(disco = disco)
        debug(len_disco = len(disco))
        debug(d_keys = disco[0].keys())
        n = 1
        if print_list:
            print(make_colors("DISCOGRAPHY:", 'lw', 'g') + " ")
            for d in disco:
                debug(FTYPE = cls.FTYPE)
                debug(ARTIST = cls.ORGARTIST)
                if cls.FTYPE == 'album':
                    album_artist_name = d.get('artist').get('name')
                    artist_id = d.get('artist').get('id')
                elif cls.FTYPE == 'artist':
                    album_artist_name = d.get('name')
                    debug(album_artist_name = album_artist_name)
                    artist_id = d.get('id')
                    if not album_artist_name:
                        album_artist_name = d.get('ART_NAME')
                        artist_id = d.get('ART_ID')
                    debug(album_artist_name = album_artist_name)
                if not album_artist_name and cls.FTYPE == 'artist':
                    album_artist_name = d.get('ART_NAME')
                debug(album_artist_name_lower = album_artist_name.lower())
                debug(cls_ORGARTIST_lower = cls.ORGARTIST.lower())
                if album_artist_name.lower() == cls.ORGARTIST.lower():
                    album_artist_name = make_colors("{0} album".format(album_artist_name), 'lw', 'r')
                else:
                    album_artist_name = make_colors("{0} album".format(album_artist_name), 'lw', 'm')
                debug(TYPE = d.get('type'))
                IS_SINGLE = ""
                if int(d.get('TYPE')) == 0:
                    IS_SINGLE = " " + make_colors("[SINGLE]", 'b', 'lg')
                if d.get('title'):
                    print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('title'), 'lw', 'bl') + " / " + album_artist_name + IS_SINGLE + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                else:
                    print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('ALB_TITLE'), 'lw', 'bl') + " / " + album_artist_name + IS_SINGLE + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                n += 1
            notify('Deez', 'Deez', 'select_album', 'Ready to Select Album !', None, None, None, cls.LOGO, True, True, True, None, None, True)
        q = cls.print_nav(None)
        q = cls.set_config(q)
        debug(q = q)
        q, is_artist, is_album = cls.detect_input(q)
        debug(q = q)
        debug(is_artist = is_artist)
        debug(is_album = is_album)
        if is_artist:
            return cls.download_interactive(q, download_path, 'artist', fformat, None, True, overwrite, None, None, True, dont_overwrite)
        elif is_album:
            return cls.download_interactive(q, download_path, 'albums', fformat, None, True, overwrite, None, None, True, dont_overwrite)

        # disco_f = cls.check_config_artist(ftype, artist_id, disco, album_artist_name)
        disco_f = cls.filter_disco(disco)
        debug(len_disco = len(disco))
        debug(len_disco_f = len(disco_f))
        if not disco == disco_f:
            disco = disco_f
            pause(pausex)
            return cls.print_disco_album(disco, ftype, print_list)
        debug(cls_DOWNLOAD_SINGLE_ORIGINAL_ONLY = cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY, debug = True)
        debug(cls_DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY, debug = True)
        pause(pausex)
        return disco, q

    @classmethod
    def print_tracks(cls, album_id = None, disco = None, q = None, debugx = True, pausex = True):
        if not album_id and disco and q:
            album_id = disco[int(q) - 1].get('ALB_ID')
            
        while 1:
            try:
                tracks = cls.deezer.get_album_tracks(album_id)
                break
            except:
                pass
        nt = 1
        for track in tracks:
            if cls.FFORMAT == 'flac':
                print(make_colors(cls.format_number(str(nt), len(tracks)), 'lc') + " " + make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE_FLAC'))).MB)) + " mb", 'lw', 'm') + "]")
            else:
                print(make_colors(cls.format_number(str(nt), len(tracks)), 'lc') + " " + make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE'))).MB)) + " mb", 'lw', 'm') + "]")
                nt += 1
        
        q = cls.print_nav(None)
        if q:
            q = str(q).strip()
        
            # detect if input is like: "artist paul gilbert" or "album Rock legend"
            # q, is_artist, is_album = cls.detect_input(q)
            # if is_album and ftype == 'artist':
            #     return cls.search(q, 'album', print_list)
            # elif is_artist and ftype == 'album':
            #     return cls.search(q, 'artist', print_list)

            q, is_artist, is_album = cls.detect_input(q)
            if is_album and ftype == 'artist':
                return cls.download_interactive(q, cls.DOWNLOAD_PATH, 'album', cls.FFORMAT, True, cls.OVERWRITE, cls.DONT_OVERWRITE)
            elif is_artist and ftype == 'album':
                return cls.download_interactive(q, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, True, cls.OVERWRITE, cls.DONT_OVERWRITE)
            debug(q = q)
            pause(pausex)
            q = cls.set_config(q)
            debug(q = q)
            pause(pausex)
        else:
            return cls.download_interactive(cls.QUERY, cls.DOWNLOAD_PATH, cls.FTYPE, cls.FFORMAT, True, cls.OVERWRITE, cls.DONT_OVERWRITE)

        notify('Deez', 'Deez', 'ready to download album', 'Ready to Download Album !', None, None, None, cls.LOGO, True, True, True, None, None, True)
        return tracks, q

    @classmethod
    def search(cls, query, ftype = 'artist', print_list = True, q_search = None, result = None, orgartist = None, debugx = True, pausex = True):
        """Only search by artist|album|track
        
        :param query: text search for, default to None 
        :type query: str

        :param ftype: what you want to search, artistalbum|track
        :type ftype: str

        :param print_list: show list of result, default True
        :type print_list: bool

        :param q_search: direct select result number, default None
        :type q_search: int, optional

        :param result: bypass :class:`Deez.find` method for fast selt return, default None
        :type result: list return from this method of :class:`Deezer.search_artists`Object or :class:`Deezer.search_albums` Object or :class:`Deezer.search_tracks` Object, optional

        :param orgartist: Original Artist name, if not set (None) then will be set, default None
        :type orgartist: str, optional
        
        :return: A list of :class:`Deezer.get_artist` Object or :class:`Deezer.get_artist_discography` Object, ``orgartist``, :class:`Deezer.search_artists`Object or :class:`Deezer.search_albums` Object or :class:`Deezer.search_tracks` Object
        :rtype: list, dictionary view object and string
        """
        
        debug(query = query, debug = debugx)
        debug(q = q_search, debug = debugx)
        debug(print_list = print_list, debug = debugx)
        debug(orgartist = orgartist)
        debug(pausex = pausex)
        
        if q_search and str(q_search).isdigit():
            print_list = False
        
        pause(pausex)
        if orgartist:        
            cls.ORGARTIST = orgartist
        disco = None
        various = False
        
        if not result and query:
            result = cls.find(query, ftype)

        if ftype == 'artist' and result:
            if not cls.ORGARTIST:
                cls.ORGARTIST = query

        if not result:
            print(make_colors('Not Found !', 'lw', 'lr', ['blink']))
            # sys.exit()
            # return cls.download_interactive(query, cls.DOWNLOAD_PATH, ftype, cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
            EXIT = False
            q_search = cls.print_nav()
            q_search = cls.set_config(q_search)
            while 1:
                # detect if input is like: "artist paul gilbert" or "album Rock legend"
                q_search, is_artist, is_album = cls.detect_input(q_search)
                if is_album and ftype == 'artist':
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'album', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                elif is_artist and ftype == 'album':
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                elif is_artist and ftype == 'artist':
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                elif is_album and ftype == 'album':
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'album', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                
                elif q_search == 'x' or q_search == 'q':
                    EXIT = True
                    break
                else:
                    if q_search and not str(q_search).isdigit():
                        return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                    q_search = cls.print_nav()
                    if str(q_search).isdigit():
                        break

            if EXIT:
                STR_EXIT = make_colors("No ", 'lw', 'r') + make_colors("Artist", 'lw', 'bl') + " | " + make_colors("Albums", 'b', 'lg') + " | " + make_colors("Tracks", 'b', 'ly') + " | " + make_colors("Playlist", 'lw', 'm') + make_colors("Found !", 'lw', 'r')

                print(STR_EXIT)
                sys.exit(0)

        n = 1
        if print_list:
            for i in result:
                if ftype == 'artist':
                    print(cls.format_number(n, len(result)) +  ". " + make_colors(i.get('name'), 'lw', 'bl') + "[" + make_colors("{0} album".format(i.get('nb_album')), 'bl', 'y') + "]")
                elif ftype == 'album':
                    print(cls.format_number(n, len(result)) +  ". " + make_colors(i.get('title'), 'lw', 'bl') + "[" + make_colors(i.get('artist').get('name'), 'lw', 'm') + "/" + make_colors("{0} tracks".format(i.get('nb_tracks')), 'bl', 'y') + "]")
                n +=1
        q_search = cls.print_nav(q_search)
        EXIT = False
        while 1:
            # detect if input is like: "artist paul gilbert" or "album Rock legend"
            q_search, is_artist, is_album = cls.detect_input(q_search)
            q_search = cls.set_config(q_search)
            debug(q_search = q_search)
            debug(is_artist = is_artist)
            debug(is_album = is_album)
            if str(q_search).isdigit():
                break
            elif is_album and ftype == 'artist':
                return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'album', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
            elif is_artist and ftype == 'album':
                return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
            elif is_artist and ftype == 'artist':
                return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
            elif is_album and ftype == 'album':
                return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'album', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
            elif q_search == 'x' or q_search == 'q':
                EXIT = True
                break
            else:
                pause(pausex)
                if q_search and not str(q_search).isdigit():
                    cls.clean_config()
                    pause(pausex)
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                n = 1
                if print_list:
                    for i in result:
                        if ftype == 'artist':
                            print(cls.format_number(n, len(result)) +  ". " + make_colors(i.get('name'), 'lw', 'bl') + "[" + make_colors("{0} album".format(i.get('nb_album')), 'bl', 'ly') + "]")
                        elif ftype == 'album':
                            print(cls.format_number(n, len(result)) +  ". " + make_colors(i.get('title'), 'lw', 'bl') + "[" + make_colors(i.get('artist').get('name'), 'lw', 'm') + "/" + make_colors("{0} tracks".format(i.get('nb_tracks')), 'bl', 'ly') + "]")
                        n +=1
                q_search = cls.print_nav()
                q_search = cls.set_config(q_search)
                pause(pausex)
                if q_search and str(q_search).isdigit():
                    pause(pausex)
                    break
                else:
                    cls.clean_config()
                    pause(pausex)
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                
        if EXIT:
            sys.exit()
        debug(q = q_search)
        debug(ftype = ftype)
        pause(pausex)

        if q_search:
            q_search = str(q_search).strip()
            q_search = cls.set_config(q_search)
        debug(q = q_search)
        pause(pausex)
        if 'artist' in ftype and str(q_search).isdigit():
            id = result[int(q_search) - 1].get('id')
            debug(album_id = id)
            disco = cls.deezer.get_artist_discography(id)
        elif 'album' in ftype:
            disco = result
        elif 'track' in ftype:
            print(make_colors("Still Development ....", 'lw', 'lr'))
        elif 'playlist' in ftype:
            print(make_colors("Still Development ....", 'lw', 'lr'))
        
        if not disco:
            if query:
                return cls.search(query, ftype, print_list, q_search, result, orgartist)
            else:
                q_search = cls.print_nav()
                if q_search and not str(q_search).isdigit():
                    return cls.download_interactive(q_search, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                # def search(cls, query, ftype = 'artist', print_list = True, q_search = None, result = None, orgartist = None):
                return cls.search(None, ftype, print_list, None, result, orgartist)
        debug(len_disco = len(disco))
        disco = cls.filter_disco(disco)
        debug(len_disco = len(disco))
        debug(q_search = q_search)
        pause(pausex)
        # if not cls.ORGARTIST and (ftype == 'artist' or ftype == 'album'):
        if len(disco) == 1 and q_search:
            if str(q_search).isdigit():
                q_search = 1
        if str(q_search).isdigit() and ftype == 'artist':
            cls.ORGARTIST = disco[int(q_search) - 1 ]['ART_NAME']
            if not cls.ORGARTIST:
                try:
                    cls.ORGARTIST = disco[int(q_search) - 1]['name']
                except:
                    pass
        if str(q_search).isdigit() and ftype == 'albums':
            cls.ORGARTIST = disco[int(q_search) - 1]['artist']['name']

        debug(ORGARTIST = cls.ORGARTIST)
        cls.Q_SEARCH = q_search
        debug(q_search = q_search)
        pause(pausex)
        return disco, ftype

    @classmethod
    def download_interactive(cls, query, download_path = None, ftype='artist', fformat='mp3', print_list = True, overwrite = False, dont_overwrite = False, disco = None, artist = None, q = None, debugx = True, pausex = True):
        cls.clean_config()
        cls.QUERY = query
        cls.DOWNLOAD_PATH = download_path
        cls.FFORMAT = fformat
        cls.OVERWRITE = overwrite
        cls.DONT_OVERWRITE = dont_overwrite
        cls.ORGARTIST = artist
        cls.FTYPE = ftype

        debug(cls_ORGARTIST = cls.ORGARTIST)
        debug(pausex = pausex)
        pause(pausex)
        disco_selected = None

        if artist and ftype == 'artist':
            cls.ORGARTIST = artist
        elif ftype == 'artist':
            cls.ORGARTIST = query

        if not download_path:
            download_path = os.getcwd()

        download_path0 = download_path
        
        result = None
        
        if not disco:
            disco, _ = cls.search(query, ftype, print_list, q, debugx = False, pausex = False)
            debug(cls_ORGARTIST = cls.ORGARTIST, debug = debugx)
        if not disco:
            print(make_colors("No Discography Found !", 'lw', 'lr'))
            sys.exit(0)
        pause(pausex)
        disco_f = cls.filter_disco(disco)
        debug(cls_ORGARTIST = cls.ORGARTIST, debug = debugx)
        pause(pausex)
        debug(len_disco = len(disco))
        debug(len_disco_f = len(disco_f))
        if disco:
            disco, q = cls.print_disco_album(disco, ftype, print_list)
        if not len(disco_f) > 0:
            print(make_colors("No Discography SET Found !", 'lw', 'lr'))
            pause(pausex)
            return cls.download_interactive(query, download_path0, ftype, fformat, print_list, overwrite, dont_overwrite)
        debug(len_disco = len(disco))
        debug(len_disco_f = len(disco_f))
        pause(pausex)
        while 1:
            if len(disco) == len(disco_f):
                break
            else:
                debug(len_disco = len(disco))
                debug(len_disco_f = len(disco_f))
                disco, q = cls.print_disco_album(disco_f, ftype, print_list)
                disco_f = cls.filter_disco(disco)
                debug(len_disco = len(disco))
                debug(len_disco_f = len(disco_f))

        debug(len_disco = len(disco))
        debug(q = q)
        debug(cls_DOWNLOAD_SINGLE_ORIGINAL_ONLY = cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY, debug = True)
        debug(cls_DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY = cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY, debug = True)
        pause(pausex)
        if q and not str(q).isdigit():
            return cls.download_interactive(q, download_path0, ftype, fformat, print_list, overwrite, dont_overwrite)

        if q and str(q).isdigit() and int(q) <= len(disco):
            # disco_selected = disco[int(q) - 1]
            album_id = disco[int(q) - 1].get('ALB_ID')
            debug(album_id = album_id)
            debug(cls_ORGARTIST = cls.ORGARTIST)
            if not cls.ORGARTIST:
                cls.ORGARTIST = disco[int(q) - 1].get('ART_NAME')
            debug(cls_ORGARTIST = cls.ORGARTIST)
            if not album_id:
                album_id = disco[int(q) - 1].get('id')
            debug(album_id = album_id)
            debug(cls_DIRECT_DOWNLOAD = cls.DIRECT_DOWNLOAD)
            pause(pausex)
            if cls.DIRECT_DOWNLOAD or cls.DOWNLOAD_DISCOGRAPHY or cls.DOWNLOAD_ORIGINAL:
                while 1:
                    try:
                        tracks = cls.deezer.get_album_tracks(album_id)
                        break
                    except:
                        pass
                download_path = cls.create_download_path(album_id, download_path0, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                debug(download_path = download_path)
                pause(pausex)
                cls.download(tracks, None, fformat, download_path, overwrite, dont_overwrite)
            elif cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY or cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY:
                pause()
                if cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY:
                    disco = cls.filter_disco(disco, single = True)
                elif cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY:
                    disco = cls.filter_disco(disco, cls.ORGARTIST, single = True)
                debug(len_disco = len(disco))
                download_path = cls.create_download_path(album_id, download_path0, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                debug(download_path = download_path)        
                
                for ds in disco:
                    album_id = ds.get('ALB_ID')
                    while 1:
                        try:
                            tracks = cls.deezer.get_album_tracks(album_id)
                            break
                        except:
                            pass
                    if not cls.DOWNLOAD_INTO_ARTIST_FOLDER and not cls.DOWNLOAD_INTO_SINGLE_FOLDER:
                        download_path = cls.create_download_path(album_id, download_path0, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                        debug(download_path = download_path)
                        download_status = cls.download(tracks, None, fformat, download_path, overwrite, dont_overwrite)
                        debug(download_status = download_status)
            else:
                tracks, q = cls.print_tracks(album_id, disco, q)            
                debug(len_tracks = len(tracks))
                debug(q = q)
                pause(pausex)
                if q and q.isdigit() and tracks and int(q) <= len(tracks):
                    download_path = cls.create_download_path(album_id, download_path, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                    debug(download_path = download_path)
                    pause(pausex)
                    download_status = cls.download(tracks, [int(q)], fformat, download_path, overwrite, dont_overwrite)
                    debug(download_status = download_status)
                    pause(pausex)
                    if download_status == "pass":
                        return cls.download_interactive(query, download_path0, ftype, fformat, print_list, overwrite, dont_overwrite)
                    
                elif cls.DOWNLOAD_ALL:
                    download_path = cls.create_download_path(album_id, download_path, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                    debug(download_path = download_path)
                    pause(pausex)
                    cls.download(tracks, None, fformat, download_path, overwrite, dont_overwrite)

                elif q and ("-" in q or "," in q) and tracks:
                    if "," in q:
                        track_number_1 = re.split(",", q2)
                        debug(track_number_1 = track_number_1)
                        track_number_1 = list(filter(None, track_number_1))
                        debug(track_number_1 = track_number_1)
                        for i in track_number_1:
                            if "-" in i:
                                track_number, _ = cls.split_number(i)
                                cls.download(tracks, track_number, fformat, download_path, overwrite, dont_overwrite)
                            else:
                                cls.download(tracks, [i], fformat, download_path, overwrite, dont_overwrite)
                    elif "-" in q2:
                        track_number, _ = cls.split_number(q2)
                        debug(track_number = track_number)
                        cls.download(tracks, track_number, fformat, download_path, overwrite, dont_overwrite)

                    else:
                        pass
                    
                    notify('Deez', 'Deez', 'finish', 'All Download Finished !', None, None, None, cls.LOGO, True, True, True, None, None, True)

                elif q and not q.isdigit():
                    return cls.download_interactive(q, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
                else:
                    return cls.download_interactive(query, cls.DOWNLOAD_PATH, 'artist', cls.FFORMAT, print_list, cls.OVERWRITE, cls.DONT_OVERWRITE)
        
        elif (cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY or cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY) and disco:

            if (cls.DOWNLOAD_INTO_ARTIST_FOLDER or cls.DOWNLOAD_INTO_SINGLE_FOLDER) and (cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY or cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY):
                pause()
                if cls.IS_SINGLE:
                    if cls.DOWNLOAD_SINGLE_DISCOGRAPHY_ONLY:
                        disco = cls.filter_disco(disco, single = True)
                    elif cls.DOWNLOAD_SINGLE_ORIGINAL_ONLY:
                        disco = cls.filter_disco(disco, cls.ORGARTIST, single = True)
                    debug(len_disco = len(disco))
                    pause()
                    single_tracks_0 = []
                    single_tracks = []
                    for ds in disco:
                        print("ALBUM_TYPE :", ds.get("TYPE"))
                        print("ARTIST NAME:", ds.get("ART_NAME"))
                    for ds in disco:
                        album_id = ds.get('ALB_ID')
                        debug(album_id = album_id)
                        while 1:
                            try:
                                tracks = cls.deezer.get_album_tracks(album_id)
                                break
                            except:
                                pass
                        for tr in tracks:
                            single_tracks_0.append(tr)

                    for s in range(1, len(single_tracks_0) + 1):
                        single_tracks.append(single_tracks_0[len(single_tracks_0) - s])

                    download_path = cls.create_download_path(album_id, download_path0, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                    debug(download_path = download_path)        
                    debug(download_path = download_path)
                    pause()

                    download_status = cls.download(single_tracks, None, fformat, download_path, overwrite, dont_overwrite, True)
                    debug(download_status = download_status)
                    pause()
                else:
                    download_path = cls.create_download_path(album_id, download_path0, cls.IS_SINGLE, cls.ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                    debug(download_path = download_path)        
                    debug(download_path = download_path)
                    pause()

                    for ds in disco:
                        album_id = ds.get('ALB_ID')
                        debug(album_id = album_id)
                        while 1:
                            try:
                                tracks = cls.deezer.get_album_tracks(album_id)
                                break
                            except:
                                pass
                        download_status = cls.download(tracks, None, fformat, download_path, overwrite, dont_overwrite)
                        debug(download_status = download_status)
                    pause()

                        
        elif q and ("-" in q or "," in q) and disco:
            if "," in q:
                track_number = re.split(",", q2)
                debug(track_number = track_number)
                track_number = list(filter(None, track_number))
                debug(track_number = track_number)
                for i in track_number:
                    if "-" in i:
                        track_number_1, _ = cls.split_number(i)
                        for it in track_number_1:
                            album_id = disco[int(it) - 1].get('ALB_ID')
                            while 1:
                                try:
                                    tracks = cls.deezer.get_album_tracks(album_id)
                                    break
                                except:
                                    pass
                            download_path = cls.create_download_path(album_id, download_path, cls.IS_SINGLE, ORGARTIST, cls.DOWNLOAD_INTO_ARTIST_FOLDER, cls.DOWNLOAD_INTO_SINGLE_FOLDER)
                            cls.download(tracks, None, fformat, download_path, overwrite, dont_overwrite)
                        
                    else:
                        album_id = disco[int(i) - 1].get('ALB_ID')
                        while 1:
                            try:
                                tracks = cls.deezer.get_album_tracks(album_id)
                                break
                            except:
                                pass
                        cls.download(tracks, track_number, fformat, download_path, overwrite, dont_overwrite)

            elif "-" in q2:
                track_number, _ = cls.split_number(q2)
                debug(track_number = track_number)
                album_id = disco[int(i) - 1].get('ALB_ID')
                while 1:
                    try:
                        tracks = cls.deezer.get_album_tracks(album_id)
                        break
                    except:
                        pass
                cls.download(tracks, track_number, fformat, download_path, overwrite, dont_overwrite)

            
            notify('Deez', 'Deez', 'finish', 'All Download Finished !', None, None, None, cls.LOGO, True, True, True, None, None, True)

        # else:
        debug(q = q)
        query = cls.print_nav(q)
        debug(query = query)
        query, is_artist, is_album = cls.detect_input(query)
        pause(pausex)
        if is_album and ftype == 'artist':
            return cls.download_interactive(query, download_path0, 'album', fformat, print_list, overwrite, dont_overwrite)
        elif is_artist and ftype == 'album':
            return cls.download_interactive(query, download_path0, 'artist', fformat, print_list, overwrite, dont_overwrite)
        elif is_artist and ftype == 'artist':
            return cls.download_interactive(query, download_path0, 'artist', fformat, print_list, overwrite, dont_overwrite)
        elif is_album and ftype == 'album':
            return cls.download_interactive(query, download_path0, 'album', fformat, print_list, overwrite, dont_overwrite)
        elif query == 'x' or query == 'q':
            print(make_colors("Exit ... !", 'lw', 'lr'))
            sys.exit()
        debug(query = query)
        debug(is_artist = is_artist)
        debug(is_album = is_album)
        pause(pausex)
        if not str(query).isdigit() and query:
            pause(pausex)
            return cls.download_interactive(query, download_path0, ftype, fformat, True, overwrite, dont_overwrite)
        if disco:
            pause(pausex)
            return cls.download_interactive(cls.QUERY, download_path0, ftype, fformat, True, overwrite, dont_overwrite, disco)        
        else:
            pause(pausex)
            return cls.download_interactive(cls.QUERY, download_path0, ftype, fformat, True, overwrite, dont_overwrite, None, None, q)

    @classmethod
    def usage(cls, debugx = True, pausex = True):
        parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
        parser.add_argument('query', action = 'store', help = 'Search For Artist')
        parser.add_argument('-s', '--search-for', action = 'store', help = 'artist (default) | album', default = 'artist')
        parser.add_argument('-p', '--download-path', action = 'store', help = 'Save download to')
        parser.add_argument('-t', '--type', action = 'store', help = 'mp3 or flac, default = mp3', default = 'mp3')
        parser.add_argument('-o', '--overwrite', action = 'store_true', help = "Overwrite if file exists")
        parser.add_argument('-no', '--dont-overwrite', action = 'store_true', help = "Dont Overwrite if file exists")
        parser.add_argument('--sleep', action = 'store', help = 'sleep every after download, value is seconds')
        if len(sys.argv) == 1:
            print("\n")
            parser.print_help()
        else:
            args = parser.parse_args()
            if args.sleep:
                cls.config.write_config('download', 'sleep', str(args.sleep))
            if cls.config.get_config('download', 'path', os.getcwd()):
                download_path = cls.config.get_config('download', 'path')
            if args.download_path:
                download_path = args.download_path
            cls.download_interactive(args.query, download_path, args.search_for, args.type, overwrite = args.overwrite, dont_overwrite = args.dont_overwrite)
            
def usage():
    Deez.usage()
        
if __name__ == '__main__':    
    #Deez.download_interactive(sys.argv[1])
    Deez.usage()
    #print(Deez.format_number(sys.argv[1]))

    