import pygame

class Snake(object):
    SNAKE_UNIT = 30
    SEGMENT_SIZE = (SNAKE_UNIT, SNAKE_UNIT)

    def __init__(self, color, pos=[0, 0]):
        """
        A snake. It has a head and body and can move.
        """
        # create the head
        head_surface = pygame.Surface(self.SEGMENT_SIZE)
        head_surface.fill(color)
        self._head = {'surface': head_surface,'pos': pos}
        self._segments = []

        # The body color is the inverse of the head color.
        self.color = pygame.Color(0xFF - color.r, 0xFF - color.g,
                                  0xFF - color.b, color.a)


    def _add_segment(self, pos):
        """
        Add a segment to the body of the snake.
        """
        segment = pygame.Surface(self.SEGMENT_SIZE)
        segment.fill(self.color)
        segment.scroll(pos[0], pos[1])
        self._segments.append({'surface': segment,'pos': pos})


    def _get_rect(self, segment):
        rect = segment['surface'].get_rect()
        rect.move_ip(segment['pos'])
        return rect


    def _redraw_segment(self, segment, game_surface):
        rect = self._get_rect(segment)
        game_surface.blit(segment['surface'], rect)


    def get_rects(self):
        """
        Return the rectangles that make up the head and body of the
        snake.
        """
        for segment in [self._head] + self._segments:
            rect = self._get_rect(segment)
            yield rect


    def head_hit_body(self):
        """
        Return True if the head hit the body.
        """
        head_rect = self._get_rect(self._head)
        for segment in self._segments:
            segment_rect = self._get_rect(segment)
            if (head_rect.colliderect(segment_rect)):
                return True

        return False


    def update(self, game_surface):
        """
        Draw the snake onto the game surface.
        """
        self._redraw_segment(self._head, game_surface)

        for segment in self._segments:
            self._redraw_segment(segment, game_surface)


    def move(self, key, game_surface):
        """
        Move the snake.
        """
        game_rect = game_surface.get_rect()

        # Move the position of the head based on the provided keypress.
        old_head_pos = self._head['pos'][:]
        head_x, head_y = old_head_pos
        if (key == pygame.K_UP):
            head_y = head_y - self.SNAKE_UNIT
        elif (key == pygame.K_DOWN):
            head_y = head_y + self.SNAKE_UNIT
        ###
        # TODO:
        # Handle the remaining movement keys (as defined in ARROW_KEYS
        # in snakes.py).
        ###
        else:
            return

        # Don't actually move if that would put the head outside the
        # bounds of the screen.
        head_rect = self._head['surface'].get_rect()
        max_x = game_rect.right - head_rect.width
        max_y = game_rect.bottom - head_rect.height
        if (head_x < 0 or head_x > max_x or
            head_y < 0 or head_y > max_y):
            return

        # Don't actually move if the head would be moving backwards
        # into the body.
        if len(self._segments) > 0:
            first_segment = self._segments[0]['surface'].get_rect().move(
                self._segments[0]['pos'])
            if head_rect.move(old_head_pos).colliderect(first_segment):
                return

        # Update the head on the screen.
        self._head['pos'] = (head_x, head_y)
        self._redraw_segment(self._head, game_surface)

        # Update the body segments on the screen.
        old_segment_pos = old_head_pos
        for segment in self._segments:
            saved_pos = segment['pos'][:]
            segment['pos'] = old_segment_pos
            self._redraw_segment(segment, game_surface)
            old_segment_pos = saved_pos

        return True


    def try_to_eat(self, food_items):
        """
        Grow the snack by a segment for every food item it consumed.
        """
        # Only the head can eat snacks.
        head_rect = self._get_rect(self._head)

        for f in food_items[:]:
            if head_rect.colliderect(f.get_rect()):
                food_items.remove(f)

                if self._segments:
                    tail = self._segments[-1]
                else:
                    tail = self._head

                x = tail['pos'][0]
                y = tail['pos'][1] + self.SNAKE_UNIT
                self._add_segment([x, y])
