import pygame
import random

pygame.init()

class DrawInformation:
    # colours
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    BACKGROUND_COLOR = WHITE
    GRADIENTS = [(128,128,128), (160,160,160), (192,192,192)]

    FONT = pygame.font.Font(None, 30)
    LARGE_FONT = pygame.font.Font(None, 40)

    SIDE_PAD = 100
    TOP_PAD = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Sorting Visualiser')
        self.speed = 60
        
        self.set_list(lst)
    
    def set_list(self, lst):
        self.lst = lst
        self.max_val = max(self.lst)
        self.min_val = min(self.lst)

        self.block_width = round((self.width - self.SIDE_PAD) / len(self.lst))
        self.block_height = int((self.height - self.TOP_PAD - 50) / (self.max_val - self.min_val))
        self.startx = self.SIDE_PAD//2
    
    def draw(self, algo_name, ascending, color_positions={}):
        self.screen.fill(self.BACKGROUND_COLOR)
        self.draw_list(color_positions)

        title = self.LARGE_FONT.render(f"{algo_name} - {'ASCENDING' if ascending else 'DESCENDING'} - SPEED {self.speed}", True, self.BLUE)
        self.screen.blit(title, (self.width/2 - title.get_width()/2, 5))

        controls = self.FONT.render('R - Reset | SPACE - Start | A - Ascending | D - Descending | UP/DOWN - Speed', True, self.BLACK)
        self.screen.blit(controls, (self.width/2 - controls.get_width()/2, 50))

        algorithms = self.FONT.render("I - Insertion Sort | B - Bubble Sort", True, self.BLACK)
        self.screen.blit(algorithms, (self.width/2 - algorithms.get_width()/2, 80))

        pygame.display.update()

    def draw_list(self, color_positions={}, clear_bg=False):
        lst = self.lst

        if clear_bg:
            clear_rect = (self.SIDE_PAD//2, self.TOP_PAD-50, self.width - self.SIDE_PAD, self.height)
            pygame.draw.rect(self.screen, self.BACKGROUND_COLOR, clear_rect)

        for i, val in enumerate(lst):
            x = self.startx + (i * self.block_width)
            y = self.height - 50 - ((val - self.min_val) * self.block_height)
            color = self.GRADIENTS[i%3]

            if i in color_positions:
                color = color_positions[i]

            pygame.draw.rect(self.screen, color, (x, y, self.block_width, self.height))
        
        if clear_bg:
            pygame.display.update()

def generate_list(n, min_val, max_val):
    lst = []
    for _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)
    return lst

def bubble_sort(draw_info: DrawInformation, ascending=True):
    lst = draw_info.lst

    for i in range(len(lst)-1):
        for j in range(len(lst)-1-i):
            num1 = lst[j]
            num2 = lst[j+1]
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_info.draw("BUBBLE SORT", ascending, {j: draw_info.RED, j+1: draw_info.GREEN})
                yield True
    
    return lst

def insertion_sort(draw_info: DrawInformation, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        while True:
            ascending_sort = i > 0 and lst[i-1] > lst[i] and ascending
            descending_sort = i > 0 and lst[i-1] < lst[i] and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i], lst[i-1] = lst[i-1], lst[i]
            i -= 1
            draw_info.draw("INSERTION SORT", ascending, {i: draw_info.GREEN, i-1: draw_info.RED}, True)
            yield True
    
    return lst

def main():
    run = True
    clock = pygame.time.Clock()

    num_vals = 50
    min_val = 0
    max_val = 100

    lst = generate_list(num_vals, min_val, max_val)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False
    ascending = True

    sorting_algorithm = bubble_sort
    sorting_algo_name = "BUBBLE SORT"
    sorting_algo_generator = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    lst = generate_list(num_vals, min_val, max_val)
                    draw_info.set_list(lst)
                    sorting = False
                
                elif event.key == pygame.K_SPACE and not sorting:
                    sorting = True
                    sorting_algo_generator = sorting_algorithm(draw_info, ascending)
                
                elif event.key == pygame.K_a and not sorting:
                    ascending = True
                
                elif event.key == pygame.K_d and not sorting:
                    ascending = False
                
                elif event.key == pygame.K_b and not sorting:
                    sorting_algorithm = bubble_sort
                    sorting_algo_name = "BUBBLE SORT"
                
                elif event.key == pygame.K_i and not sorting:
                    sorting_algorithm = insertion_sort
                    sorting_algo_name = "INSERTION SORT"
                
                elif event.key == pygame.K_UP:
                    draw_info.speed += 5
                
                elif event.key == pygame.K_DOWN:
                    if draw_info.speed >= 5:
                        draw_info.speed -= 5
        
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw_info.draw(sorting_algo_name, ascending)
        
        clock.tick(draw_info.speed)
    
    pygame.quit()

if __name__ == '__main__':
    main()