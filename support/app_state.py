import pygame, sys
from pygame.math import Vector2

class AppState():
    def __init__(
            self,
            window_width: int,
            window_height: int,
            background_color: tuple[int, int, int],
            keys_pressed: dict,
            zoomable: bool = False,
            panable: bool = False
    ) -> None:
        """
        Parent Class
        ------------
        This is a parent class that creates a runable state in pygame.

        Parameters
        ----------
        window_width : int
        window_height : int
        background_color : tuple[int, int, int]
        keys_pressed : dict
        zoomable : bool, default False
        panable : bool, default False 
        """
        self.__window_width = window_width
        self.__window_height = window_height
        self.__background_color = background_color
        self.__keys_pressed = keys_pressed
        self.__zoomable = zoomable
        self.__panable = panable

        self.display_surface = pygame.display.get_surface()
        if self.__zoomable: self.surface = pygame.Surface((window_width * 3, window_height * 3)).convert_alpha()
        else: self.surface = pygame.Surface((window_width, window_height)).convert_alpha()
        self.origin = Vector2(0, 0)
        if self.__zoomable: self.zoom = 1
        if self.__panable: self.pan_active = False


    def __manage_window(self, event) -> None:
        """
        This method manages when to quit application, when to toggle fullscreen,
        and when to zoom.

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.WINDOWMAXIMIZED:
            pygame.display.toggle_fullscreen()
        if event.type == pygame.WINDOWMINIMIZED:
            pygame.display.toggle_fullscreen()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F12:
                pygame.quit()
                sys.exit()
        if self.__zoomable: self.__manage_zoom(event)
        if self.__panable: self.__manage_pan(event)


    def __manage_zoom(self, event) -> None:
        """
        This method manages when to zoom the application.
        TODO: make zoom center on the middle of the screen not top left

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
        if event.type == pygame.MOUSEWHEEL:
            if self.zoom > 0.34 and event.y < 0:
                self.zoom += event.y / 100
                self.origin -= Vector2((4) / self.zoom, (3) / self.zoom)
            if self.zoom < 3 and event.y > 0:
                self.zoom += event.y / 100
                self.origin -= Vector2((4) / self.zoom, (3) / self.zoom) # working on it here
        if self.zoom < 0.34:
            self.zoom = 0.34
        elif self.zoom > 3:
            self.zoom = 3


    def __manage_pan(self, event) -> None:
        """
        This method manages when to pan the application and the direction to pan to.

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
        pan_value = 10
        mouse_buttons = pygame.mouse.get_pressed()
        mouse_pos = Vector2(pygame.mouse.get_pos()) / self.zoom

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_buttons[0]:
                self.pan_active = True
                self.pan_offset_from_mouse = mouse_pos - self.origin
        if not mouse_buttons[0]:
            self.pan_active = False
        
        if self.pan_active:
            # sets origin to mouse pos when paning
            self.origin = mouse_pos - self.pan_offset_from_mouse
            
        if self.__keys_pressed[pygame.K_UP]:
            self.origin.y += pan_value
        if self.__keys_pressed[pygame.K_RIGHT]:
            self.origin.x += -pan_value
        if self.__keys_pressed[pygame.K_DOWN]:
            self.origin.y += -pan_value
        if self.__keys_pressed[pygame.K_LEFT]:
            self.origin.x += pan_value

    def __update_keys_pressed(self, event) -> None:
        """
        This method updates which of the keys in the dict __keys_pressed has
        been pressed or unpressed.

        Parameters
        ----------
        event : Event
            Paramenter from the pygame method pygame.event.get() in the event loop.
        """
        if event.type == pygame.KEYDOWN:
            for key in self.__keys_pressed:
                if event.key == key:
                    self.__keys_pressed[key] = True

        if event.type == pygame.KEYUP:
            for key in self.__keys_pressed:
                if event.key == key:
                    self.__keys_pressed[key] = False

    def event_loop(
            self,
            event
    ) -> None:
        """
        This method is empty and is meant to be overwritten.

        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override.
        """

    def __event_loop(self) -> None:
        """
        This method manages all events and calls all methods with the event parameter.
        """
        for event in pygame.event.get():
            
            self.__manage_window(event)
            self.__update_keys_pressed(event)
            
            self.event_loop(event)
    
    def draw_assets(self) -> None:
        """
        This method is empty and is meant to be overwritten.

        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        draw().
        """

    def draw_non_zoomable_assets(self):
        """
        This method is empty and is meant to be overwritten and only used if AppState is zoomable.

        The default implementation of this method does nothing; it's just a
        convenient "hook" that you can override. This method is called by
        draw().
        """

    def __draw(self) -> None:
        """
        This method draws the background first, then it draws the origin point,
        then it draws the zoomed screen depending on how zoomed the screen is.
        """
        self.surface.fill((self.__background_color))

        self.draw_assets()

        if self.__zoomable:
            zoomed_screen = pygame.transform.smoothscale_by(self.surface, self.zoom)
            self.display_surface.blit(zoomed_screen, Vector2(0, 0))

            self.draw_non_zoomable_assets()
        else:
            self.display_surface.blit(self.surface, Vector2(0, 0))

    def run(self) -> None:
        """
        This method runs both the event_loop and the draw methods and this
        is the only method needed to be called for this class to function.
        """

        self.__event_loop()

        self.__draw()