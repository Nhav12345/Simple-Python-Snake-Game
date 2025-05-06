import customtkinter as ctk
import tkinter as tk
import math
import random
import pygame
import os


os.chdir(os.path.dirname(os.path.abspath(__file__)))


EATSOUND="Eat.wav"

class App(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        global score
        self.resizable(False, False)
        self.geometry("600x600")
        self.rowconfigure(0, weight=33)
        self.rowconfigure(1, weight=66)
        self.columnconfigure(0, weight=1)
        pygame.mixer.init()
        score=tk.StringVar(self)
        score.set("Score: 0")
        self.CallTopFrame()
        self.startButton=ctk.CTkButton(self, text="START GAME", command=self.CallGameCanva)
        self.startButton.grid(row=1, column=0)
    def CallTopFrame(self):
        self.topFrame=TopFrame(self)
        self.topFrame.grid(row=0, column=0, sticky="nesw")
    def CallGameCanva(self):
        self.startButton.destroy()
        self.gmaeCanva=GameCanva(master=self)
        self.gmaeCanva.grid(row=1, column=0, sticky="nesw")
        self.UpdateGameCanva()
    def UpdateGameCanva(self):
        self.gmaeCanva.Update()
        self.after(50, self.UpdateGameCanva)


class TopFrame(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.score=ctk.CTkLabel(self, textvariable=score)
        self.score.pack(anchor="center", expand=True)


class GameCanva(tk.Canvas):
    def __init__(self, *args, **kwargs):
        self.width=590
        self.height=450
        super().__init__(*args, **kwargs)
        self.player=Snake(self, 100, 100, 10)
        self.food=Food(self, self.width, self.height, 10)
        self.focus_set()
        self.bind("<Left>", self.Left)
        self.bind("<Right>", self.Right)
        self.bind("<Up>", self.Up)
        self.bind("<Down>", self.Down)
    def Left(self, event:tk.Event):
        if self.player.looking=="r":
            pass
        else:
            self.player.direction="horizontal"
            self.player.velocity['x']=-1
            self.player.velocity["y"]=0
            self.player.looking="l"
    def Right(self, event):
        if self.player.looking=="l":
            pass
        else:
            self.player.direction="horizontal"
            self.player.velocity['x']=1
            self.player.velocity["y"]=0
            self.player.looking="r"
    def Up(self, event):
        if self.player.looking=="d":
            pass
        else:
            self.player.direction="vertical"
            self.player.velocity['x']=0
            self.player.velocity["y"]=-1
            self.player.looking="u"
    def Down(self, event):
        if self.player.looking=="u":
            pass
        else:
            self.player.direction="vertical"
            self.player.velocity['x']=0
            self.player.velocity["y"]=1
            self.player.looking="d"
    def Update(self):
        if self.player.direction=="vertical":
            if (self.height+self.player.speed)>self.player.coords[1]>(0-self.player.speed):
                self.player.Move()
            elif self.player.coords[1]>=(self.height+self.player.speed):
                self.player.MoveTo(self.player.coords[0], 0)
            elif self.player.coords[1]<=-(0-self.player.speed):
                self.player.MoveTo(self.player.coords[0], self.height)

        else:
            if (self.width+self.player.speed)>self.player.coords[0]>(0-self.player.speed):
                self.player.Move()
            elif self.player.coords[0]>=(self.width+self.player.speed):
                self.player.MoveTo(0, self.player.coords[1])
            elif self.player.coords[0]<=(0-self.player.speed):
                self.player.MoveTo(self.width, self.player.coords[1])
        self.eatenSate=self.food.CheckEaten(self.player)
        if self.eatenSate:
            self.food.Reset()
            scoreToEdit=score.get()
            scorenum=int(scoreToEdit.split()[-1])
            score.set(f"Score: {scorenum+1}")
            self.player.AddCell()




class Snake:
    def __init__(self, canva : tk.Canvas, x, y, size):
        self.canva=canva
        self.size=size
        self.color="Blue"
        self.head=self.canva.create_rectangle(x,y, x+size, y+size, fill=self.color)
        self.body={}
        self.body_order = []
        self.direction="vertical"
        self.looking="d"
        self.speed=10
        self.velocity={"x":0, "y":1}
        self.coords=self.canva.coords(self.head)
        x = int(self.coords[0] // self.size) * self.size
        y = int(self.coords[1] // self.size) * self.size
        self.body[self.head]=[x, y]
        self.body_order.append(self.head)
    def Move(self):
        dx = self.velocity["x"] * self.speed
        dy = self.velocity["y"] * self.speed
        for e in self.body_order:
            coords=self.canva.coords(e)
            x = int(coords[0] // self.size) * self.size
            y = int(coords[1] // self.size) * self.size
            self.body[e]=(x, y)
        self.coords=self.body[self.head]
        self.keys=self.body_order
        for index, e in enumerate(self.body_order):
            if self.head==e:
                new_head_x = self.body[e][0] + dx
                new_head_y = self.body[e][1] + dy
                self.canva.moveto(self.head, new_head_x, new_head_y)
            elif e!=self.head:
                self.canva.moveto(e, self.body[self.keys[index-1]][0], self.body[self.keys[index-1]][1])
    def MoveTo(self, x, y):
        self.canva.moveto(self.head, x, y)
        coords=self.canva.coords(self.head)
        mx = int(coords[0] // self.size) * self.size
        my = int(coords[1] // self.size) * self.size
        self.body[self.head]=[mx, my]
        self.coords=self.body[self.head]
    def AddCell(self):
        self.keys=list(self.body.keys())
        x=self.body[self.keys[-1]][0]
        y=self.body[self.keys[-1]][1]
        snakecell=SnakeCell(self.canva, x , y, self.size, self.color)
        self.body[snakecell.cell]=[x, y, x+self.size, y+self.size]
        self.body_order.append(snakecell.cell)




class SnakeCell:
    def __init__(self, canva:tk.Canvas, x, y, size, color):
        self.canva=canva
        self.color=color
        self.cell=self.canva.create_rectangle(x, y, x+size, y+size, fill=self.color)



        
class Food:
    def __init__(self, canva: tk.Canvas, canvawidth, canvaheight, size):
        self.canva=canva
        self.size=size
        self.canvawidth=canvawidth
        self.canvaheight=canvaheight
        x, y=random.randint(self.size, self.canvawidth-self.size), random.randint(self.size, self.canvaheight-self.size)
        self.body=self.canva.create_rectangle(x,y, x+self.size, y+self.size, fill="red")
        self.coords=self.canva.coords(self.body)
    def CheckEaten(self, player):
        self.playerBbox=self.canva.bbox(player.head)
        self.Bbox=self.canva.bbox(self.body)
        if self.playerBbox[2]>=self.Bbox[0] and self.playerBbox[0] <= self.Bbox[2] and self.playerBbox[3] >= self.Bbox[1] and self.playerBbox[1] <= self.Bbox[3]:
            return True
        return False
    def Reset(self):
        pygame.mixer.music.load(EATSOUND)
        pygame.mixer.music.play()
        x, y=random.randint(self.size, self.canvawidth-self.size), random.randint(self.size, self.canvaheight-self.size)
        self.canva.moveto(self.body, x, y)
        
        

if __name__=='__main__':
    print("Start...")
    app=App()
    app.mainloop()