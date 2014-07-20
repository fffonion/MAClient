# coding:utf-8
from _prototype import plugin_prototype
import pymedia.audio.acodec as acodec
import pymedia.audio.sound as sound
import pymedia.muxer as muxer
import os, os.path as opath
import sys
import threading
import time
# start meta
__plugin_name__ = 'bgm player'
__author = 'fffonion'
__version__ = 0.1
# hooks={'ENTER/EXIT_ACTION':PRIORITY}
# eg:
# hook on explore start with priority 1 (the bigger the higher):
# 'ENTER_explore':1
hooks = {'ENTER__fairy_battle':1, 'EXIT__fairy_battle':1, 'ENTER__explore_floor':1, 'EXIT__explore_floor':1, 'ENTER_tasker':1, 'EXIT_tasker':1}
# extra cmd hook
extra_cmd = {'bgm':'set_bgm'}
require_feature_nologin = True
# end meta
getPATH0 = (opath.split(sys.argv[0])[1].find('py') != -1 or sys.platform == 'cli') \
         and sys.path[0].decode(sys.getfilesystemencoding()) \
         or sys.path[1].decode(sys.getfilesystemencoding())

def set_bgm(plugin_vals):
    snd = sound.Output(5, 1, sound.AFMT_S16_LE)  # whatever
    def do(arg):
        if arg == 'on':
            fade_in(snd)
        elif arg == 'off':
            fade_out(snd)
    return do


def fade_out(snd, duration = 0.5):
    if snd:
        for i in xrange(25):
            snd.setVolume(65535 * (24 - i) / 25)
            time.sleep(duration / 25.0)

def fade_in(snd, duration = 0.5):
    if snd:
        for i in xrange(25):
            snd.setVolume(65535 * (i + 1) / 25)
            time.sleep(duration / 25.0)

def play_sound_from_file(file_name):
    p = music_player(file_name)
    p.setDaemon(True)
    p.start()
    return p

def get_abs_path(cmp_path):
    return opath.join(getPATH0, cmp_path).encode('utf-8')

class music_player(threading.Thread):
    def __init__(self, mfile):
        threading.Thread.__init__(self)
        self.mfile = mfile
        self.stop = False
        self.pos = 0
        self.buf = None

    def getbuff(self, csize = 512):
        # get buf loop so that playing can last long
        if not self.buf:
            f = open(self.mfile, 'rb')
            self.buf = f.read()
        if self.pos + csize > len(self.buf):
            ret = self.buf[self.pos:]
            self.pos = 0
        else:
            ret = self.buf[self.pos:self.pos + csize]
            self.pos += csize
        return ret

    def run(self):
        dm = muxer.Demuxer(str.split(self.mfile, '.')[-1].lower())
        self.snd = dec = None
        s = self.getbuff()
        while len(s) and not self.stop:
            frames = dm.parse(s)
            if frames:
                for fr in frames:
                    if dec == None:
                        dec = acodec.Decoder(dm.streams[fr[0]])
                    r = dec.decode(fr[1])
                    if r and r.data:
                        if self.snd == None:
                            self.snd = sound.Output(
                                int(r.sample_rate),
                                r.channels,
                                sound.AFMT_S16_LE)
                        data = r.data
                        self.snd.play(data)
            s = self.getbuff()
        # 淡出
        fade_out(self.snd)
        # 停止
        self.snd.stop()
        # 设置音量正常
        self.snd.setVolume(65535)


class plugin(plugin_prototype):
    def __init__(self):
        self.__name__ = __plugin_name__
        self.state = 0
        self.last_state = [0]
        self.playing = None
        self.state_file = ['plugins/bgm/bgm_common1.mp3', 'plugins/bgm/bgm_sarch1.mp3', 'plugins/bgm/bgm_event1.mp3']

    def _change_state(self, state):
        # change state
        self.last_state.append(self.state)  # stack push
        if self.playing and state != self.state:
            self.playing.stop = True
            self.playing.join()
            self.state = state
            self.playing = play_sound_from_file(get_abs_path(self.state_file[state]))
            return True
        elif not self.playing:
            self.playing = play_sound_from_file(get_abs_path(self.state_file[state]))
        else:
            return False

    def _rollback_state(self, *args, **kwargs):
        # take this as simple "stack pop"
        if len(self.last_state) < 1:
            self.last_state = [0]
        self._change_state(self.last_state[-1])
        self.last_state = self.last_state[:-2]

    def ENTER_tasker(self, *args, **kwargs):
        self._change_state(0)

    def ENTER__explore_floor(self, *args, **kwargs):
        self._change_state(1)

    def ENTER__fairy_battle(self, *args, **kwargs):
        self._change_state(2)

    EXIT__fairy_battle = EXIT__explore_floor = EXIT_tasker = _rollback_state


if __name__ == '__main__':
    # cd ..
    getPATH0 = opath.split(getPATH0)[0]
    a = plugin()
    a.setval(1, 2)
    a.ENTER_tasker()
    time.sleep(2)
    a.ENTER__explore_floor()
    time.sleep(2)
    snd = sound.Output(5, 1, sound.AFMT_S16_LE)
    snd.setVolume(0)
    time.sleep(3)
    snd.setVolume(65535)
    a.ENTER__fairy_battle()
    a.ENTER__fairy_battle()
    time.sleep(10)
    a.EXIT__fairy_battle()
    time.sleep(2)
    a.EXIT__explore_floor()
    time.sleep(2)
    a.EXIT_tasker()
    # a.ENTER_explore()
    time.sleep(120)
