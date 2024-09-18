from tkinter import *
from functools import partial

from GAMST_OBSERVER.controller.HomeController import *
from GAMST_OBSERVER.domain.process_word import *
from GAMST_OBSERVER.domain.ReportedInformation import *
from GAMST_OBSERVER.view.styles.sizes import *
from GAMST_OBSERVER.view.styles.colors import *


class HomeView:
    def __init__(self):
        self.root = Tk()
        self.root.title("GAMST - 용인대학교 강의실 관제 프로그램")
        self.root.iconbitmap(default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "images/icon.ico"))
        self.root.config(bg=BACKGROUND_FRAME_COLOR)
        self.root.resizable(False, False)

        self.init_seat_frame()
        self.init_record_frame()

        self.root.mainloop()

    def init_seat_frame(self):
        seat_frame = LabelFrame(self.root, text="좌석", bg=BACKGROUND_FRAME_COLOR)
        seat_frame.pack(padx=30, pady=10)

        seat_grids = []

        for index in range(SEAT_ROW_COUNT * SEAT_COLUMN_COUNT):
            button = Button(seat_frame,
                            anchor="w", justify=LEFT,
                            overrelief="solid",
                            padx=10,
                            width=BUTTON_WIDTH, height=BUTTON_HEIGHT
                            )
            button.config(command=partial(on_seat_button_event, index), bg=SEAT_OFFLINE_COLOR)  # 버튼 생성 후 command 설정
            seat_grids.append(button)

        for row in range(SEAT_ROW_COUNT):
            for column in range(SEAT_COLUMN_COUNT):
                if column == 0:
                    seat_grids[row * SEAT_COLUMN_COUNT + column].grid(row=row, column=column, padx=(20, 0))  # 좌측 패딩 추가
                elif column % 2 == 1:
                    seat_grids[row * SEAT_COLUMN_COUNT + column].grid(row=row, column=column, padx=(0, 20))  # 우측 패딩 추가
                if row == 0:
                    seat_grids[row * SEAT_COLUMN_COUNT + column].grid(row=row, column=column, pady=(10, 0))  # 상단 패딩 추가
                elif row == SEAT_ROW_COUNT - 1:
                    seat_grids[row * SEAT_COLUMN_COUNT + column].grid(row=row, column=column, pady=(0, 15))  # 하단 패딩 추가
                else:
                    seat_grids[row * SEAT_COLUMN_COUNT + column].grid(row=row, column=column)

        self.update_seat_button_texts(seat_grids)

    def init_record_frame(self):
        record_frame = LabelFrame(self.root, text="영상 녹화", bg=BACKGROUND_FRAME_COLOR)
        record_frame.pack(padx=30, pady=20, side=RIGHT)

        record_start_button = Button(record_frame,
                                     text="시작",
                                     overrelief="solid",
                                     width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
        record_start_button.config(command=partial(on_record_button_event, record_start_button))
        record_start_button.grid(row=0, column=0, padx=20, pady=10)

    def update_seat_button_texts(self, seat_grids):
        lifetime = 7
        for ps in ps_informations:
            if ps.identifier is not None:
                if time.time() - ps.unix_time > lifetime:
                    seat_grids[int(ps.identifier)].config(text="", bg=SEAT_OFFLINE_COLOR)
                    continue
                elif ps.foreground_name in WARNING_PROCESS or ps.cursor_name in WARNING_PROCESS:
                    bg = WARNING_COLOR
                elif ps.foreground_name in SUSPECT_PROCESS or ps.cursor_name in SUSPECT_PROCESS:
                    bg = SUSPECT_COLOR
                elif ps.foreground_name in GOOD_PROCESS or ps.cursor_name in GOOD_PROCESS:
                    bg = GOOD_COLOR
                else:
                    bg = SEAT_ONLINE_COLOR

                new_text = (f"{ps.foreground_name}\n"
                            f"{ps.foreground_title}\n"
                            "\n"
                            f"{ps.cursor_name}\n"
                            f"{ps.cursor_title}\n"
                            )
                seat_grids[int(ps.identifier)].config(text=new_text, bg=bg)

        self.root.after(1000, partial(self.update_seat_button_texts, seat_grids))  # stackoverflow X, eventloop 에 의해 발생.


if __name__ == '__main__':
    HomeView()
