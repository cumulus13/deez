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
    def format_number(cls, number, length = 100):
        number = str(number).strip()
        zeros = len(str(length)) - len(number)
        r = ("0" * zeros) + str(number)
        if len(r) == 1:
            return "0" + r
        return r

    @classmethod
    def download(cls, tracks, numbers = None, fformat = 'mp3', download_path = None, overwrite = False):
        # os.environ.update({'DEBUG':'1'})
        error = False
        download_path0 = download_path
        if not os.path.isdir(download_path):
            os.makedirs(download_path)
        print(make_colors("SAVE TO", 'lw', 'bl') + ": " + make_colors(download_path, 'lw', 'm'))
        if not numbers:
            numbers = list(range(len(tracks) + 1))[1:]
            debug(numbers = numbers)
            
        for i in numbers:
            debug(i = i)
            try:
                int(i)
            except:
                return False
            track_id = tracks[int(i) - 1].get('SNG_ID')
            debug(track_id = track_id)
            # track_detail = None
            # pause()
            while 1:
                try:
                    track_detail = cls.deezer.get_track(track_id)
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

                
            name = cls.format_number(tracks[int(i) - 1].get('TRACK_NUMBER'), len(tracks)) + ". " + tracks[int(i) - 1].get('SNG_TITLE')# + ".mp3"
            track_detail.get('info').get('DATA').update({'SNG_TITLE': name})
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
                        if os.path.isfile(os.path.join(download_path, name + ".mp3")) and not overwrite:
                            q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                            if q == 'y' or q == 'Y':
                                track_detail["download"](download_path, quality=track_formats.MP3_320)
                            elif q == 'n' or q == 'N':
                                error = "pass"
                                break
                            elif q == 'x' or q == 'q':
                                error = "exit"
                                break
                            else:
                                break
                        elif os.path.isfile(os.path.join(download_path, name + ".mp3")) and overwrite:
                            track_detail["download"](download_path, quality=track_formats.MP3_320)
                        else:
                            track_detail["download"](download_path, quality=track_formats.MP3_320)
                        break
                    except:
                        pass
            elif fformat == 'flac':
                while 1:
                    try:
                        if os.path.isfile(os.path.join(download_path, name + ".flac")) and not overwrite:
                            q = raw_input(make_colors("FILE EXISTS, OVERWRITE [y/n/x/q]:", 'lw', 'lr') + " ")
                            if q == 'y' or q == 'Y':
                                track_detail["download"](download_path, quality=track_formats.FLAC)
                            elif q == 'n' or q == 'N':
                                error = "pass"
                                break
                            elif q == 'x' or q == 'q':
                                error = "exit"
                                break
                            else:
                                break
                        elif os.path.isfile(os.path.join(download_path, name + ".flac")) and overwrite:
                            track_detail["download"](download_path, quality=track_formats.FLAC)
                        else:
                            track_detail["download"](download_path, quality=track_formats.FLAC)
                        break
                    except:
                        pass
        if error == "pass":
            return error
        elif error == "exit":
            sys.exit()
        return True

    @classmethod
    def split_number(cls, x):
        debug(x = x)
        fr, to = x.split("-")
        fr = fr.strip()
        to = to.strip()
        track_number = list(range(int(fr), int(to)+1))
        return track_number

    @classmethod
    def create_download_path(cls, id, download_path, is_single = False):
        cover_name = 'Cover'
        poster_name = 'Poster'
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
        while 1:
            try:
                artist_picture_data = cls.deezer.get_artist_poster(cls.deezer.get_artist(artist_data.get('id')), 1000)
                break
            except:
                pass
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
        folder_name = re.sub("\: ", " - ", folder_name)
        folder_name = re.sub("\?|\*", " ", folder_name)
        folder_name = re.sub("\:", "", folder_name)
        folder_name = re.sub("\.\.\.", "", folder_name)
        download_path = os.path.join(download_path, folder_name)

        if is_single:
            download_path += " [single]"
        
        if not os.path.isdir(download_path):
            try:
                os.makedirs(download_path)
            except:
                pass
            
        cover = cover_name + "." + cover_data.get('ext')
        cover = os.path.join(download_path, cover)
        poster = poster_name + "." + cover_data.get('ext')
        poster = os.path.join(download_path, poster)
        artist_pic = "Artist" + "." + artist_picture_data.get('ext')
        artist_pic = os.path.join(download_path, artist_pic)
        #print("Cover      =", cover)
        #print("Artist Pic =", artist_pic)
        
        with open(u"{}".format(cover), 'wb') as cover_file:
            cover_file.write(cover_data.get('image'))
        with open(u"{}".format(poster), 'wb') as poster_file:
            poster_file.write(cover_data.get('image'))
        with open(u"{}".format(artist_pic), 'wb') as artist_pic_file:
            artist_pic_file.write(artist_picture_data.get('image'))

        return download_path

    @classmethod
    def print_nav(cls, q, default = "Select Number:", ntype = 1):
        if not q:
            if ntype == 1:
                print(
                    make_colors("n = Select discography of Artist", 'b', 'lw') + ", " +\
                    make_colors("[n]a = Select show Album with Appereance of Artist Only", 'b', 'lg') + ", " +\
                    make_colors("[n]o = Select show Album of Artist Only", 'b', 'lc') + ", " +\
                    make_colors("[n]s = Select show Single of Artist Only", 'b', 'ly') + ", " +\
                    make_colors("[n]S = Select show Single of Artist Only from Discography", 'b', 'ly') + ", " +\
                    make_colors("[n]v = Select show Appereance of Artist Only", 'lw', 'm') + ", " +\
                    make_colors("[n]V = Select show Appereance of Artist from Discography", 'lw', 'm') + ", " +\
                    make_colors("x|q|exit|quit = Exit/Quit", 'lr')
                )
            elif ntype == 2:
                print(
                    make_colors("n = Select album number to download", 'b', 'lw') + ", " +\
                    make_colors("a = Download All Albums ", 'lw', 'lr') + ", " +\
                    make_colors("aa = Select show Album with Appereance of Artist", 'b', 'lg') + ", " +\
                    make_colors("A = Select show Album with Appereance of Artist from Discography", 'lr', 'ly') + ", " +\
                    make_colors("o = Select show Album of Artist Only", 'b', 'lc') + ", " +\
                    make_colors("s = Select show Single of Artist Only", 'b', 'ly') + ", " +\
                    make_colors("S = Select show Single of Artist Only from Discography", 'b', 'ly') + ", " +\
                    make_colors("v = Select show Appereance of Artist Only", 'lw', 'm') + ", " +\
                    make_colors("V = Select show Appereance of Artist from Discography", 'lw', 'm') + ", " +\
                    make_colors("x|q|exit|quit = Exit/Quit", 'lr')
                )

            elif ntype == 3:
                print(
                    make_colors("n = Select track number to download", 'b', 'lw') + ", " +\
                    make_colors("a = Download All tracks ", 'lw', 'lr') + ", " +\
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
    def download_interactive(cls, query, download_path = None, ftype='artist', fformat='mp3', q = None, print_list_artist = True, overwrite = False, q1 = None, q2 = None, print_list_album = True):
        if print_list_artist:
            q = None
        result = cls.find(query, ftype)
        
        just_artist = False
        just_artist_disco = False
        just_origin = False
        just_singles = False
        just_single_disco = False
        just_others = False
        just_other_disco = False

        ARTIST_ORIGIN = []
        if not download_path:
            download_path = os.getcwd()
        download_path0 = download_path
        debug(q = q)
        if result:
            n = 1
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
            
            if q[-1] == 'o':
                just_origin = True
                q = q[:-1]
            elif q[-1] == 'a' or q[-2:] == 'aa':
                just_artist = True
                if q[-2:] == 'aa':
                    q = q[:-2]    
                else:
                    q = q[:-1]
            elif q[-1] == 'A':
                just_artist_disco = True
                q = q[:-1]
            elif q[-1] == 's':
                just_singles = True
                q = q[:-1]
            elif q[-1] == 'S':
                just_single_disco = True
                q = q[:-1]
            elif q[-1] == 'v':
                just_others = True
                q = q[:-1]
            elif q[-1] == 'V':
                just_other_disco = True
                q = q[:-1]

            debug(q = q)
            if q and q.isdigit():
                debug(q = q)
                debug(len_result = len(result))
                debug(just_singles = just_singles)
                if int(q) <= len(result):
                    debug(q = q)
                    n = 1
                    id = result[int(q) - 1].get('id')
                    artist_name = result[int(q) - 1].get('name')
                    debug(id = id)
                    #id = 81238
                    while 1:
                        try:
                            if not just_artist and not just_origin and not just_singles and not just_others:
                                disco = cls.deezer.get_artist_discography(id)
                                if just_artist_disco:
                                    disco_t = disco
                                    disco = []
                                    for p in disco_t:
                                        if p.get('ART_NAME') == artist_name:
                                            disco.append(p)
                                elif just_single_disco:
                                    disco_t = disco
                                    disco = []
                                    for p in disco_t:
                                        if p.get('TYPE') == '0' or p.get('TYPE') == 0:
                                            disco.append(p)
                                elif just_other_disco:
                                    disco_t = disco
                                    disco = []
                                    for p in disco_t:
                                        if not p.get('TYPE') == '0' or not p.get('TYPE') == 0 or not p.get('ART_NAME') == artist_name:
                                            disco.append(p)
                            else:
                                disco = cls.deezer.get_artist(id)['ALBUMS']['data']
                                if just_origin:
                                    disco_t = disco
                                    disco = []
                                    for p in disco_t:
                                        if p.get('ART_NAME') == artist_name:
                                            disco.append(p)
                                elif just_singles:
                                    print("x"*100)
                                    disco_t = disco
                                    debug(len_disco_t = len(disco_t))
                                    disco = []
                                    for p in disco_t:
                                        if p.get('TYPE') == '0' or p.get('TYPE') == 0:
                                            disco.append(p)
                                    debug(len_disco = len(disco))
                                elif just_others:
                                    disco_t = disco
                                    disco = []
                                    for p in disco_t:
                                        if not p.get('TYPE') == '0' or not p.get('TYPE') == 0 or not p.get('ART_NAME') == artist_name:
                                            disco.append(p)
                                
                            break
                        except:
                            traceback.format_exc()
                    just_artist = False
                    just_artist_disco = False
                    just_origin = False
                    just_singles = False
                    just_single_disco = False
                    just_others = False
                    just_other_disco = False
                    debug(disco = disco)
                    if not disco:
                        return cls.download_interactive(query, download_path, ftype, fformat)
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
                            if d.get('TYPE') == '0' or d.get('TYPE') == 0:
                                IS_SINGLE = " " + make_colors("[SINGLE]", 'b', 'lg')
                            else:
                                IS_SINGLE = ""
                            print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('ALB_TITLE'), 'lw', 'bl') + " / " + album_artist_name + IS_SINGLE + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                            n += 1
                        notify('Deez', 'Deez', 'ready to select album', 'Ready to Select Album !', icon=cls.LOGO, direct_run = True)
                    # q1 = raw_input(make_colors("Select Number:", 'lw', 'm') + " ")
                    if not q1:
                        q1 = cls.print_nav(None, "Select Number:", 2)
                    debug(q1 = q1)
                    if q1:
                        q1 = str(q1).strip()
                    if q1 == 'q' or q1 == 'x':
                        sys.exit()

                    if q1 and q1.isdigit():
                        DOWNLOAD_IS_SINGLE = False
                        if int(q1) <= len(disco):
                            n = 1
                            id = disco[int(q1) - 1].get('ALB_ID')
                            if disco[int(q1) - 1].get('TYPE') == '0' or disco[int(q1) - 1].get('TYPE') == 0:
                                DOWNLOAD_IS_SINGLE = True
                            while 1:
                                try:
                                    tracks = cls.deezer.get_album_tracks(id)
                                    break
                                except:
                                    pass
                            nt = 1
                            for track in tracks:
                                if fformat == 'flac':
                                    print(make_colors(cls.format_number(str(nt), len(tracks)), 'lc') + " " + make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE_FLAC'))).MB)) + " mb", 'lw', 'm') + "]")
                                else:
                                    print(make_colors(cls.format_number(str(nt), len(tracks)), 'lc') + " " + make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE'))).MB)) + " mb", 'lw', 'm') + "]")
                                    nt += 1
                        notify('Deez', 'Deez', 'ready to download album', 'Ready to Download Album !', icon=cls.LOGO, direct_run = True)
                        debug(tracks = tracks)
                        if not q2:
                            q2 = cls.print_nav(None, "Select Number to download: ", 2)
                        # q2 = raw_input(make_colors("Select Number to download [a/all = download all]:", 'lw', 'm') + " ")
                        debug(q2 = q2)
                        if q2:
                            download_path = cls.create_download_path(id, download_path, DOWNLOAD_IS_SINGLE)
                        if q2 and q2 == 'all' or q2 == 'a':
                            cls.download(tracks, fformat = fformat, download_path = download_path, overwrite = overwrite)

                        elif "-" in q2 or "," in q2:
                            if "," in q2:
                                track_number_1 = re.split(",", q2)
                                debug(track_number_1 = track_number_1)
                                track_number_1 = list(filter(None, track_number_1))
                                debug(track_number_1 = track_number_1)
                                for i in track_number_1:
                                    if "-" in i:
                                        track_number = cls.split_number(i)
                                        cls.download(tracks, track_number, fformat, download_path, overwrite = overwrite)
                                    else:
                                        cls.download(tracks, [i], fformat, download_path, overwrite = overwrite)
                            elif "-" in q2:
                                track_number = cls.split_number(q2)
                                debug(track_number = track_number)
                                cls.download(tracks, track_number, fformat, download_path, overwrite = overwrite)

                        else:
                            # track_id = tracks[int(q2) - 1].get('SNG_ID')
                            debug(q2 = q2)
                            if q2 and str(q2).isdigit():
                                download_status = cls.download(tracks, [int(q2)], fformat, download_path, overwrite = overwrite)
                                if download_status == "pass":
                                    return cls.download_interactive(query, download_path0, ftype, fformat, q, False, overwrite, q1, q2, False)
                            else:
                                if q2:
                                    if q1 == 'aa' or q1 == 'A' or q1 == 'o' or q1 == 's' or q1 == 'S' or q1 == 'v' or q1 == 'V': 
                                        return cls.download_interactive(query, download_path0, ftype, fformat, q1 + q2, False)        
                                    else:
                                        return cls.download_interactive(q2, download_path0, ftype, fformat, None)        

                                # else:
                                    return cls.download_interactive(query, download_path0, ftype, fformat, None)

                        notify('Deez', 'Deez', 'finish', 'All Download Finished !', icon=cls.LOGO, direct_run = True)

                    elif q1 and q1 == 'all' or q1 == 'a':
                        for ds in disco:
                            DOWNLOAD_IS_SINGLE = False
                            id = ds.get('ALB_ID')
                            if ds.get('TYPE') == '0' or ds.get('TYPE') == 0:
                                DOWNLOAD_IS_SINGLE = True
                            while 1:
                                try:
                                    tracks = cls.deezer.get_album_tracks(id)
                                    break
                                except:
                                    pass
                            download_path = cls.create_download_path(id, download_path0, DOWNLOAD_IS_SINGLE)
                            cls.download(tracks, fformat = fformat, download_path = download_path, overwrite = overwrite)

                    elif "-" in q1 or "," in q1:
                        if "," in q1:
                            album_numbers = re.split(",", q1)
                            debug(album_numbers = album_numbers)
                            album_numbers = list(filter(None, album_numbers))
                            debug(album_numbers = album_numbers)
                            for ds in album_numbers:
                                DOWNLOAD_IS_SINGLE = False
                                if "-" in ds:
                                    album_numbers1 = cls.split_number(ds)
                                    debug(album_numbers = album_numbers1)
                                    for dss in album_numbers1:
                                        id1 = disco[int(dss) - 1].get('ALB_ID')
                                        if disco[int(dss) - 1] == '0' or disco[int(dss) - 1] == 0:
                                            DOWNLOAD_IS_SINGLE = True    
                                        while 1:
                                            try:
                                                tracks = cls.deezer.get_album_tracks(id1)
                                                break
                                            except:
                                                pass
                                        download_path = cls.create_download_path(id1, download_path0, DOWNLOAD_IS_SINGLE)
                                        cls.download(tracks, fformat = fformat, download_path = download_path, download = download)                                
                                else:
                                    DOWNLOAD_IS_SINGLE = False
                                    id = disco[int(ds) - 1].get('ALB_ID')
                                    if disco[int(ds) - 1] == '0' or disco[int(ds) - 1] == 0:
                                        DOWNLOAD_IS_SINGLE = True    
                                    while 1:
                                        try:
                                            tracks = cls.deezer.get_album_tracks(id)
                                            break
                                        except:
                                            pass
                                    download_path = cls.create_download_path(id, download_path0, DOWNLOAD_IS_SINGLE)
                                    cls.download(tracks, fformat = fformat, download_path = download_path, download = download)                                
                        elif "-" in q1:
                            album_numbers = cls.split_number(q1)
                            debug(album_numbers = album_numbers)
                            for ds in album_numbers:
                                DOWNLOAD_IS_SINGLE = False
                                id = disco[int(ds) - 1].get('ALB_ID')
                                if disco[int(ds) - 1] == '0' or disco[int(ds) - 1] == 0:
                                    DOWNLOAD_IS_SINGLE = True    
                                while 1:
                                    try:
                                        tracks = cls.deezer.get_album_tracks(id)
                                        break
                                    except:
                                        pass
                                download_path = cls.create_download_path(id, download_path0, DOWNLOAD_IS_SINGLE)
                                cls.download(tracks, fformat = fformat, download_path = download_path, download = download)                                
                    else:
                        debug(q = q)
                        debug(q1 = q1)
                        if q1:
                            if q1 == 'aa' or q1 == 'A' or q1 == 'o' or q1 == 's' or q1 == 'S' or q1 == 'v' or q1 == 'V': 
                                return cls.download_interactive(query, download_path0, ftype, fformat, q + q1, False)
                            else:
                                return cls.download_interactive(q1, download_path0, ftype, fformat, None)
                        else:
                            return cls.download_interactive(query, download_path0, ftype, fformat, None)
            
            else:
                debug(q = q)
                if q == 'aa' or q == 'A' or q == 'o' or q == 's' or q == 'S' or q == 'v' or q == 'V': 
                    return cls.download_interactive(query, download_path0, ftype, fformat, q, False)        
                else:
                    if not q:
                        return cls.download_interactive(query, download_path0, ftype, fformat, None, True)
                    else:        
                        return cls.download_interactive(q, download_path0, ftype, fformat, None, True)        
        else:
            print(make_colors('Not Found !', 'lw', 'lr', ['blink']))
            sys.exit()
        return cls.download_interactive(query, download_path0, ftype, fformat)

    @classmethod
    def usage(cls):
        parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
        parser.add_argument('query', action = 'store', help = 'Search For Artist')
        parser.add_argument('-p', '--download-path', action = 'store', help = 'Save download to')
        parser.add_argument('-t', '--type', action = 'store', help = 'mp3 or flac, default = mp3', default = 'mp3')
        parser.add_argument('-o', '--overwrite', action = 'store_true', help = "Overwrite if file exists")
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            cls.download_interactive(args.query, args.download_path, fformat = args.type, overwrite = args.overwrite)
            
def usage():
    Deez.usage()
        
if __name__ == '__main__':    
    #Deez.download_interactive(sys.argv[1])
    Deez.usage()
    #print(Deez.format_number(sys.argv[1]))

    