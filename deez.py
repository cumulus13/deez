#!/usr/bin/env python3

from __future__ import print_function

from pydeezer import Deezer
from pydeezer.constants import track_formats
import os
import sys
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
            result = cls.deezer.search_artists(query)
        elif ftype == 'album':
            result = cls.deezer.search_albums(query)
        elif ftype == 'track':
            result = cls.deezer.search_tracks(query)
        elif ftype == 'playlist':
            result = cls.deezer.search_playlists(query)
        else:
            print(make_colors("Invalid ftype !", 'lw' ,'lr'))
            return False

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
    def download_interactive(cls, query, download_path = None, ftype='artist', fformat='mp3'):
        result = cls.find(query, ftype)
        if not download_path:
            download_path = os.getcwd()
        cover_name = 'Cover'
        poster_name = 'Poster'
        
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
                    debug(id = id)
                    #id = 81238
                    disco = cls.deezer.get_artist_discography(id)
                    debug(disco = disco)
                    disco = sorted(disco, key = lambda k: k['DIGITAL_RELEASE_DATE'], reverse = True)
                    print(make_colors("DISCOGRAPHY:", 'b', 'ly') + " ")
                    for d in disco:
                        print(cls.format_number(n, len(disco)) +  ". " + make_colors(d.get('ALB_TITLE'), 'lw', 'bl') + " / " + make_colors("{0} album".format(d.get('ART_NAME')), 'bl', 'ly') + " [" + make_colors(d.get('DIGITAL_RELEASE_DATE'), 'lr', 'lw') + "]")
                        n += 1
                    q1 = raw_input(make_colors("Select Number:", 'lw', 'm') + " ")
                    if q1:
                        q1 = str(q1).strip()
                    if q1 and q1.isdigit():
                        if int(q1) <= len(disco):
                            n = 1
                            id = disco[int(q1) - 1].get('ALB_ID')
                            album_detail = cls.deezer.get_album(id)
                            cover_data = cls.deezer.get_album_poster(album_detail, 1200)
                            artist_data = album_detail.get('artist')
                            artist = artist_data.get('name')
                            artist_picture_data = cls.deezer.get_artist_poster(cls.deezer.get_artist(artist_data.get('id')), 1000)
                            release_date = album_detail.get('release_date')
                            release_year = datetime.strptime(release_date, '%Y-%m-%d').year
                            
                            folder_name = artist + " - " + album_detail.get('title') + " (" + str(release_year) + ")"
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
                            print("Cover      =", cover)
                            print("Artist Pic =", artist_pic)
                            
                            with open(cover, 'wb') as cover_file:
                                cover_file.write(cover_data.get('image'))
                            with open(poster, 'wb') as poster_file:
                                poster_file.write(cover_data.get('image'))
                            with open(artist_pic, 'wb') as artist_pic_file:
                                artist_pic_file.write(artist_picture_data.get('image'))                            
                            
                            tracks = cls.deezer.get_album_tracks(id)
                            for track in tracks:
                                if fformat == 'flac':
                                    print(make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(
                                        tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(
                                            tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE_FLAC'))).MB)) + " mb", 'lw', 'lr') + "]")
                                else:
                                    print(make_colors(cls.format_number(track.get('TRACK_NUMBER'), len(
                                        tracks)) + "/" + cls.format_number(track.get('DISK_NUMBER'), len(
                                            tracks)), 'lw', 'bl') + ". " + make_colors(track.get('SNG_TITLE'), 'bl', 'ly') + " [" + make_colors(str("%0.2f"%(int(track.get('DURATION')) / 60) + " minutes"), 'lr', 'lw')  + "/" + make_colors(str("%0.2f"%(bitmath.Byte(int(track.get('FILESIZE'))).MB)) + " mb", 'lw', 'lr') + "]")
                                    n += 1
                        q2 = raw_input(make_colors("Select Number to download [a/all = download all]:", 'lw', 'm') + " ")
                        if q2:
                            q2 = str(q2).strip()
                        if q2 and q2 == 'all' or q2 == 'a':
                            tracks = cls.deezer.get_album_tracks(id)
                            for track in tracks:
                                track_id = track.get('SNG_ID')
                                track_detail = cls.deezer.get_track(track_id)
                                track_info = track_detail["info"]
                                tags_separated_by_comma = track_detail["tags"]
                                
                                #url_download = cls.deezer.get_track_download_url(track, quality=track_formats.MP3_320)
                                #debug(url_download = url_download[0])
                                name = cls.format_number(track.get('TRACK_NUMBER'), len(tracks)) + ". " + track.get('SNG_TITLE')# + ".mp3"
                                track_detail.get('info').get('DATA').update({'SNG_TITLE': name})
                                #name = os.path.join(download_path, name)
                                #wget.download(url_download[0], out=name)
                                if fformat == 'mp3':
                                    track_detail["download"](download_path, quality=track_formats.MP3_320)
                                elif fformat == 'flac':
                                    track_detail["download"](download_path, quality=track_formats.FLAC)
                        
                                
        return cls.download_interactive(query, download_path, ftype, fformat)

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
        
if __name__ == '__main__':    
    #Deez.download_interactive(sys.argv[1])
    Deez.usage()
    #print(Deez.format_number(sys.argv[1]))

    