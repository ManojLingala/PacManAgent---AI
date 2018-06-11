(define (problem pacman0)

  (:domain pacman)

  (:objects x1 x2 x3 x4 x5 y1 y2 y3 y4 y5 a b c d p) ;x and y co-ordinates, dot names, power pill
  
    ;lays out the 5x5 grid and defines which movements will end in which positions.

  (:init

    (inc x1 x2) (inc x2 x3) (inc x3 x4) (inc x4 x5)

    (inc y1 y2) (inc y2 y3) (inc y3 y4) (inc y4 y5)

    (dec x5 x4) (dec x4 x3) (dec x3 x2) (dec x2 x1) 

    (dec y5 y4) (dec y4 y3) (dec y3 y2) (dec y2 y1)

    (at x1 y1) (dotat a x1 y1) (dotat b x5 y1) (dotat c x1 y5) (dotat d x5 y5)
    
    (wall x3 y3) (wall x4 y3) (wall x5 y3) (ghost x1 y3) (ghost x2 y3) (powerpillat p x2 y2))

  (:goal

    (and (eaten a) (eaten b) (eaten c) (eaten d) (at x1 y1))

  )
  )