import Tkinter
from PIL import ImageTk, Image
import itertools as it
import time


class TkSceneRoot(Tkinter.Tk):
    def __init__(self, scene):
        if scene.saved_frames == []:
            raise Exception(str(scene) + " has no frames!")
        master = Tkinter.Tk.__init__(self)

        kwargs = {
            "height" : scene.camera.pixel_shape[0],        
            "width" : scene.camera.pixel_shape[1],
        }

        self.frames = scene.saved_frames

        self.frame = Tkinter.Frame(self, **kwargs)
        self.frame.pack()
        self.canvas = Tkinter.Canvas(self.frame, **kwargs)
        self.canvas.configure(background='black')        
        self.canvas.place(x=0, y=0)

        nb_frames = len(scene.saved_frames)
        self.present_frame_nb = 0
        self.playing = True
        
        self.slider = Tkinter.Scale(master, from_ = 0, to = nb_frames - 1,
            orient = Tkinter.HORIZONTAL, length = 500)
        print "there are ", nb_frames, " frames"
        self.slider.bind("<Button-1>",self.skip_to_frame)
        self.slider.bind("<B1-Motion>",self.skip_to_frame)
        self.slider.pack()

        last_time = time.time()
        #for frame in it.cycle(scene.saved_frames):
        for frame_nb in it.cycle(range(nb_frames)):
            # try:
            #     self.show_new_image(frame)
            # except:
            #     break
            if not self.playing:
                break
            frame = self.frames[frame_nb]
            self.show_new_image(frame)
            sleep_time = scene.frame_duration
            sleep_time -= time.time() - last_time
            time.sleep(max(0, sleep_time))
            last_time = time.time()
            self.present_frame_nb += 1
            self.slider.set(self.present_frame_nb)
            if self.present_frame_nb == nb_frames:
                self.present_frame_nb = 0
        self.mainloop()

    def show_new_image(self, frame):
        image = Image.fromarray(frame.astype('uint8')).convert('RGB')
        photo = ImageTk.PhotoImage(image)
        self.canvas.delete(Tkinter.ALL)
        self.canvas.create_image(
            0, 0,
            image = photo, anchor = Tkinter.NW
        )
        self.update()

    def skip_to_frame(self,event):
        print "skipping to frame"
        self.playing = False
        slider_value = 51 #self.slider.get()
        print "present frame is ", self.present_frame_nb
        if self.present_frame_nb != slider_value:
            print "updating present frame to ", slider_value
            self.present_frame_nb = slider_value
            self.show_new_image(self.frames[self.present_frame_nb])



