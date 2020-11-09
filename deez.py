#!d:/virtualenv/py-deezer/Scripts/python.exe

from __future__ import print_function

from pydeezer import Deezer
from pydeezer.constants import track_formats
import os
import sys
import re
if sys.platform == 'win32':
    import win32api, win32con, win32gui, win32console
    from dcmd import dcmd
    from ctypes import windll, byref, wintypes
os.environ.update({'PYTHONIOENCODING':'UTF-8'})
from configset import configset
import argparse
import clipboard
import bitmath
from make_colors import make_colors
from pydebugger.debug import debug
from pywget import wget
from datetime import datetime
from xnotify.notify import notify
import shutil
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
    ARL = "4659ecf4e9e46931714cbf470afd5242fdf97505c7f0e89aecc9442caa056064c9a538693acb37292467d76a2039e4e6b38e0d118fe018625d5252f38db315c46bf17d45cd1442acaf15006d9ef9d42aaf385a71c937b6fafa342bb2bb0dfa6e"
    deezer = None
    if ARL:
        debug(ARL = ARL)
        deezer = Deezer(arl = ARL)
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
    def download(cls, tracks, numbers = None, fformat = 'mp3', download_path = None):
        # os.environ.update({'DEBUG':'1'})
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
            # debug(track_detail = track_detail, debug = True)
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
            #name = os.path.join(download_path, name)
            #wget.download(url_download[0], out=name)
            if fformat == 'mp3':
                while 1:
                    try:
                        track_detail["download"](download_path, quality=track_formats.MP3_320)
                        break
                    except:
                        pass
            elif fformat == 'flac':
                while 1:
                    try:
                        track_detail["download"](download_path, quality=track_formats.FLAC)
                        break
                    except:
                        pass
    @classmethod
    def split_number(cls, x):
        debug(x = x)
        fr, to = x.split("-")
        fr = fr.strip()
        to = to.strip()
        track_number = list(range(int(fr), int(to)+1))
        return track_number

    @classmethod
    def create_download_path(cls, id, download_path):
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
        release_year = datetime.strptime(release_date, '%Y-%m-%d').year
        
        if not os.path.isdir(os.path.join(download_path, artist)):
            os.makedirs(os.path.join(download_path, artist))
        download_path = os.path.join(download_path, artist)
        # folder_name = artist + " - " + album_detail.get('title') + " (" + str(release_year) + ")"
        folder_name = "(" + str(release_year) + ") " + album_detail.get('title')
        folder_name = re.sub("\: ", " - ", folder_name)
        folder_name = re.sub("\?|\*", " ", folder_name)
        folder_name = re.sub("\:", "", folder_name)
        download_path = os.path.join(download_path, folder_name)
        
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
        
        with open(cover, 'wb') as cover_file:
            cover_file.write(cover_data.get('image'))
        with open(poster, 'wb') as poster_file:
            poster_file.write(cover_data.get('image'))
        with open(artist_pic, 'wb') as artist_pic_file:
            artist_pic_file.write(artist_picture_data.get('image'))

        return download_path

    @classmethod
    def download_interactive(cls, query, download_path = None, ftype='artist', fformat='mp3'):
        result = cls.find(query, ftype)
        if not download_path:
            download_path = os.getcwd()
        download_path0 = download_path
        
        if result:
            n = 1
            for i in result:
                print(cls.format_number(n, len(result)) +  ". " + make_colors(i.get('name'), 'lw', 'bl') + "[" + make_colors("{0} album".format(i.get('nb_album')), 'bl', 'ly') + "]")
                n +=1
            q = raw_input(make_colors("Select Number:", 'lw', 'm') + " ")
            if q:
                q = str(q).strip()
            else:
                sys.exit()
            if q and q.isdigit():
                if int(q) <= len(i):
                    n = 1
                    id = result[int(q) - 1].get('id')
                    artist_name = result[int(q) - 1].get('name')
                    debug(id = id)
                    #id = 81238
                    while 1:
                        try:
                            disco = cls.deezer.get_artist_discography(id)
                            break
                        except:
                            pass
                    debug(disco = disco)
                    disco = sorted(disco, key = lambda k: k['DIGITAL_RELEASE_DATE'], reverse = True)
                    print(make_colors("DISCOGRAPHY:", 'lw', 'g') + " ")
                    debug(d_keys = disco[0].keys())
                    for d in disco:
                        album_artist_name = d.get('ART_NAME')
                        if artist_name == album_artist_name:
                            album_artist_name = make_colors("{0} album".format(d.get('ART_NAME')), 'lw', 'lr')
                        else:
                            album_artist_name = make_colors("{0} album".format(d.get('ART_NAME')), 'b', 'y')
                        print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('ALB_TITLE'), 'lw', 'bl') + " / " + album_artist_name + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                        n += 1
                    notify('Deez', 'Deez', 'ready to select album', 'Ready to Select Album !', icon=cls.LOGO, direct_run = True)
                    q1 = raw_input(make_colors("Select Number:", 'lw', 'm') + " ")
                    if q1:
                        q1 = str(q1).strip()
                    if q1 and q1.isdigit():
                        if int(q1) <= len(disco):
                            n = 1
                            id = disco[int(q1) - 1].get('ALB_ID')
                                                        
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
                        q2 = raw_input(make_colors("Select Number to download [a/all = download all]:", 'lw', 'm') + " ")
                        if q2:
                            q2 = str(q2).strip()
                        debug(tracks = tracks)
                        debug(q2 = q2)
                        if q2:
                            download_path = cls.create_download_path(id, download_path)
                        if q2 and q2 == 'all' or q2 == 'a':
                            cls.download(tracks, fformat = fformat, download_path = download_path)

                        elif "-" in q2 or "," in q2:
                            if "," in q2:
                                track_number_1 = re.split(",", q2)
                                debug(track_number_1 = track_number_1)
                                track_number_1 = list(filter(None, track_number_1))
                                debug(track_number_1 = track_number_1)
                                for i in track_number_1:
                                    if "-" in i:
                                        track_number = cls.split_number(i)
                                        cls.download(tracks, track_number, fformat, download_path)
                                    else:
                                        cls.download(tracks, [i], fformat, download_path)
                            elif "-" in q2:
                                track_number = cls.split_number(q2)
                                debug(track_number = track_number)
                                cls.download(tracks, track_number, fformat, download_path)

                        else:
                            # track_id = tracks[int(q2) - 1].get('SNG_ID')
                            if q2 and str(q2).isdigit():
                                cls.download(tracks, [int(q2)], fformat, download_path)
                            else:
                                if q2:
                                    return cls.download_interactive(q2, download_path0, ftype, fformat)        
                                else:
                                    return cls.download_interactive(query, download_path0, ftype, fformat)        
                        notify('Deez', 'Deez', 'finish', 'All Download Finished !', icon=cls.LOGO, direct_run = True)

                    elif q1 and q1 == 'all' or q1 == 'a':
                        for ds in disco:
                            id = ds.get('ALB_ID')
                            while 1:
                                try:
                                    tracks = cls.deezer.get_album_tracks(id)
                                    break
                                except:
                                    pass
                            download_path = cls.create_download_path(id, download_path0)
                            cls.download(tracks, fformat = fformat, download_path = download_path)


                    elif "-" in q1 or "," in q1:
                        if "," in q1:
                            album_numbers = re.split(",", q1)
                            debug(album_numbers = album_numbers)
                            album_numbers = list(filter(None, album_numbers))
                            debug(album_numbers = album_numbers)
                            for ds in album_numbers:
                                id = disco[int(ds) - 1].get('ALB_ID')
                                while 1:
                                    try:
                                        tracks = cls.deezer.get_album_tracks(id)
                                        break
                                    except:
                                        pass
                                download_path = cls.create_download_path(id, download_path0)
                                cls.download(tracks, fformat = fformat, download_path = download_path)                                
                        elif "-" in q1:
                            album_numbers = cls.split_number(q1)
                            debug(album_numbers = album_numbers)
                            for ds in album_numbers:
                                id = disco[int(ds) - 1].get('ALB_ID')
                                while 1:
                                    try:
                                        tracks = cls.deezer.get_album_tracks(id)
                                        break
                                    except:
                                        pass
                                download_path = cls.create_download_path(id, download_path0)
                                cls.download(tracks, fformat = fformat, download_path = download_path)                                
                    else:
                        if q1:
                            return cls.download_interactive(q1, download_path0, ftype, fformat)
                        else:
                            return cls.download_interactive(query, download_path0, ftype, fformat)
            else:
                if q:
                    return cls.download_interactive(q, download_path0, ftype, fformat)
                else:
                    return cls.download_interactive(query, download_path0, ftype, fformat)
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
        if len(sys.argv) == 1:
            parser.print_help()
        else:
            args = parser.parse_args()
            cls.download_interactive(args.query, args.download_path, fformat = args.type)
            
def usage():
    Deez.usage()
        
if __name__ == '__main__':    
    #Deez.download_interactive(sys.argv[1])
    Deez.usage()
    #print(Deez.format_number(sys.argv[1]))

    