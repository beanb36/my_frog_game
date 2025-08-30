import pygame


class FrogGame:
    def __init__(self):
        pygame.init()
        
        # Set up the display
        self.width = 720
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("My Frog")
        
        # Set up colors
        self.BG_COLOR = (144, 238, 144) 
        
        # Define regions and their corresponding animations
        self.regions = {
            'head': {'rect': pygame.Rect(240, 0, 240, 240),      
                    'frames': self.load_animation('head')},          
            'right_hand': {'rect': pygame.Rect(480, 240, 240, 240), # Middle right
                    'frames': self.load_animation('right')},      

        }
        # Animation state
        self.current_region = None
        self.current_frame = 0
        self.animation_speed = 5  # Frames to wait before showing next animation frame
        self.frame_counter = 0
        
        # Load base frog image
        try:
            self.base_frog = pygame.image.load("frames\\frog.png").convert_alpha()
            self.base_frog = pygame.transform.scale(self.base_frog, (self.width, self.height))
        except pygame.error:
            print("Error: Could not load frog.png")
            print("Please ensure you have a frog.png file in the same directory")
            self.base_frog = pygame.Surface((self.width, self.height))
            self.base_frog.fill(self.BG_COLOR)

    def load_animation(self, region_name):
        #Load animation frames for a specific region 
        frames = []
        try:
            i = 0
            while True:
                frame = pygame.image.load(f"frames\\{region_name}_{i}.png").convert_alpha()
                frames.append(frame)
                i += 1
        except FileNotFoundError:
            1==1 #when no more frames are found do nothing
        return frames
    
    def get_clicked_region(self, pos):
        #Determine which region was clicked 
        for region_name, region_data in self.regions.items():
            if region_data['rect'].collidepoint(pos):
                return region_name
        return None

    def draw(self):
        # Draw the current game state
        # If no animation is playing, show the base frog
        if not self.current_region:
            self.screen.blit(self.base_frog, (0, 0))
        # If animation is active
        else:
            region_data = self.regions[self.current_region]
            frame = region_data['frames'][self.current_frame % len(region_data['frames'])]
            self.screen.blit(frame, (0, 0))   
        pygame.display.flip()

    def run(self):
        #Main game loop
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        clicked_region = self.get_clicked_region(event.pos)
                        if clicked_region:
                            self.current_region = clicked_region
                            self.current_frame = 0
                            self.frame_counter = 0
            
            # Update animation
            if self.current_region:
                self.frame_counter += 1
                if self.frame_counter >= self.animation_speed:
                    self.frame_counter = 0
                    self.current_frame += 1
                    if self.current_frame >= len(self.regions[self.current_region]['frames']):
                        self.current_region = None
            
            self.draw()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = FrogGame()
    game.run()