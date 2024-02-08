from manim import * 
from manim_slides import Slide

UG_BLUE = '#003865'
UG_COBALT = '#009DEC'
CMU_SANS = "CMU Sans Serif"
config["background_color"] = WHITE

class TalkHeaderFooter(VMobject):

        def _get_slide_count(self):
            return sum([self.dots_per_sec[s] for s in self.dots_per_sec])

        def _create_header(self, dots_per_sec):
            self.h_background = Rectangle(width=config["frame_width"], height=config["frame_height"]/17, fill_color=UG_BLUE, color=UG_BLUE, fill_opacity=1).to_edge(UP, 0)

            self.h_background2 = Rectangle(width=config["frame_width"], height=config["frame_height"]/10, fill_color=UG_COBALT, color=UG_COBALT, fill_opacity=1).to_edge(UP, 0)

            self.sections = list(dots_per_sec)
            self.dots_per_sec = dots_per_sec
            self.current_section = self.sections[0]
            self.current_dot = 0
            self.current_section_number = 0
            
            self.title_texts = dict(zip(
                self.sections,
                [Text(sec, color=WHITE, font_size=36, font=CMU_SANS, weight="BOLD").scale(0.35).set_opacity(0.5) for sec in self.sections]))

            # Even spacing between section titles
            total_title_width = sum([t.width for t in self.title_texts.values()])
            buff = (config["frame_width"] - total_title_width - DEFAULT_MOBJECT_TO_EDGE_BUFFER*2)/(len(self.sections) - 1)

            self.title_texts[self.current_section].set_opacity(1)

            self.title_group = \
                Group(*self.title_texts.values())\
                .arrange(aligned_edge=UP, buff=buff)\
                .to_edge(UP, buff=0.08)\
                .to_edge(LEFT)\
            
            self.dots = dict(zip(list(self.sections), 
                [
                    VGroup(*[Circle(color=WHITE, radius=0.05, stroke_width=1.5, stroke_opacity=0.5) for i in range(self.dots_per_sec[sec])])\
                        .arrange(buff=0.03)
                for sec in self.sections] 
            ))

            for sec in self.sections:
                self.dots[sec].move_to(self.title_texts[sec].get_left()- self.dots[sec].get_left()).shift(DOWN*0.2 + RIGHT*0.01)
            
            [d.set_stroke(opacity = 1) for d in self.dots[self.current_section]]
            self.dots[self.current_section][self.current_dot].set_fill(WHITE, opacity=1)

            self.add(self.h_background2, self.h_background, self.title_group, *self.dots.values())

        def _create_footer(self, dots_per_sec, title, name):
            self.f_background = Rectangle(width=config["frame_width"], height=config["frame_height"]/26, fill_color=UG_BLUE, color=UG_BLUE, fill_opacity=1).to_edge(DOWN, 0)

            self.f_background2 = Rectangle(width=config["frame_width"], height=config["frame_height"]/13, fill_color=UG_COBALT, color=UG_COBALT, fill_opacity=1).to_edge(DOWN, 0)

            self.title_text = Text(title, color=WHITE, font=CMU_SANS, font_size=38, weight=BOLD).scale(0.4).move_to(self.f_background).to_edge(LEFT)

            to_midpoint = self.f_background2.get_top() - (self.f_background2.height - self.f_background.height)/2

            self.name_text = Text(name, color=WHITE, font=CMU_SANS, font_size=38, weight=BOLD).scale(0.4).move_to(to_midpoint).to_edge(LEFT)
            total_frames = self._get_slide_count()
            
            self.count_text = Text("1/" + str(total_frames), color=WHITE, font=CMU_SANS, font_size=38, weight=BOLD).scale(0.4).move_to(self.f_background).to_edge(RIGHT)

            self.add(self.f_background2, self.f_background, self.title_text, self.name_text, self.count_text)

        def __init__(self, dots_per_sec, title="", name="Matthew McIlree", **kwargs):
            super().__init__(**kwargs)
            
            self._create_header(dots_per_sec)
            self._create_footer(dots_per_sec, title, name)
            self.add(Circle())
        
        
        def set_current(self, section, dot_number):
            animations = []
            if isinstance(section, int):
                section = self.sections[section]

            self.title_texts[self.current_section].set_opacity(0.5)
            [d.set_stroke(opacity = 0.5) for d in self.dots[self.current_section]]
            self.dots[self.current_section][self.current_dot].set_fill(opacity=0.01)

            self.current_section = section
            self.current_section_number = self.sections.index(section)
            self.current_dot = dot_number
            self.title_texts[self.current_section].set_opacity(1)
            
            current_frame = sum([self.dots_per_sec[self.sections[i]] for i in range(len(self.sections)) if i < self.current_section_number]) + self.current_dot + 1
            total_frames = self._get_slide_count()

            self.count_text.become(Text(str(current_frame) + "/" + str(total_frames), color=WHITE, font=CMU_SANS, font_size=38).scale(0.4).move_to(self.count_text))
            [d.animate.set_stroke(opacity = 1) for d in self.dots[self.current_section]]
            self.dots[self.current_section][self.current_dot].set_fill(WHITE, opacity=1)
            
        
        def next(self):
            if self.current_dot == self.dots_per_sec[self.current_section] - 1:
                return self.set_current(self.current_section_number+1, 0)
            else:
                return self.set_current(self.current_section_number, self.current_dot + 1)

# Testing

test_talk_header1 = TalkHeaderFooter(
    {
        "Introduction": 3,
        "Middle Bit": 6,
        "Worked Example": 5,
        "Conclusion": 2
    }
)

test_talk_header2 = TalkHeaderFooter(
    {
        "Hi": 15,
        "NOOOOOOOOOOO": 2,
    }
)

header = TalkHeaderFooter(
    {
        "Introduction": 3,
        "Proof Logging": 5,
        "Simple Circuit Algorithms": 10,
        "SCC Circuit Algorithms": 10,
        "Testing": 5,
        "Conclusion": 3
    },
    title="Proof Logging for the Circuit Constraint"
)

class TestHeader(Slide):
    def construct(self):
        header.set_current(0, 0)
        self.add(header)
        self.wait(0.5)

        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.set_current("Testing", 3), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.set_current(0, 2), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)
        self.next_slide()
        self.play(header.animate.next(), run_time=0.01)

        